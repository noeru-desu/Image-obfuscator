"""
Author       : noeru_desu
Date         : 2022-02-19 19:46:01
LastEditors  : noeru_desu
LastEditTime : 2022-09-06 12:03:48
Description  : 图像项目
"""
from abc import ABC
from collections import OrderedDict
from gc import collect
from os.path import isfile, join, split
from typing import TYPE_CHECKING, Any, Generator, Optional, Union

from wx import BLACK, CURSOR_ARROWWAIT, CURSOR_ARROW, VERTICAL, HORIZONTAL, Bitmap, CallAfter

from image_obfuscator.constants import LIGHT_RED, PIL_RESAMPLING_FILTERS
from image_obfuscator.modes.base import EmptySettings
from image_obfuscator.modules.image import cal_best_size, cal_best_scale, open_image
from image_obfuscator.modules.version_adapter import load_encryption_attributes
from image_obfuscator.utils.misc_utils import add_to

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import TreeItemId
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.types import ModeInterface, ItemSettings, ItemEncryptionParameters, NormalImageCacheHash, ScalableImageCacheHash, ImageCacheHash
    from image_obfuscator.modules.argparse import Parameters
    from image_obfuscator.modules.image import WrappedImage


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


class PreviewCache(object):
    """预览图(处理结果)缓存"""
    __slots__ = ('scalable_cache', 'normal_cache')
    startup_parameters: 'Parameters' = ...

    def __init__(self) -> None:
        self.normal_cache: OrderedDict['NormalImageCacheHash', Bitmap] = OrderedDict()
        self.scalable_cache: OrderedDict['ScalableImageCacheHash', WrappedImage] = OrderedDict()

    def clear_redundant_cache(self) -> None:
        """清理冗余缓存, 即从普通缓存与可缩放缓存中删除除最新缓存外的其他缓存"""
        if len(self.normal_cache) > 1:
            for i in tuple(self.normal_cache)[:-1]:
                del self.normal_cache[i]
        if len(self.scalable_cache) > 1:
            for i in tuple(self.scalable_cache)[:-1]:
                del self.scalable_cache[i]

    def add_cache(self, cache_hash: 'ImageCacheHash', image: Union['WrappedImage', 'Bitmap']) -> None:
        """添加缓存(自动识别缓存类型)

        Args:
            cache_hash (Hashable): 用于标记缓存的可哈希对象(为`int`时不进行`hash(cache_hash)`处理)
            image (WrappedImage | Bitmap): 需要添加到缓存的图像实例
        """
        if isinstance(image, Bitmap):
            self.add_normal_cache(cache_hash, image)
        elif image.scalable:
            self.add_scalable_cache(cache_hash, image)
        else:
            self.add_normal_cache(cache_hash, image.wxBitmap)

    def add_normal_cache(self, cache_hash: 'NormalImageCacheHash', bitmap: 'Bitmap' = None) -> None:
        """添加普通缓存

        如果`cache_hash`已存在于缓存中, 将会把缓存位置放到最后, 并且`bitmap`参数可以为`None`\n
        如果`cache_hash`不存在于缓存中, 则`bitmap`参数不可为`None`\n
        如果缓存长度超过设定的最大长度, 将会删除第一个缓存

        Args:
            cache_hash (Hashable): 用于标记缓存的可哈希对象
            bitmap (Bitmap, optional): 需要添加到缓存的`wx.Bitmap`实例. 默认为`None`.
        """
        if cache_hash in self.normal_cache:
            self.normal_cache.move_to_end(cache_hash)
            if bitmap is not None:
                self.normal_cache[cache_hash] = bitmap
            return
        assert bitmap is not None, 'Bitmap cannot be NoneType when the cache_hash does not exist in the cache.'
        if len(self.normal_cache) >= self.startup_parameters.maximum_redundant_cache_length:
            self.normal_cache.popitem(False)
        self.normal_cache[cache_hash] = bitmap

    def add_scalable_cache(self, cache_hash: 'ScalableImageCacheHash', image: 'WrappedImage' = None) -> None:
        """添加可缩放缓存

        如果`cache_hash`已存在于缓存中, 将会把缓存位置放到最后, 并且`image`参数可以为`None`\n
        如果`cache_hash`不存在于缓存中, 则`image`参数不可为`None`\n
        如果缓存长度超过设定的最大长度, 将会删除第一个缓存

        Args:
            cache_hash (Hashable): 用于标记缓存的可哈希对象
            image (WrappedImage, optional): 需要添加到缓存的`WrappedImage`实例. 默认为`None`.
        """
        if cache_hash in self.scalable_cache:
            self.scalable_cache.move_to_end(cache_hash)
            if image is not None:
                self.scalable_cache[cache_hash] = image
            return
        assert image is not None, 'Image cannot be NoneType when the cache_hash does not exist in the cache.'
        if len(self.scalable_cache) >= self.startup_parameters.maximum_redundant_cache_length:
            self.scalable_cache.popitem(False)
        self.scalable_cache[cache_hash] = image

    def get_cache(self, cache_hash: 'ImageCacheHash') -> Optional[Union['WrappedImage', 'Bitmap']]:
        """获取缓存(优先搜索普通缓存)

        如果`cache_hash`不存在于缓存中, 将返回`None`

        Args:
            cache_hash (Hashable): 用于标记缓存的可哈希对象

        Returns:
            WrappedImage | Bitmap | None
        """
        if self.startup_parameters.disable_cache:
            return None
        if cache_hash in self.normal_cache:
            self.add_normal_cache(cache_hash)
            return self.normal_cache[cache_hash]
        if cache_hash in self.scalable_cache:
            self.add_scalable_cache(cache_hash)
            return self.scalable_cache[cache_hash]
        return None

    def get_normal_cache(self, cache_hash: 'NormalImageCacheHash') -> Optional['Bitmap']:
        """获取普通缓存

        如果`cache_hash`不存在于缓存中, 将返回`None`

        Args:
            cache_hash (Hashable): 用于标记缓存的可哈希对象

        Returns:
            Bitmap | None
        """
        if self.startup_parameters.disable_cache:
            return None
        if cache_hash in self.normal_cache:
            self.add_normal_cache(cache_hash)
            return self.normal_cache[cache_hash]
        return None

    def get_scalable_cache(self, cache_hash: 'ScalableImageCacheHash') -> Optional['WrappedImage']:
        """获取可缩放缓存

        如果`cache_hash`不存在于缓存中, 将返回`None`

        Args:
            cache_hash (Hashable): 用于标记缓存的可哈希对象

        Returns:
            WrappedImage | None
        """
        if self.startup_parameters.disable_cache:
            return None
        if cache_hash in self.scalable_cache:
            self.add_scalable_cache(cache_hash)
            return self.scalable_cache[cache_hash]
        return None

    def clear(self):
        """清空缓存"""
        self.scalable_cache.clear()
        self.normal_cache.clear()

    def delete(self):
        """删除缓存与自身实例"""
        del self.scalable_cache
        del self.normal_cache
        del self


class ImageEncryptionAttributes(object):
    __slots__ = ('decryption_mode', 'settings')

    def __init__(self, decryption_mode: 'ModeInterface', settings: 'ItemSettings') -> None:
        self.decryption_mode = decryption_mode
        self.settings = settings

    def backtrack_interface(self):
        self.settings.backtrack_interface()


EmptyEncryptionAttributes = ImageEncryptionAttributes(None, EmptySettings)


class ImageItemCache(object):
    """图像项目缓存控制器"""
    __slots__ = (
        '_item', 'initial_preview', 'previews', 'preview_size', '_encryption_attributes', '_loaded_image',
        'loading_encryption_attributes_error', '_best_layout', 'loaded_image_size', '_image_panel_size_for_best_layout',
        'encryption_attributes_from_file'
    )

    def __init__(self, item: 'ImageItem', loaded_image: 'Image', force_cache: bool = False):
        """
        Args:
            item (ImageItem): `ImageItem`实例
            loaded_image (Image, optional): 已加载的图像. 默认为`None`.
        """
        self._item = item
        self.initial_preview: Image = None
        self.preview_size: tuple[int, int] = None
        self.previews = PreviewCache()
        self.loading_encryption_attributes_error: Optional[str] = None
        self._encryption_attributes: Optional['ImageEncryptionAttributes'] = None
        self.encryption_attributes_from_file = False
        self._loaded_image = loaded_image if force_cache or not self._item.frame.startup_parameters.low_memory else None
        self.loaded_image_size = loaded_image.size
        self._image_panel_size_for_best_layout = None
        self._best_layout = VERTICAL

    @property
    def loaded_image(self) -> 'Image':
        """已加载的图像数据

        如果缓存中不存在, 将重新从文件中加载图像\n
        使用低内存占用模式时注意, 如果项目未被选中, 则每次使用此属性时都将重新从文件中加载图像, 所以如果有使用的必要, 请使用临时变量存储获取到的实例

        Returns:
            Image: `PIL.Image.Image`实例
        """
        if self._loaded_image is None:
            reload_encryption_attributes = self._item.loading_image_data_error is not None    # 是否需要在读取图像数据后读取加密参数
            self._loaded_image, self._item.loading_image_data_error = open_image(self._item.loaded_image_path)
            if self._item.loading_image_data_error is not None:
                self._item.frame.dialog.async_error(self._item.loading_image_data_error, '重新载入图像时出现错误')
                self._item.encrypted_image = False
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, LIGHT_RED)
            else:
                if reload_encryption_attributes:
                    self._item.load_encryption_attributes_from_file()
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, BLACK)
        if self._item.frame.startup_parameters.low_memory and not self._item.selected:  # 为防止低内存占用模式下的内存泄露, 在项目未被选中时不可缓存图像数据
            loaded_image = self._loaded_image
            del self._loaded_image
            return loaded_image
        return self._loaded_image

    @loaded_image.setter
    def loaded_image(self, v):
        self._loaded_image = v

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

    def refresh_cache(self):
        self.clear_cache()
        self.loaded_image_size = self.loaded_image.size

    def clear_cache(self):
        """清除缓存"""
        self.initial_preview = None
        self.previews.clear()
        self.preview_size = None
        self._encryption_attributes = None
        self.encryption_attributes_from_file = False

    def del_cache(self):
        """删除各缓存实例(不包括自身)"""
        del self.initial_preview
        self.previews.delete()
        del self.preview_size
        del self._encryption_attributes
        del self._loaded_image


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


class ImageItem(Item):
    """存储每个载入的图像的相关信息"""
    __slots__ = (
        'cache', 'path_data', 'loaded_image_path', '_settings_dict', '_settings', 'item_id', 'selected',
        'no_file', 'keep_cache_loaded_image', 'encrypted_image', 'loading_image_data_error', '_proc_mode',
        'settings_source'
    )

    def __init__(self, loaded_image: Optional['Image'], path_data: 'PathData', settings: 'ItemSettings' = ..., no_file=False, keep_cache_loaded_image=False):
        """
        Args:
            frame (MainFrame): `MainFrame`实例
            loaded_image (Image): 已加载的图像实例(可为`None`)
            path_data (PathData): 记录了图像原始文件路径的`PathData`实例
            settings (Settings, optional): 图像当前的加密设置(不给出时将使用当前的默认加密设置)
            no_file (bool, optional): 是否没有原始文件. `默认为False`
            keep_cache_loaded_image (bool, optional): 是否在低内存占用模式下保留原始图像数据缓存(一般用于从剪切板加载的图像). 默认为`False`
        """
        self.path_data = path_data
        self._proc_mode = self.frame.mode_manager.default_mode
        self.settings_source = 0
        self.loaded_image_path = path_data.file_name if no_file else path_data.full_path
        self._settings_dict: dict[int, 'ItemSettings'] = {self.proc_mode.mode_id: self.frame.mode_manager.default_settings.copy() if settings is Ellipsis else settings}
        self._settings = self._settings_dict[self.proc_mode.mode_id]

        self.item_id: TreeItemId = ...
        self.parent: Optional['FolderItem'] = None
        self.parent_id: Optional['TreeItemId'] = None
        self.selected = False
        self.no_file = no_file
        self.keep_cache_loaded_image = keep_cache_loaded_image
        self.loading_image_data_error = None
        self.encrypted_image: bool = None

        self.cache = ImageItemCache(self, loaded_image, keep_cache_loaded_image)

        if self.no_file:
            self.encrypted_image = False
            self.cache.loading_encryption_attributes_error = f'来自剪贴板的图像[{self.path_data.file_name}]不支持解密操作'
        else:
            self.cache.loading_encryption_attributes_error = None

    def set_settings_source(self, source: int):
        self.settings_source = source
        if self.selected:
            self.frame.controller.set_settings_source_used(source, False)

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

    def unselect(self):
        """取消选中时的相关操作"""
        self.selected = False
        if self.frame.startup_parameters.low_memory:
            if not self.keep_cache_loaded_image:
                self.cache._loaded_image = None
            self.cache.clear_cache()
        else:
            self.cache.previews.clear_redundant_cache()

    def display_initial_preview(self, cache=True) -> bool:
        """在界面中显示原始图像预览图

        Args:
            cache (bool, optional): 是否尝试使用缓存. 默认为`True`

        Returns:
            bool: 命中缓存返回`False`, 未命中则生成并返回`True`
        """
        size = self.frame.controller.preview_size
        if cache and not self.frame.startup_parameters.disable_cache and self.cache.initial_preview is not None and size == self.cache.preview_size:
            self.frame.controller.imported_image = self.cache.initial_preview
            return False
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
        if cache and not self.frame.startup_parameters.disable_cache:
            gen_hash = cache_hash is Ellipsis
            if gen_hash:
                cache_hash = self.scalable_cache_hash
            if cache_hash in self.cache.previews.scalable_cache:
                self.frame.controller.previewed_bitmap = (
                    self.cache.previews.scalable_cache[cache_hash].gen_wxBitmap(
                        self.frame.controller.preview_size,
                        self.frame.controller.resampling_filter_id,
                    )
                    if resize
                    else self.cache.previews.scalable_cache[cache_hash].wxBitmap
                )
                return False
            if gen_hash:
                cache_hash = self.normal_cache_hash
            if cache_hash in self.cache.previews.normal_cache:
                self.frame.controller.previewed_bitmap = self.cache.previews.get_normal_cache(cache_hash)
                return False
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
        如果当前实例`no_file`属性为`True`或图像原始文件不存在, 则跳过操作\n
        加载成功后, 将自动切换项目设置中的处理模式为解密模式
        """
        if self.no_file or not isfile(self.loaded_image_path):
            return
        self.load_encryption_attributes(*load_encryption_attributes(self.loaded_image_path), True)

    def load_encryption_attributes(self, encryption_attributes, loading_encryption_attributes_error, from_file: bool):
        """加载图像加密参数\n
        如果当前实例`no_file`属性为`True`或图像原始文件不存在, 则跳过操作\n
        加载成功后, 将自动切换项目设置中的处理模式为解密模式, 返回True
        """
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
            self.proc_mode.mode_id, self.frame.controller.settings_source_used, self._settings.settings_tuple,
            self.encryption_attributes.settings.settings_tuple
        ))

    @property
    def normal_cache_hash(self) -> 'NormalImageCacheHash':
        return hash((
            self.proc_mode.mode_id, self.frame.controller.settings_source_used, self._settings.settings_tuple,
            self.encryption_attributes.settings.settings_tuple, self.frame.controller.resampling_filter_id,
            self.frame.controller.preview_source, *self.frame.controller.preview_size
        ))

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        if del_item:
            self.frame.set_cursor(CURSOR_ARROWWAIT)
            self.frame.imageTreeCtrl.Delete(item_id)
            if self.parent is not None:
                del self.parent.children[item_id]
        del self.frame.tree_manager.file_dict[self.loaded_image_path]
        self.cache.del_cache()
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

        loaded_image, error = open_image(self.loaded_image_path)
        if error is not None:
            if dialog:
                self.frame.dialog.async_warning(f'{self.path_data.file_name}重载失败: {error}')
                self.reload_done()
            self.frame.imageTreeCtrl.SetItemTextColour(self.item_id, LIGHT_RED)
            return 0, 1
        else:
            self.frame.imageTreeCtrl.SetItemTextColour(self.item_id, BLACK)
        self.cache.loaded_image = loaded_image
        self.cache.refresh_cache()
        if self.settings_source == 2:
            self.set_settings_source(0)
        self.load_encryption_attributes_from_file()
        if dialog:
            self.frame.dialog.async_info(f'{self.path_data.file_name}重载成功')
            self.reload_done()
        if refresh_preview:
            if self.encrypted_image:
                CallAfter(self._refresh_encrypted_image)
            else:
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
