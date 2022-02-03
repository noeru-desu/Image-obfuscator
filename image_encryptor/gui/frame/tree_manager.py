'''
Author       : noeru_desu
Date         : 2021-11-06 19:08:35
LastEditors  : noeru_desu
LastEditTime : 2022-02-03 14:14:27
Description  : 节点树控制
'''
from abc import ABC
from os.path import isdir, isfile, join, sep, split
from typing import TYPE_CHECKING, Generator

from wx import ART_FOLDER, ART_NORMAL_FILE, ArtProvider, ImageList, Size
from image_encryptor.constants import DECRYPTION_MODE, ENCRYPTION_MODE

from image_encryptor.common.utils.utils import open_image
from image_encryptor.gui.modules.password_verifier import get_image_data
from image_encryptor.gui.frame.controls import EncryptionParameters
from image_encryptor.gui.utils.thread import ThreadManager

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import TreeCtrl, TreeItemId
    from image_encryptor.gui.frame.controls import Settings
    from image_encryptor.gui.frame.events import MainFrame


class TreeManager(object):
    'wx.TreeCtrl类的控制器'

    def __init__(self, frame: 'MainFrame', tree_ctrl: 'TreeCtrl', root_name: str, root_icon_index=0):
        self.frame = frame
        self.tree_ctrl = tree_ctrl
        self.reloading_thread = ThreadManager('reloading-thread')
        tree_image_list = ImageList(16, 16, True, 2)
        tree_image_list.Add(ArtProvider.GetBitmap(ART_FOLDER, size=Size(16, 16)))
        tree_image_list.Add(ArtProvider.GetBitmap(ART_NORMAL_FILE, size=Size(16, 16)))
        self.tree_ctrl.AssignImageList(tree_image_list)
        self.root = self.tree_ctrl.AddRoot(root_name, image=root_icon_index)
        self.root_dir_dict = {}
        self.dir_dict = {}
        self.file_dict = {}

    @staticmethod
    def _recursively_merge_list(list: list):
        li = ''
        for i in list:
            li = join(li, i)
            yield li, i

    def add_dir(self, root_path: str, relative_path: str):
        assert isdir(join(root_path, relative_path)), f'{relative_path} is not a folder.'
        dir_list = relative_path.split(sep)
        if root_path not in self.root_dir_dict:
            self.frame.logger.info(f'根文件夹添加至文件树: {root_path}')
            self.root_dir_dict[root_path] = root = self.tree_ctrl.AppendItem(self.root, root_path, 0, data=FolderItem(self.frame, root_path, True))
        else:
            root = self.root_dir_dict[root_path]
        if relative_path == '':
            return
        for r_path, name in self._recursively_merge_list(dir_list):
            path = join(root_path, r_path)
            if path not in self.dir_dict:
                self.frame.logger.info(f'文件夹添加至文件树: {r_path}')
                parent_data = self.tree_ctrl.GetItemData(root)
                data = FolderItem(self.frame, path)
                self.dir_dict[path] = root = self.tree_ctrl.AppendItem(root, name, 0, data=data)
                parent_data.children[root] = data
                data.parent = parent_data

    def add_file(self, root_path: str, relative_path: str = None, file: str = None, data: dict = None, add_to_root=True):
        if relative_path is None and file is None:
            relative_path = ''
            root_path, file = split(root_path)
        absolute_path = join(root_path, relative_path, file)
        assert isfile(absolute_path), f'{file} is not a file.'
        if absolute_path in self.file_dict:
            return
        root = self.root
        if not add_to_root:
            parent_folder_path = join(root_path, relative_path)
            if parent_folder_path not in self.dir_dict:
                self.add_dir(root_path, relative_path)
            absolute_dir_path = parent_folder_path.strip(sep)
            root = self.root_dir_dict[absolute_dir_path] if absolute_dir_path in self.root_dir_dict else self.dir_dict[absolute_dir_path]
        self.file_dict[absolute_path] = item_id = self.tree_ctrl.AppendItem(root, file, 1, data=data)
        if not add_to_root:
            parent_data = self.tree_ctrl.GetItemData(root)
            parent_data.children[item_id] = data
            data.parent = parent_data
        # self.frame.logger.info(f'文件添加至文件树: {file}')

    def del_item(self, item_id: 'TreeItemId'):
        if item_id.IsOk():
            self.tree_ctrl.GetItemData(item_id).del_item(item_id)

    def reload_item(self, item_id: 'TreeItemId'):
        if item_id.IsOk():
            self.reloading_thread.start_new(self.tree_ctrl.GetItemData(item_id).reload_item)

    @property
    def _all_item_data(self) -> Generator['ImageItem', None, None]:
        for i in self.file_dict.values():
            yield self.tree_ctrl.GetItemData(i)


class Item(ABC):
    def del_item(self, item_id: 'TreeItemId', del_item=True):
        ...

    def reload_item(self, dialog=True):
        ...

    def reload_done(self):
        if self.frame.tree_manager.reloading_thread.exit_signal:
            self.frame.stop_reloading(False)
        self.frame.stop_reloading_func.init()


class ImageItem(Item):
    """每个载入的图片的存储实例"""

    def __init__(self, frame: 'MainFrame', loaded_image: 'Image', path_data: tuple[str, str, str], settings: 'Settings'):
        self.frame = frame
        self.loaded_image = loaded_image
        self.path_data = path_data
        self.loaded_image_path = join(*path_data)
        self.settings = settings
        self.parent = None
        self._init_cache()

    def _init_cache(self):
        self.initial_preview = None
        self.processed_preview = None
        self.preview_size = None
        self.encryption_settings_md5 = None
        self.encrypted_image = None
        self.encryption_data: 'EncryptionParameters' = None
        self.loading_image_data_error = None

    def check_encryption_parameters(self):
        if self.encrypted_image is None:
            self.load_encryption_parameters()
        if self.encrypted_image:
            self.encryption_data.backtrack_interface()

    def load_encryption_parameters(self):
        encryption_data, self.loading_image_data_error = get_image_data(self.loaded_image_path, skip_password=True)
        if self.loading_image_data_error is None:
            self.encrypted_image = True
            self.settings.proc_mode = DECRYPTION_MODE
            self.encryption_data = EncryptionParameters(self.frame.controls, encryption_data)
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

    def reload_item(self, dialog=True):
        if self.frame.tree_manager.reloading_thread.exit_signal:
            return 0, 0
        loaded_image, error = open_image(self.loaded_image_path)
        if error is not None:
            if dialog:
                self.frame.dialog.async_warning(f'图像重载失败: {error}')
                self.reload_done()
            return 0, 1
        self.loaded_image = loaded_image
        self._init_cache()
        self.load_encryption_parameters()
        if dialog:
            self.frame.dialog.async_info('图像重载成功')
            self.reload_done()
            if self.encrypted_image:
                self.encryption_data.backtrack_interface()
        return 1, 0


class FolderItem(Item):
    def __init__(self, frame: 'MainFrame', path, root=False):
        self.frame = frame
        self.path = path
        self.root = root
        self.children = {}
        self.parent = None

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

    def reload_item(self, dialog=True):
        if self.frame.tree_manager.reloading_thread.exit_signal:
            return 0, 0
        fail_num = 0
        success_num = 0
        for data in self.children.values():
            add_success_num, add_fail_num = data.reload_item(False)
            success_num += add_success_num
            fail_num += add_fail_num
        if dialog:
            self.frame.dialog.async_info(f'重载成功: {success_num}个, 失败: {fail_num}个')
            self.reload_done()
        return success_num, fail_num
