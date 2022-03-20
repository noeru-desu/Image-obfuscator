"""
Author       : noeru_desu
Date         : 2022-02-19 19:46:01
LastEditors  : noeru_desu
LastEditTime : 2022-03-20 12:51:56
Description  : 图像项目
"""
from abc import ABC
from gc import collect
from os.path import isfile, join
from typing import TYPE_CHECKING, NamedTuple, Optional, Union

from wx import BLACK, CallAfter

from image_encryptor.constants import (DECRYPTION_MODE, ENCRYPTION_MODE,
                                       LIGHT_RED)
from image_encryptor.frame.controls import EncryptionParameters
from image_encryptor.modules.version_adapter import load_encryption_attributes
from image_encryptor.utils.misc_util import open_image

if TYPE_CHECKING:
    from image_encryptor.frame.controls import Settings
    from image_encryptor.frame.events import MainFrame
    from PIL.Image import Image
    from wx import Bitmap, TreeItemId


class Item(ABC):
    __slots__ = ()

    def del_item(self, item_id: 'TreeItemId', del_item=True):
        ...

    def reload_item(self, dialog=True):
        ...

    def reload_done(self):
        if self.frame.tree_manager.reloading_thread.exit_signal:
            self.frame.stop_reloading(False)
        self.frame.stop_reloading_func.init()


class ImageItemCache(object):
    """图像项目缓存控制器"""
    __slots__ = (
        '_item', 'initial_preview', 'processed_previews', 'preview_size', '_encryption_data', '_loaded_image',
        'loading_encryption_attributes_error'
    )

    def __init__(self, item: 'ImageItem', loaded_image=None):
        self._item = item
        self.initial_preview: Image = None
        self.processed_previews: dict[bytes, Bitmap] = {}
        self.preview_size: tuple[int, int] = None
        self.loading_encryption_attributes_error = None
        self._encryption_data = None
        self._loaded_image = loaded_image

    @property
    def loaded_image(self) -> 'Image':
        if self._item.selected and self._loaded_image is None:
            reload_encryption_data = self._item.loading_image_data_error is not None
            self._loaded_image, self._item.loading_image_data_error = open_image(self._item.loaded_image_path)
            if self._item.loading_image_data_error is not None:
                self._item.frame.dialog.async_error(self._item.loading_image_data_error, '重新载入图片时出现错误')
                self._loaded_image = BLACK_IMAGE
                self._item.encrypted_image = False
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, LIGHT_RED)
            else:
                if reload_encryption_data:
                    self._item.load_encryption_parameters()
                self._item.frame.imageTreeCtrl.SetItemTextColour(self._item.item_id, BLACK)
        if not self._item.frame.startup_parameters.low_memory or self._item.selected:
            return self._loaded_image

    def get_processed_preview_cache(self, cache_hash) -> Optional['Bitmap']:
        return self.processed_previews.get(cache_hash)

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

    @property
    def processed_preview(self) -> 'Bitmap':
        # 使用get_processed_preview_cache代替
        try:
            raise
        except Exception:
            print_exc()
        return list(self.processed_previews.values())[-1]

    def add_processed_preview(self, hash, bitmap):
        if hash in self.processed_previews:
            return
        keys = self.processed_previews.keys()
        if len(keys) >= self._item.frame.startup_parameters.maximum_redundant_cache_length:
            del self.processed_previews[list(keys)[0]]
        self.processed_previews[hash] = bitmap

    def clear_redundant_cache(self):
        for i in list(self.processed_previews.keys())[:-1]:
            del self.processed_previews[i]

    def clear_cache(self):
        self.initial_preview = None
        self.processed_previews.clear()
        self.preview_size = None
        self._encryption_data = None

    def del_cache(self):
        del self.processed_previews
        del self.initial_preview
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
            self.cache.clear_redundant_cache()

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
