"""
Author       : noeru_desu
Date         : 2021-11-06 19:08:35
LastEditors  : noeru_desu
LastEditTime : 2022-08-06 12:17:29
Description  : 节点树控制
"""
from contextlib import suppress
from os.path import join, sep, split
from typing import TYPE_CHECKING, Generator, Optional, Union, overload

from wx import ART_FOLDER, ART_NORMAL_FILE, ArtProvider, ImageList, Size

from image_encryptor.frame.file_item import FolderItem
from image_encryptor.utils.thread import SingleThreadExecutor

if TYPE_CHECKING:
    from wx import TreeCtrl, TreeItemId
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import ImageItem, Item


class TreeManager(object):
    'wx.TreeCtrl类的控制器'
    __slots__ = ('frame', 'tree_ctrl', 'reloading_thread', 'root', 'root_dir_dict', 'dir_dict', 'file_dict', 'stop_reloading_signal')

    def __init__(self, frame: 'MainFrame', tree_ctrl: 'TreeCtrl', root_name: str, root_icon_index=0):
        self.frame = frame
        self.tree_ctrl = tree_ctrl
        self.reloading_thread = SingleThreadExecutor('reloading-thread')
        self.stop_reloading_signal = False
        tree_image_list = ImageList(16, 16, True, 2)
        tree_image_list.Add(ArtProvider.GetBitmap(ART_FOLDER, size=Size(16, 16)))
        tree_image_list.Add(ArtProvider.GetBitmap(ART_NORMAL_FILE, size=Size(16, 16)))
        self.tree_ctrl.AssignImageList(tree_image_list)
        self.root = self.tree_ctrl.AddRoot(root_name, image=root_icon_index)
        self.root_dir_dict: dict[str, 'TreeItemId'] = {}
        self.dir_dict: dict[str, 'TreeItemId'] = {}
        self.file_dict: dict[str, 'TreeItemId'] = {}

    @staticmethod
    def _recursively_merge_list(list: list):
        li = ''
        for i in list:
            li = join(li, i)
            yield li, i

    def add_dir(self, root_path: str, relative_path: str = None) -> 'TreeItemId':
        """添加文件夹至文件树，如果重复则不进行操作(重复时`root_dir_dict`优先级高于`dir_dict`)

        Args:
            root_path (str): 文件树中的根文件夹(不存在时自动添加)
            relative_path (str, optional): 根文件夹中的相对路径(相对路径中的文件夹不存在时自动添加, 可为多级文件夹). 默认为None.

        Returns:
            TreeItemId: 添加的到文件树的项目的TreeItemId(如果有多个则返回最后一个)
        """
        if root_path in self.root_dir_dict:
            root = self.root_dir_dict[root_path]
        elif root_path in self.dir_dict:
            root = self.dir_dict[root_path]
        else:
            self.frame.logger.info(f'根文件夹添加至文件树: {root_path}')
            self.root_dir_dict[root_path] = root = self.tree_ctrl.AppendItem(self.root, root_path, 0, data=FolderItem(root_path))
        if not relative_path:
            return root
        dir_list = relative_path.split(sep)
        for r_path, name in self._recursively_merge_list(dir_list):
            path = join(root_path, r_path)
            if path in self.root_dir_dict:
                root = self.root_dir_dict[path]
            elif path in self.dir_dict:
                root = self.dir_dict[path]
            else:
                self.frame.logger.info(f'文件夹添加至文件树: {r_path}')
                parent_data: 'FolderItem' = self.tree_ctrl.GetItemData(root)
                parent_id = root
                data = FolderItem(path)
                self.dir_dict[path] = root = self.tree_ctrl.AppendItem(root, name, 0, data=data)
                parent_data.children[root] = data
                data.parent = parent_data
                data.parent_id = parent_id
        return root

    @overload
    def add_file(self, data: 'ImageItem', file_path: str, *, add_to_root=True) -> 'TreeItemId':
        """添加文件项目到文件树，如果重复则不进行操作(所属文件夹重复时`root_dir_dict`优先级高于`dir_dict`)\n
        如果处理期间涉及的目录不存在于文件树中，将自动创建\n
        `relative_path` 和 `file` 参数需要同时给出或不给出，\n
        不给出时，将进行如下操作：

        `
        relative_path = ''
        `\n
        `
        root_path, file = os.path.split(file_path)
        `

        Args:
            data (ImageItem): 需要绑定到项目的数据实例(一般为ImageItem实例)
            file_path (str): 要添加的文件的绝对路径
            root_path (str): 要添加到的根文件夹
            relative_path (str, optional): 要添加到的根文件夹中的相对路径. 默认分情况处理，具体见上文
            file (str, optional): 文件名称. 默认分情况处理，具体见上文
            add_to_root (bool, optional): 是否无视`root_path`与`relative_path`参数, 直接添加到根目录中. 默认为True

        Returns:
            TreeItemId: 添加的到文件树的项目的TreeItemId
        """

    @overload
    def add_file(self, data: 'ImageItem', root_path: str, relative_path: str, file: str, add_to_root=True) -> 'TreeItemId': ...

    def add_file(self, data: 'ImageItem', root_path: str, relative_path: str = ..., file: str = ..., add_to_root=True) -> 'TreeItemId':
        if relative_path is ... and file is ...:
            absolute_path = root_path
            relative_path = ''
            root_path, file = split(root_path)
        else:
            assert relative_path is not ... and file is not ..., '"relative_path" and "file" arguments need to be given or not given at the same time.'
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
        data.item_id = item_id
        if not add_to_root:
            parent_data: 'FolderItem' = self.tree_ctrl.GetItemData(root)
            parent_data.children[item_id] = data
            data.parent = parent_data
            data.parent_id = root
        # self.frame.logger.info(f'文件添加至文件树: {file}')
        return item_id

    def del_item(self, item_id: 'TreeItemId', __item: 'Item' = None):
        """从文件树删除指定的文件夹/文件

        Args:
            item_id (TreeItemId): 项目的TreeItemId, 如果为无效ID则不进行操作
            __item (Item): 内部迭代删除空父级时使用, 正常使用无需传入
        """
        if item_id.IsOk():
            item = self.tree_ctrl.GetItemData(item_id) if __item is None else __item
            item.del_item(item_id)
            if item.parent is not None and (not item.parent.children):
                self.del_item(item.parent_id, item.parent)

    def reload_item(self, item_id: 'TreeItemId'):
        """重载指定的文件夹/文件

        Args:
            item_id (TreeItemId): 项目的TreeItemId, 如果为无效ID则不进行操作
        """
        if item_id.IsOk():
            self.reloading_thread.add_task(self.tree_ctrl.GetItemData(item_id).reload_item)

    @property
    def selected_item_data(self) -> Optional[Union['ImageItem', 'FolderItem']]:
        """等价于`<TreeCtrl>.GetItemData(<TreeCtrl>.Selection)`

        Returns:
            当前选择的项目的数据实例(一般为ImageItem或FolderItem)
        """
        with suppress(RuntimeError):
            return self.tree_ctrl.GetItemData(self.tree_ctrl.Selection)

    @property
    def all_item_data(self) -> Generator[Union['ImageItem', 'FolderItem'], None, None]:
        """生成器

        Yields:
            文件树中的每一个数据实例: 一般为ImageItem或FolderItem
        """
        with suppress(RuntimeError):
            for i in self.root_dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
            for i in self.dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
            for i in self.file_dict.values():
                yield self.tree_ctrl.GetItemData(i)

    @property
    def all_image_item_data(self) -> Generator['ImageItem', None, None]:
        """生成器

        Yields:
            文件树中的每一个文件项目的数据实例: 一般为ImageItem
        """
        with suppress(RuntimeError):
            for i in self.file_dict.values():
                yield self.tree_ctrl.GetItemData(i)

    @property
    def all_folder_item_data(self) -> Generator['FolderItem', None, None]:
        """生成器

        Yields:
            文件树中的每一个文件夹项目的数据实例: 一般为FolderItem
        """
        with suppress(RuntimeError):
            for i in self.root_dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
            for i in self.dir_dict.values():
                yield self.tree_ctrl.GetItemData(i)
