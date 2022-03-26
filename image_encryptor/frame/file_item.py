"""
Author       : noeru_desu
Date         : 2022-02-19 19:46:01
LastEditors  : noeru_desu
LastEditTime : 2022-03-26 19:46:28
Description  : 图像项目
"""
from abc import ABC
from collections import OrderedDict
from gc import collect
from os.path import isfile, join
from typing import TYPE_CHECKING, Hashable, NamedTuple, Optional, Union

from wx import BLACK, CallAfter

from image_encryptor.constants import (DECRYPTION_MODE, ENCRYPTION_MODE,
                                       LIGHT_RED, PIL_RESAMPLING_FILTERS)
from image_encryptor.frame.controls import EncryptionParameters
from image_encryptor.modules.argparse import Parameters
from image_encryptor.modules.version_adapter import load_encryption_attributes
from image_encryptor.utils.misc_util import open_image, scale

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Bitmap, TreeItemId
    from image_encryptor.frame.controls import Settings
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.utils.image import WrappedImage


class Item(ABC):
    __slots__ = ()

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        raise NotImplementedError()

    def reload_item(self, dialog=True):
        raise NotImplementedError()

    def reload_done(self):
        if self.frame.tree_manager.reloading_thread.exit_signal:
            self.frame.stop_reloading(False)
        self.frame.stop_reloading_func.init()


class PreviewCache(object):
    __slots__ = ('scalable_cache', 'normal_cache', 'startup_parameters')

    def __init__(self, startup_parameters: Parameters) -> None:
        self.startup_parameters = startup_parameters
        self.normal_cache: OrderedDict[int, Bitmap] = OrderedDict()
        self.scalable_cache: OrderedDict[int, WrappedImage] = OrderedDict()

    def clear_redundant_cache(self):
        for i in list(self.normal_cache)[:-1]:
            del self.normal_cache[i]
        for i in list(self.scalable_cache)[:-1]:
            del self.scalable_cache[i]

    def add_cache(self, cache_hash: Hashable, image: Union['WrappedImage', 'Bitmap'] = None):
        if image.scalable:
            self.add_scalable_cache(cache_hash, image)
        else:
            self.add_normal_cache(cache_hash, image)

    def add_normal_cache(self, cache_hash: Hashable, bitmap: 'Bitmap' = None):
        if cache_hash in self.normal_cache:
            self.normal_cache.move_to_end(cache_hash)
            if bitmap is None:
                return
        assert bitmap is not None, 'Bitmap cannot be NoneType when the cache_hash does not exist in the cache.'
        if len(self.normal_cache) >= self.startup_parameters.maximum_redundant_cache_length:
            self.normal_cache.popitem(False)
        self.normal_cache[cache_hash] = bitmap

    def add_scalable_cache(self, cache_hash: Hashable, image: 'WrappedImage' = None):
        if cache_hash in self.scalable_cache:
            self.scalable_cache.move_to_end(cache_hash)
            if image is None:
                return
        assert image is not None, 'Image cannot be NoneType when the cache_hash does not exist in the cache.'
        if len(self.scalable_cache) >= self.startup_parameters.maximum_redundant_cache_length:
            self.scalable_cache.popitem(False)
        self.scalable_cache[cache_hash] = image

    def get_cache(self, cache_hash) -> Optional[Union['WrappedImage', 'Bitmap']]:
        if cache_hash in self.normal_cache:
            self.add_normal_cache(cache_hash)
            return self.normal_cache[cache_hash]
        if cache_hash in self.scalable_cache:
            self.add_scalable_cache(cache_hash)
            return self.scalable_cache[cache_hash]

    def get_normal_cache(self, cache_hash) -> Optional['Bitmap']:
        if cache_hash in self.normal_cache:
            self.add_normal_cache(cache_hash)
            return self.normal_cache[cache_hash]

    def get_scalable_cache(self, cache_hash) -> Optional['WrappedImage']:
        if cache_hash in self.scalable_cache:
            self.add_scalable_cache(cache_hash)
            return self.scalable_cache[cache_hash]

    def clear(self):
        self.scalable_cache.clear()
        self.normal_cache.clear()

    def delete(self):
        del self.scalable_cache
        del self.normal_cache
        del self


class ImageItemCache(object):
    """图像项目缓存控制器"""
    __slots__ = ('_item', 'initial_preview', 'previews', 'preview_size', '_encryption_data', '_loaded_image', 'loading_encryption_attributes_error')

    def __init__(self, item: 'ImageItem', loaded_image=None):
        self._item = item
        self.initial_preview: Image = None
        self.preview_size: tuple[int, int] = None
        self.previews = PreviewCache(item.frame.startup_parameters)
        self.loading_encryption_attributes_error = None
        self._encryption_data = None
        self._loaded_image = loaded_image

    @property
    def loaded_image(self) -> 'Image':
        assert self._item.selected, 'Image is not selected.'    # 低内存占用模式下可能出现内存泄露
        if self._loaded_image is None:
            reload_encryption_data = self._item.loading_image_data_error is not None
            self._loaded_image, self._item.loading_image_data_error = open_image(self._item.loaded_image_path)
            if self._item.loading_image_data_error is not None:
                self._item.frame.dialog.async_error(self._item.loading_image_data_error, '重新载入图像时出现错误')
                self._item.encrypted_image = False
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, LIGHT_RED)
            else:
                if reload_encryption_data:
                    self._item.load_encryption_parameters()
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, BLACK)
        # if not self._item.frame.startup_parameters.low_memory or self._item.selected:
        return self._loaded_image

    @loaded_image.setter
    def loaded_image(self, v):
        self._loaded_image = v

    @property
    def encryption_data(self) -> Optional['EncryptionParameters']:
        if self._encryption_data is None:
            self._item.load_encryption_parameters()
        return self._encryption_data

    @encryption_data.setter
    def encryption_data(self, v):
        self._encryption_data = v

    def clear_cache(self):
        self.initial_preview = None
        self.previews.clear()
        self.preview_size = None
        self._encryption_data = None

    def del_cache(self):
        del self.initial_preview
        self.previews.delete()
        del self.preview_size
        del self._encryption_data
        del self._loaded_image


class PathData(NamedTuple):
    root_path: str
    relative_path: str
    file_name: str

    @property
    def full_path(self) -> str:
        return join(*self)


class ImageItem(Item):
    """每个载入的图像的存储实例"""
    __slots__ = (
        'frame', 'cache', 'path_data', 'loaded_image_path', 'settings', 'parent', 'item_id',
        'selected', 'no_file', 'keep_cache_loaded_image', 'encrypted_image', 'loading_image_data_error'
    )

    def __init__(self, frame: 'MainFrame', loaded_image: 'Image', path_data: 'PathData', settings: 'Settings', no_file=False, keep_cache_loaded_image=False):
        self.frame = frame
        self.cache = ImageItemCache(self, loaded_image)

        self.path_data = path_data
        self.loaded_image_path = path_data.file_name if no_file else path_data.full_path
        self.settings = settings

        self.item_id: TreeItemId = ...
        self.parent: Optional[FolderItem] = None
        self.selected = False
        self.no_file = no_file
        self.keep_cache_loaded_image = keep_cache_loaded_image

        self.encrypted_image: bool = None
        if self.no_file:
            self.encrypted_image = False
            self.loading_image_data_error = '来自剪贴板的文件不支持解密操作'
        else:
            self.loading_image_data_error = None

    def unselect(self):
        self.selected = False
        if self.frame.startup_parameters.low_memory:
            if not self.keep_cache_loaded_image:
                self.cache._loaded_image = None
            self.cache.clear_cache()
        else:
            self.cache.previews.clear_redundant_cache()

    def display_initial_preview(self, cache=True) -> bool:
        """命中缓存返回False, 未命中则生成并返回True"""
        size = self.frame.controls.preview_size
        if cache and self.cache.initial_preview is not None and size == self.cache.preview_size:
            self.frame.controls.imported_image = self.cache.initial_preview
            return False
        image = self.cache.loaded_image.resize(scale(*self.cache.loaded_image.size, *size), PIL_RESAMPLING_FILTERS[self.frame.controls.resampling_filter_id])
        self.frame.controls.imported_image = image
        self.cache.preview_size = size
        self.cache.initial_preview = image
        return True

    def display_processed_preview(self, cache=True, resize=True):
        """命中缓存返回False, 未命中则生成并返回True"""
        if cache:
            cache_hash = self.frame.settings.encryption_settings_hash
            if cache_hash in self.cache.previews.scalable_cache:
                self.frame.controls.previewed_bitmap = (
                    self.cache.previews.scalable_cache[cache_hash].gen_wxBitmap(
                        self.frame.controls.preview_size,
                        self.frame.controls.resampling_filter_id,
                    )
                    if resize
                    else self.cache.previews.scalable_cache[cache_hash].wxBitmap
                )
                return False
            cache_hash = self.frame.settings.encryption_settings_hash_with_size
            if cache_hash in self.cache.previews.normal_cache:
                self.frame.controls.previewed_bitmap = self.cache.previews.get_normal_cache(cache_hash)
                return False
        self.frame.preview_generator.generate_preview()
        return True

    def check_encryption_parameters(self):
        if self.encrypted_image is None:
            self.load_encryption_parameters()
        if self.encrypted_image:
            self.cache.encryption_data.backtrack_interface()

    def load_encryption_parameters(self):
        if self.no_file or not isfile(self.loaded_image_path):
            return
        encryption_data, self.cache.loading_encryption_attributes_error = load_encryption_attributes(self.loaded_image_path)
        if self.cache.loading_encryption_attributes_error is None:
            self.encrypted_image = True
            self.settings.proc_mode = DECRYPTION_MODE
            self.cache.encryption_data = EncryptionParameters(self.frame.controls, encryption_data)
        else:
            default_proc_mode = self.frame.settings.default.proc_mode
            self.encrypted_image = False
            self.settings.proc_mode = default_proc_mode if default_proc_mode != DECRYPTION_MODE else ENCRYPTION_MODE

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        if del_item:
            self.frame.imageTreeCtrl.Delete(item_id)
            if self.parent is not None:
                del self.parent.children[item_id]
        del self.frame.tree_manager.file_dict[self.loaded_image_path]
        self.cache.del_cache()
        del self.cache
        if del_item:
            collect()

    def reload_item(self, dialog=True) -> 'Optional[tuple[int, int]]':
        if self.no_file:
            self.frame.dialog.async_warning('来自剪贴板的文件不支持重载操作')
            self.reload_done()
            return
        if self.frame.tree_manager.reloading_thread.exit_signal:
            return 0, 0
        loaded_image, error = open_image(self.loaded_image_path)
        if error is not None:
            if dialog:
                self.frame.dialog.async_warning(f'图像重载失败: {error}')
                self.reload_done()
            self.frame.imageTreeCtrl.SetItemTextColour(self.item_id, LIGHT_RED)
            return 0, 1
        else:
            self.frame.imageTreeCtrl.SetItemTextColour(self.item_id, BLACK)
        self.cache.loaded_image = loaded_image
        self.cache.clear_cache()
        self.load_encryption_parameters()
        if dialog:
            self.frame.dialog.async_info('图像重载成功')
            self.reload_done()
            if self.encrypted_image:
                CallAfter(self._refresh_encrypted_image)
        return 1, 0

    def _refresh_encrypted_image(self):
        self.cache.encryption_data.backtrack_interface()
        self.frame.force_refresh_preview()


class FolderItem(Item):
    __slots__ = ('frame', 'path', 'root', 'children', 'parent')

    def __init__(self, frame: 'MainFrame', path, root=False):
        self.frame = frame
        self.path = path
        self.root = root
        self.children: dict[TreeItemId, Union[FolderItem, ImageItem]] = {}
        self.parent: Optional[FolderItem] = None

    def del_item(self, item_id: 'TreeItemId', del_item=True):
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
            collect()

    def reload_item(self, dialog=True):
        if self.frame.tree_manager.reloading_thread.exit_signal:
            return 0, 0
        fail_num = 0
        success_num = 0
        for data in self.children.values():
            add_success_num, add_fail_num = data.reload_item(False)
            success_num += add_success_num
            fail_num += add_fail_num
            if self.frame.tree_manager.reloading_thread.exit_signal:
                break
        if dialog:
            self.frame.dialog.async_info(f'重载成功: {success_num}个, 失败: {fail_num}个')
            self.reload_done()
        return success_num, fail_num
