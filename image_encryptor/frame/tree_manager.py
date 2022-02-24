"""
Author       : noeru_desu
Date         : 2021-11-06 19:08:35
LastEditors  : noeru_desu
LastEditTime : 2022-02-24 21:13:24
Description  : 节点树控制
"""
from typing import Union
from os.path import isdir, join, sep, split
from typing import TYPE_CHECKING, Generator, Optional

from wx import ART_FOLDER, ART_NORMAL_FILE, ArtProvider, ImageList, Size

from image_encryptor.frame.file_item import FolderItem
from image_encryptor.utils.thread import ThreadManager

if TYPE_CHECKING:
    from wx import TreeCtrl, TreeItemId
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import ImageItem


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
            return root
        for r_path, name in self._recursively_merge_list(dir_list):
            path = join(root_path, r_path)
            if path not in self.dir_dict:
                self.frame.logger.info(f'文件夹添加至文件树: {r_path}')
                parent_data = self.tree_ctrl.GetItemData(root)
                data = FolderItem(self.frame, path)
                self.dir_dict[path] = root = self.tree_ctrl.AppendItem(root, name, 0, data=data)
                parent_data.children[root] = data
                data.parent = parent_data
        return root

    def add_file(self, root_path: str, relative_path: str = None, file: str = None, data: dict = None, add_to_root=True):
        if relative_path is None and file is None:
            relative_path = ''
            root_path, file = split(root_path)
        absolute_path = join(root_path, relative_path, file)
        if absolute_path in self.file_dict:
            return self.file_dict[absolute_path]
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
        return item_id

    def del_item(self, item_id: 'TreeItemId'):
        if item_id.IsOk():
            self.tree_ctrl.GetItemData(item_id).del_item(item_id)

    def reload_item(self, item_id: 'TreeItemId'):
        if item_id.IsOk():
            self.reloading_thread.start_new(self.tree_ctrl.GetItemData(item_id).reload_item)

    @property
    def selected_item_data(self) -> Optional[Union['ImageItem', 'FolderItem']]:
        try:
            return self.tree_ctrl.GetItemData(self.tree_ctrl.Selection)
        except RuntimeError:
            return

    @property
    def all_item_data(self) -> Generator[Union['ImageItem', 'FolderItem'], None, None]:
        try:
            for i in self.root_dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
            for i in self.dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
            for i in self.file_dict.values():
                yield self.tree_ctrl.GetItemData(i)
        except RuntimeError:
            return

    @property
    def all_image_item_data(self) -> Generator[Union['ImageItem', 'FolderItem'], None, None]:
        try:
            for i in self.file_dict.values():
                yield self.tree_ctrl.GetItemData(i)
        except RuntimeError:
            return

    @property
    def all_folder_item_data(self) -> Generator[Union['ImageItem', 'FolderItem'], None, None]:
        try:
            for i in self.root_dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
            for i in self.dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
        except RuntimeError:
            return
