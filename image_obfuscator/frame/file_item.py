"""
Author       : noeru_desu
Date         : 2022-02-19 19:46:01
LastEditors  : noeru_desu
LastEditTime : 2023-01-21 10:50:21
"""
from abc import ABC
from gc import collect
from os.path import isfile, join, split
from typing import TYPE_CHECKING, Any, Generator, Optional, Union

from wx import BLACK, CURSOR_ARROWWAIT, CURSOR_ARROW, VERTICAL, HORIZONTAL, CallAfter

from image_obfuscator.constants import EMPTY_IMAGE, LIGHT_RED, PIL_RESAMPLING_FILTERS
from image_obfuscator.modes.base import EmptySettings
from image_obfuscator.modules.image import cal_best_size, cal_best_scale, open_image
from image_obfuscator.modules.version_adapter import load_encryption_attributes
from image_obfuscator.utils.misc_utils import LRUCache, LRUCacheRecord, add_to, get_factors

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import TreeItemId
    from image_obfuscator.constants import ImageReadErrorInfo
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.types import ModeInterface, ItemSettings, ItemEncryptionParameters, ScalableImageCacheHash, NormalImageCacheHash, ImageCacheHash
    from image_obfuscator.modules.argparse import Options
    from image_obfuscator.modules.image import WrappedImage


class PathData(object):
    root_path: str
    relative_path: str
    file_name: str
    relative_save_dir: str
    full_path: str

    def __setattr__(self, __name: str, __value: Any) -> None:
        """`PathData`只读"""
        raise AttributeError("can't set attribute")

    def __init__(self, root_path: str, relative_path: str, file_name: str, no_save_dir=False):
        setter = super().__setattr__
        setter('root_path', root_path)
        setter('relative_path', relative_path)
        setter('file_name', file_name)
        setter('relative_save_dir', '' if no_save_dir else join(split(root_path)[1], relative_path))
        setter('full_path', join(self.root_path, self.relative_path, self.file_name))


class Item(ABC):
    __slots__ = ('parent', 'parent_id')
    frame: 'MainFrame' = ...
    parent: Optional['FolderItem']
    parent_id: Optional['TreeItemId']

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        """删除自身项目

        Args:
            item_id (TreeItemId): 项目的TreeItemId (必须有效), 特殊情况: 在`del_item`参数为`False`时不会使用此参数
            del_item (bool): 是否从文件树移除项目并执行GC
        """
        raise NotImplementedError()

    def reload_item(self, dialog=True, refresh_preview=True):
        """重载自身项目的图像相关数据

        Args:
            dialog (bool, optional): 是否在重载完成后进行弹窗提示. 默认为`True`
            refresh_preview (bool, optional): 是否在重载完成后刷新预览图. 默认为`True`. `FolderItem.reload_item`中此参数无效, 恒为`False`

        Returns:
            tuple[int, int]: (重载成功数量, 重载失败数量)元组
        """
        raise NotImplementedError()

    def reload_done(self):
        """重载完后的操作"""
        if self.frame.tree_manager.stop_reloading_signal:
            self.frame.stop_reloading(False, False)
        self.frame.stop_reloading_func.init()
        self.frame.set_cursor(CURSOR_ARROW)


class ImageEncryptionAttributes(object):
    __slots__ = ('decryption_mode', 'settings')

    def __init__(self, decryption_mode: 'ModeInterface', settings: 'ItemSettings') -> None:
        self.decryption_mode = decryption_mode
        self.settings = settings

    def backtrack_interface(self):
        self.settings.backtrack_interface()


EmptyEncryptionAttributes = ImageEncryptionAttributes(None, EmptySettings)


class PreviewCache(LRUCache):
    __slots__ = ()

    lru_cache_recorder = LRUCacheRecord()
    program_options: 'Options' = ...

    def __init__(self) -> None:
        super().__init__(self.program_options.maximum_redundant_cache_length)

    @property
    def _maxlen(self):
        return self.program_options.maximum_redundant_cache_length

    @_maxlen.setter
    def _maxlen(self, v): pass


class ImageItemCache(object):
    """图像项目缓存控制器"""
    __slots__ = (
        '_item', 'initial_preview', 'preview_cache', 'preview_size', '_encryption_attributes', '_loaded_image',
        'loading_encryption_attributes_error', '_best_layout', 'loaded_image_size', '_image_panel_size_for_best_layout',
        'encryption_attributes_from_file', '_size_factors'
    )
    lru_cache_recorder = LRUCacheRecord()

    def __init__(self, item: 'ImageItem', loaded_image: 'Image'):
        """
        Args:
            item (ImageItem): `ImageItem`实例
            loaded_image (Image, optional): 已加载的图像. 默认为`None`.
        """
        self._item: 'ImageItem' = item
        self.initial_preview: Image = None
        self.preview_size: tuple[int, int] = None
        self.preview_cache: LRUCache['ImageCacheHash', 'WrappedImage'] = PreviewCache()
        self.loading_encryption_attributes_error: Optional[str] = None
        self._encryption_attributes: Optional['ImageEncryptionAttributes'] = None
        self._size_factors: Optional[tuple[int]] = None
        self.encryption_attributes_from_file = False
        self._loaded_image = loaded_image
        self.lru_cache_recorder.record_cache(item.cache_id, self.loaded_image_cache_deleter)
        self.loaded_image_size = loaded_image.size
        self._image_panel_size_for_best_layout = None
        self._best_layout = VERTICAL

    @property
    def loaded_image(self) -> 'Image':
        """已加载的图像数据

        如果缓存中不存在, 将重新从文件中加载图像

        Returns:
            Image: `PIL.Image.Image`实例
        """
        if self._loaded_image is None or self._loaded_image is EMPTY_IMAGE:
            if __debug__:
                self._item.frame.logger.debug(f'从磁盘上读取图像[{self._item.loaded_image_path}]')
            reload_encryption_attributes = self._item.loading_image_data_error is not None    # 是否需要在读取图像数据后读取加密参数
            self._loaded_image, loading_image_data_error = open_image(self._item.loaded_image_path)
            if loading_image_data_error is None:
                self.loaded_image_size = self._loaded_image.size
                if reload_encryption_attributes:
                    self._item.load_encryption_attributes_from_file()
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, BLACK)
            elif loading_image_data_error != self._item.loading_image_data_error:
                self._item.loading_image_data_error = loading_image_data_error
                self._item.frame.dialog.async_error(loading_image_data_error.info, '重新载入图像时出现错误')
                self._item.encrypted_image = False
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, LIGHT_RED)
        else:
            self.lru_cache_recorder.record_cache(self._item.cache_id, self.loaded_image_cache_deleter)
        return self._loaded_image

    @loaded_image.setter
    def loaded_image(self, v):
        self._loaded_image = v

    def loaded_image_cache_deleter(self):
        self._loaded_image = None
        if __debug__:
            self._item.frame.logger.debug(f'原始图像缓存被删除[{self._item.loaded_image_path}]')

    @property
    def encryption_attributes(self) -> 'ImageEncryptionAttributes':
        """被加密图像的加密参数

        如果缓存中不存在, 将重新从文件中加载加密参数

        Returns:
            BaseSettings
        """
        if self._encryption_attributes is None:
            self._item.load_encryption_attributes_from_file()
        return self._encryption_attributes

    @encryption_attributes.setter
    def encryption_attributes(self, v):
        self._encryption_attributes = v

    @property
    def best_layout(self):
        image_panel_size = self._item.frame.controller.image_panel_size
        if image_panel_size != self._image_panel_size_for_best_layout:
            image_panel_w, image_panel_h = self._image_panel_size_for_best_layout = image_panel_size
            v_scale = cal_best_scale(*self.loaded_image_size, image_panel_w, image_panel_h // 2)
            h_scale = cal_best_scale(*self.loaded_image_size, image_panel_w // 2, image_panel_h)
            self._best_layout = VERTICAL if v_scale >= h_scale else HORIZONTAL
        return self._best_layout

    @property
    def size_factors(self):
        if self._size_factors is None:
            self._size_factors = (
                tuple(get_factors(self.loaded_image_size[0], False)),
                tuple(get_factors(self.loaded_image_size[1], False))
            )
        return self._size_factors

    def refresh_cache(self):
        self.clear_extra_cache()
        self.loaded_image_size = self.loaded_image.size

    def clear_extra_cache(self):
        """清除缓存"""
        self.initial_preview = None
        self.preview_size = None
        self._encryption_attributes = None
        self.encryption_attributes_from_file = False
        self._image_panel_size_for_best_layout = None

    def del_cache(self):
        """删除各缓存实例(不包括自身)"""
        del self.initial_preview
        del self.preview_cache
        del self.preview_size
        del self._encryption_attributes
        del self._loaded_image


class ImageItem(Item):
    """存储每个载入的图像的相关信息"""
    __slots__ = (
        'cache', 'path_data', '_loaded_image_path', '_settings_dict', '_settings', 'item_id', 'selected',
        'no_file', 'encrypted_image', 'loading_image_data_error', '_proc_mode', 'settings_source',
        'cache_id', 'cached_on_disk'
    )

    def __init__(self, loaded_image: Optional['Image'], path_data: 'PathData', settings: 'ItemSettings' = ..., no_file=False, cached_on_disk=False):
        """
        Args:
            frame (MainFrame): `MainFrame`实例
            loaded_image (Image): 已加载的图像实例(可为`None`)
            path_data (PathData): 记录了图像原始文件路径的`PathData`实例
            settings (Settings, optional): 图像当前的加密设置(不给出时将使用当前的默认加密设置)
            no_file (bool, optional): 是否没有原始文件. `默认为False`
            cached_on_disk (bool, optional): 是否已将图像缓存到磁盘中
        """
        self.path_data = path_data
        self._proc_mode = self.frame.mode_manager.default_mode
        self.settings_source = 0
        self._loaded_image_path = path_data.file_name if no_file else path_data.full_path
        self.cache_id = hash(self._loaded_image_path)
        self._settings_dict: dict[int, 'ItemSettings'] = {self.proc_mode.mode_id: self.frame.mode_manager.default_settings.copy() if settings is Ellipsis else settings}
        self._settings = self._settings_dict[self.proc_mode.mode_id]

        self.item_id: TreeItemId = ...
        self.parent: Optional['FolderItem'] = None
        self.parent_id: Optional['TreeItemId'] = None
        self.selected: bool = False
        self.no_file: bool = no_file
        self.cached_on_disk: bool = cached_on_disk
        self.loading_image_data_error: Optional['ImageReadErrorInfo'] = None
        self.encrypted_image: Optional[bool] = None

        self.cache = ImageItemCache(self, loaded_image)

        if self.no_file:
            self.encrypted_image = False
            self.cache._encryption_attributes = EmptyEncryptionAttributes
            self.cache.loading_encryption_attributes_error = f'来自剪贴板的图像[{self.path_data.file_name}]不支持解密操作'
        else:
            self.cache.loading_encryption_attributes_error = None

    def set_settings_source(self, source: int):
        self.settings_source = source
        if self.selected:
            self.frame.controller.set_settings_source(source, False)

    @property
    def loaded_image_path(self):
        return self.frame.image_disk_cache.get_cache_path(self._loaded_image_path) if self.cached_on_disk else self._loaded_image_path

    @property
    def proc_mode(self):
        return self._proc_mode

    @proc_mode.setter
    def proc_mode(self, v: 'ModeInterface'):
        if v.mode_id == self._proc_mode.mode_id:
            return
        self._proc_mode = v
        mode_id = v.mode_id
        if mode_id in self._settings_dict:
            self._settings = self._settings_dict[mode_id]
        else:
            self._settings_dict[mode_id] = self._settings = v.default_settings.copy()

    @property
    def settings(self) -> 'ItemSettings':
        """当前`proc_mode`对应模式的设置实例\n
        如果需要对此属性进行赋值, 请确保赋值前`proc_mode`属性已正确设置

        Returns:
            BaseSettings
        """
        return self._settings

    @settings.setter
    def settings(self, v: 'ItemSettings'):
        self._settings_dict[self._proc_mode.mode_id] = self._settings = v

    def sync_options_from_interface(self):
        self.proc_mode = self.frame.controller.proc_mode_interface
        if self.settings_source == 0:
            self.settings.sync_from_interface()

    @property
    def best_layout(self):
        return self.cache.best_layout

    def on_select(self):
        self.selected = True

    def unselect(self):
        """取消选中时的相关操作"""
        self.selected = False
        if self.frame.program_options.no_extra_data_cache:
            self.cache.clear_extra_cache()
            if __debug__:
                self.frame.logger.debug(f'额外缓存被删除[{self.loaded_image_path}]')
        self.cache.preview_cache.reserve(1)
        PreviewCache.lru_cache_recorder.record_cache(self.cache_id, self.cache.preview_cache.clear)

    def display_initial_preview(self, cache=True) -> bool:
        """在界面中显示原始图像预览图

        Args:
            cache (bool, optional): 是否尝试使用缓存. 默认为`True`

        Returns:
            bool: 命中缓存返回`False`, 未命中则生成并返回`True`
        """
        size = self.frame.controller.preview_size
        if cache and not self.frame.program_options.disable_cache and self.cache.initial_preview is not None and size == self.cache.preview_size:
            self.frame.controller.imported_image = self.cache.initial_preview
            return False
        if __debug__:
            self.frame.logger.debug(f'重新生成原始图像预览图并缓存(原本是否为None: {self.cache.initial_preview is None})[{self.loaded_image_path}]')
        image = self.cache.loaded_image.resize(cal_best_size(*self.cache.loaded_image.size, *size), PIL_RESAMPLING_FILTERS[self.frame.controller.resampling_filter_id])
        self.frame.controller.imported_image = image
        self.cache.preview_size = size
        self.cache.initial_preview = image
        return True

    def display_processed_preview(self, cache=True, resize=True, cache_hash: int = ...) -> bool:
        """在界面中显示处理结果预览图

        Args:
            cache (bool, optional): 是否尝试使用缓存. 默认为`True`
            resize (bool, optional): 如果为可缩放缓存, 是否缩放至合适大小显示. 默认为`True`
            cache_hash (int, optional): 指定需要显示的缓存的cache_hash. 不指定时将由`settings`生成

        Returns:
            bool: 命中缓存返回`False`, 未命中则生成并返回`True`
        """
        if cache and not self.frame.program_options.disable_cache:
            if cache_hash is Ellipsis:
                cache_hash = self.scalable_cache_hash if (self.frame.controller.preview_source == 1) or (self.frame.controller.proc_mode_interface.always_use_orig_image) else self.normal_cache_hash
            cache = self.cache.preview_cache.get(cache_hash)
            if cache is not None:
                self.frame.controller.previewed_bitmap = (
                    cache.gen_wxBitmap(
                        self.frame.controller.preview_size,
                        self.frame.controller.resampling_filter_id
                    )
                    if resize and cache.scalable else cache.wxBitmap
                )
                return False
        if __debug__:
            self.frame.logger.debug(f'重新生成处理结果并缓存[{self.loaded_image_path}]')
        self.frame.preview_generator.generate_preview()
        return True

    def display_encryption_attributes(self):
        """如果当前图像包含加密参数, 则在界面中显示加密参数\n
        如果尚未检测是否包含加密参数, 则进行检测并加载后再进行上述操作
        """
        if self.cache._encryption_attributes is None:
            self.load_encryption_attributes_from_file()
        if self.encrypted_image:
            self.frame.controller.backtrack_interface(self.cache.encryption_attributes.settings, self.cache.encryption_attributes.decryption_mode)

    def load_encryption_attributes_from_file(self):
        """加载图像加密参数\n
        如果当前实例`no_file`属性为`True`或图像原始文件不存在, 则跳过操作
        """
        if self.no_file or not isfile(self.loaded_image_path):
            self.cache._encryption_attributes = EmptyEncryptionAttributes
            return
        self.load_encryption_attributes(*load_encryption_attributes(self.loaded_image_path), True)

    def load_encryption_attributes(self, encryption_attributes, loading_encryption_attributes_error, from_file: bool):
        """加载图像加密参数\n
        如果当前实例`no_file`属性为`True`或图像原始文件不存在, 则跳过操作\n
        加载成功后, 返回True
        """
        if __debug__:
            self.frame.logger.debug(f'尝试读取加密参数[{self.loaded_image_path}]')
        self.cache.loading_encryption_attributes_error = loading_encryption_attributes_error
        if self.cache.loading_encryption_attributes_error is None:
            mode = self.frame.mode_manager.modes.get(encryption_attributes['corresponding_decryption_mode'], None)
            if mode is None:
                self.frame.dialog.warning(
                    f'该图像对应的解密模式({encryption_attributes["corresponding_decryption_mode"]})不存在, 无法解密',
                    '指定的解密模式不存在'
                )
                self.encrypted_image = False
                if self.proc_mode.requires_encryption_parameters and self.proc_mode.encryption_parameters_must_be_used:
                    self.proc_mode = self.frame.mode_manager.default_mode_that_can_be_set_as_default
                self.cache._encryption_attributes = EmptyEncryptionAttributes
                return False
            self.cache._encryption_attributes = ImageEncryptionAttributes(
                mode, mode.instantiate_encryption_parameters_cls(
                    mode.encryption_parameters_cls.deserialize_encrypted_parameters(encryption_attributes['data'])
                    if isinstance(encryption_attributes['data'], str)
                    else encryption_attributes['data']      # 兼容旧版加密参数
                )
            )
            self.encrypted_image = True
            self.proc_mode = mode
            if from_file:
                self.cache.encryption_attributes_from_file = True
                self.set_settings_source(1)
            else:
                self.cache.encryption_attributes_from_file = False
            return True
        else:
            self.cache._encryption_attributes = EmptyEncryptionAttributes
            self.encrypted_image = False
            if self.proc_mode.requires_encryption_parameters and self.proc_mode.encryption_parameters_must_be_used:
                self.proc_mode = self.frame.mode_manager.default_mode_that_can_be_set_as_default
        return False

    def is_correct_decryption_mode(self, mode: 'ModeInterface') -> bool:
        if self.encrypted_image:
            decryption_mode = self.cache.encryption_attributes.decryption_mode
            return decryption_mode.requires_encryption_parameters and mode.mode_id == decryption_mode.mode_id
        return False

    def enable_available_settings_source_btn(self, proc_mode: 'ModeInterface' = ..., sync_to_item: bool = True):
        if proc_mode is Ellipsis:
            proc_mode = self.proc_mode
        if proc_mode.requires_encryption_parameters:
            if self.is_correct_decryption_mode(proc_mode) and self.cache.encryption_attributes_from_file:
                self.frame.controller.enable_settings_source_btn(1, sync_to_item=sync_to_item)
            elif not proc_mode.encryption_parameters_must_be_used:
                self.frame.controller.enable_settings_source_btn((0, 2), self.settings_source, sync_to_item)
        else:
            self.frame.controller.enable_settings_source_btn(0, sync_to_item=sync_to_item)

    @property
    def available_settings_inst(self) -> tuple[Union['ItemSettings', 'EmptySettings'], Union['ItemEncryptionParameters', 'EmptySettings']]:
        match self.settings_source:
            case 0:
                return self.settings, EmptySettings
            case 1:
                return EmptySettings, self.encryption_attributes.settings
            case 2:
                return EmptySettings, self.encryption_attributes.settings
            case 3:
                return self.settings, self.encryption_attributes.settings
        raise ValueError()

    @property
    def encryption_attributes(self) -> 'ImageEncryptionAttributes':
        """当图像包含加密参数时返回`self.cache.encryption_attributes`, 否则返回`EmptyEncryptionAttributes`"""
        return self.cache.encryption_attributes

    @property
    def scalable_cache_hash(self) -> 'ScalableImageCacheHash':
        return hash((
            self.proc_mode.mode_id, self.frame.controller.settings_source, self._settings.settings_tuple,
            self.encryption_attributes.settings.settings_tuple
        ))

    @property
    def normal_cache_hash(self) -> 'NormalImageCacheHash':
        return hash((
            self.proc_mode.mode_id, self.frame.controller.settings_source, self._settings.settings_tuple,
            self.encryption_attributes.settings.settings_tuple, self.frame.controller.resampling_filter_id,
            self.frame.controller.preview_source, *self.frame.controller.preview_size
        ))

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        if del_item:
            self.frame.set_cursor(CURSOR_ARROWWAIT)
            self.frame.imageTreeCtrl.Delete(item_id)
            if self.parent is not None:
                del self.parent.children[item_id]
        if self.cached_on_disk:
            self.frame.image_disk_cache.remove(self._loaded_image_path)
        del self.frame.tree_manager.file_dict[self._loaded_image_path]
        self.cache.del_cache()
        PreviewCache.lru_cache_recorder.remove_cache_recode(self.cache_id)
        ImageItemCache.lru_cache_recorder.remove_cache_recode(self.cache_id)
        del self.cache
        if del_item:
            self.frame.set_cursor(CURSOR_ARROW)
            collect()

    def reload_item(self, dialog=True, refresh_preview=True) -> Optional[tuple[int, int]]:
        if self.no_file:
            self.frame.dialog.async_warning(f'来自剪贴板的图像[{self.path_data.file_name}]不支持重载操作')
            self.reload_done()
            return 0, 0
        if self.frame.tree_manager.stop_reloading_signal:
            return 0, 0
        if dialog:
            self.frame.set_cursor(CURSOR_ARROWWAIT)

        loaded_image, error = open_image(self.loaded_image_path, False)
        if error is not None:
            if dialog:
                self.frame.dialog.async_warning(f'{self.path_data.file_name}重载失败: {error}')
                self.reload_done()
            self.frame.imageTreeCtrl.SetItemTextColour(self.item_id, LIGHT_RED)
            return 0, 1
        else:
            self.frame.imageTreeCtrl.SetItemTextColour(self.item_id, BLACK)
        self.cache.loaded_image = loaded_image

        # 重置缓存与设置源
        self.cache.loaded_image_size = loaded_image.size
        self.cache.refresh_cache()
        self.settings_source = 0
        self.frame.controller.reset_settings_source(sync_to_item=False)

        self.load_encryption_attributes_from_file()
        if dialog:
            self.enable_available_settings_source_btn()
            self.frame.dialog.async_info(f'{self.path_data.file_name}重载成功')
            self.reload_done()
        if refresh_preview:
            if self.encrypted_image:
                CallAfter(self._refresh_encrypted_image)
            else:
                self.frame.controller.backtrack_interface(self.settings, self.proc_mode)
                self.frame.force_refresh_preview()
        return 1, 0

    def _refresh_encrypted_image(self):
        self.frame.controller.backtrack_interface(self.cache.encryption_attributes.settings, self.cache.encryption_attributes.decryption_mode)
        self.frame.force_refresh_preview()


class FolderItem(Item):
    __slots__ = ('path', 'name', 'children', 'parent_dir')

    def __init__(self, path: str):
        """
        Args:
            frame (MainFrame): `MainFrame`实例
            path (str): 文件夹路径
        """
        self.path = path
        self.parent_dir, self.name = split(path)
        self.children: dict[TreeItemId, Union['FolderItem', 'ImageItem']] = {}
        self.parent: Optional['FolderItem'] = None
        self.parent_id: Optional['TreeItemId'] = None

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        if del_item:
            self.frame.set_cursor(CURSOR_ARROWWAIT)
        for id, data in tuple(self.children.items()):
            data.del_item(id, False)
            del self.children[id]
        if del_item:
            self.frame.imageTreeCtrl.Delete(item_id)
            if self.parent is not None:
                del self.parent.children[item_id]
        if self.path in self.frame.tree_manager.root_dir_dict:
            del self.frame.tree_manager.root_dir_dict[self.path]
        else:
            del self.frame.tree_manager.dir_dict[self.path]
        if del_item:
            self.frame.set_cursor(CURSOR_ARROW)
            collect()

    def reload_item(self, dialog=True, refresh_preview=False):
        if self.frame.tree_manager.stop_reloading_signal:
            return 0, 0
        if dialog:
            self.frame.set_cursor(CURSOR_ARROWWAIT)
        nums = [0, 0]
        for data in self.children.values():
            if self.frame.tree_manager.stop_reloading_signal:
                break
            add_to(data.reload_item(False, False), nums)
        if dialog:
            self.frame.dialog.async_info(f'重载成功: {nums[0]}个, 失败: {nums[1]}个')
            self.reload_done()
        return nums

    def all_included_items(self, sub_folder: bool = True) -> Generator[tuple[None, None, ImageItem], None, None]:
        for i in self.children.values():
            if sub_folder and isinstance(i, FolderItem):
                    yield from i.all_included_items()
            elif isinstance(i, ImageItem):
                yield None, None, i

    def walk(self, sub_folder: bool = True, path_offset: int = ...) -> Generator[tuple[str, str, ImageItem], None, None]:
        """遍历全部子项目

        Args:
            sub_folder (bool, optional): 是否遍历子目录. 默认为`True`
            path_offset (int, optional): 绝对路径截断位置. 默认为当前文件夹的上级路径长度
            (`len(self.parent_dir) + 1`, 即不包含自身, `+1`用于删除`/`)

        Yields:
            Generator[tuple[str, str, ImageItem], None, None]: (截断后的文件夹绝对路径, 文件夹名称, 子项目)
        """
        if path_offset is Ellipsis:
            path_offset = len(self.parent_dir) + 1
        for i in self.children.values():
            if sub_folder and isinstance(i, FolderItem):
                    yield from i.walk(path_offset=path_offset)
            elif isinstance(i, ImageItem):
                yield self.path[path_offset:], self.name, i
