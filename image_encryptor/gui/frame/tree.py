'''
Author       : noeru_desu
Date         : 2021-11-06 19:08:35
LastEditors  : noeru_desu
LastEditTime : 2021-11-10 20:29:22
Description  : 节点树控制
'''
from os.path import sep, isfile, isdir, split, join
from typing import TYPE_CHECKING

from wx import ImageList, ART_FOLDER, ART_NORMAL_FILE, ArtProvider, Size

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import TreeCtrl
    from image_encryptor.gui.frame.main_frame import MainFrame


class TreeManager(object):
    'wx.TreeCtrl类的控制器'
    def __init__(self, frame: 'MainFrame', tree_ctrl: 'TreeCtrl', root_name: str, root_icon_index=0):
        self.frame = frame
        self.tree_ctrl = tree_ctrl
        tree_image_list = ImageList(16, 16, True, 2)
        tree_image_list.Add(ArtProvider.GetBitmap(ART_FOLDER, size=Size(16, 16)))
        tree_image_list.Add(ArtProvider.GetBitmap(ART_NORMAL_FILE, size=Size(16, 16)))
        self.tree_ctrl.AssignImageList(tree_image_list)
        self.root = self.tree_ctrl.AddRoot(root_name, image=root_icon_index)
        self.root_dir_dict = {}
        self.dir_dict = {}
        self.file_dict = {}
        self.frame.program.logger.info('TreeManager初始化完成')

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
            self.frame.program.logger.info(f'根文件夹添加至文件树：{root_path}')
            self.root_dir_dict[root_path] = root = self.tree_ctrl.AppendItem(self.root, root_path, 0)
        else:
            root = self.root_dir_dict[root_path]
        if relative_path == '':
            return
        for r_path, name in self._recursively_merge_list(dir_list):
            path = join(root_path, r_path)
            if path not in self.dir_dict:
                self.frame.program.logger.info(f'文件夹添加至文件树：{r_path}')
                self.dir_dict[path] = root = self.tree_ctrl.AppendItem(root, name, 0)

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
            if join(root_path, relative_path) not in self.dir_dict:
                self.add_dir(root_path, relative_path)
            absolute_dir_path = join(root_path, relative_path).strip(sep)
            root = self.root_dir_dict[absolute_dir_path] if absolute_dir_path in self.root_dir_dict else self.dir_dict[absolute_dir_path]
        self.file_dict[absolute_path] = self.tree_ctrl.AppendItem(root, file, 1, data=data)
        self.frame.program.logger.info(f'文件添加至文件树：{file}')

    @property
    def _all_item_data(self):
        for i in self.file_dict.values():
            yield self.tree_ctrl.GetItemData(i)


class ImageItem(object):
    def __init__(self, loaded_image: 'Image', loaded_image_path: str, settings: dict, data: tuple = (None, None, None, None, None, None)):
        self.loaded_image = loaded_image
        self.loaded_image_path = loaded_image_path
        self.settings = settings
        self.initial_preview, self.processed_preview, self.preview_size, self.preview_summary, self.encrypted_image, self.encryption_data = data

    def update(self, initial_preview: 'Image', processed_preview: 'Image', preview_size: tuple, preview_summary: bytes, encrypted_image: bool, encryption_data: dict, settings: dict):
        self.initial_preview = initial_preview
        self.processed_preview = processed_preview
        self.preview_size = preview_size
        self.preview_summary = preview_summary
        self.encrypted_image = encrypted_image
        self.encryption_data = encryption_data
        self.settings = settings

    def backtrack_interface(self, frame: 'MainFrame'):
        frame.loaded_image = self.loaded_image
        frame.initial_preview = self.initial_preview
        frame.processed_preview = self.processed_preview
        frame.loaded_image_path = self.loaded_image_path
        frame.encrypted_image = self.encrypted_image
        frame.encryption_data = self.encryption_data
        frame.preview_size = self.preview_size
        frame.preview_summary = self.preview_summary

        if self.settings['mode'] != 1:
            frame.mode.Select(self.settings['mode'])
            frame.row.SetValue(self.settings['row'])
            frame.col.SetValue(self.settings['col'])
            frame.upset.SetValue(self.settings['upset'])
            frame.rgbMapping.SetValue(self.settings['rgb_mapping'])
            frame.flip.SetValue(self.settings['flip'])
            frame.xorRgb.Select(self.settings['xor'])
            frame.processingSettingsPanel1.Enable(True)
            frame.xorRgb.Enable(True)
        else:
            frame.check_encryption_parameters()

        frame.imageInfo.SetLabelText(f'大小：{self.loaded_image.size[0]}x{self.loaded_image.size[1]}')
        frame.selectSavePath.SetPath(self.settings['save_path'])
        frame.selectFormat.Select(self.settings['save_format'])
