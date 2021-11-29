'''
Author       : noeru_desu
Date         : 2021-11-06 19:08:35
LastEditors  : noeru_desu
LastEditTime : 2021-11-29 21:17:35
Description  : 节点树控制
'''
from os.path import isdir, isfile, join, sep, split
from typing import TYPE_CHECKING, Generator

from wx import ART_FOLDER, ART_NORMAL_FILE, ArtProvider, ImageList, Size

if TYPE_CHECKING:
    from image_encryptor.gui.frame.main_frame import MainFrame
    from PIL.Image import Image
    from wx import TreeCtrl


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
        self.frame.logger.info('TreeManager实例化完成')

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
            self.frame.logger.info(f'根文件夹添加至文件树：{root_path}')
            self.root_dir_dict[root_path] = root = self.tree_ctrl.AppendItem(self.root, root_path, 0)
        else:
            root = self.root_dir_dict[root_path]
        if relative_path == '':
            return
        for r_path, name in self._recursively_merge_list(dir_list):
            path = join(root_path, r_path)
            if path not in self.dir_dict:
                self.frame.logger.info(f'文件夹添加至文件树：{r_path}')
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
        self.frame.logger.info(f'文件添加至文件树：{file}')

    @property
    def _all_item_data(self) -> Generator['ImageItem', None, None]:
        for i in self.file_dict.values():
            yield self.tree_ctrl.GetItemData(i)


class ImageItem(object):
    """每个载入的图片的存储实例"""

    def __init__(self, frame: 'MainFrame', loaded_image: 'Image', path_data: tuple[str, str, str], settings: dict):
        self.frame = frame
        self.loaded_image = loaded_image
        self.path_data = path_data
        self.loaded_image_path = join(*path_data)
        self.settings = settings
        self.initial_preview = None
        self.processed_preview = None
        self.preview_size = None
        self.preview_summary = None
        self.manual_switch_mode = False
        self.encrypted_image = None
        self.encryption_data = None
        self.loading_image_data_error = None
        self.xor_checkbox = {'r': frame.xorR, 'g': frame.xorG, 'b': frame.xorB, 'a': frame.xorA}

    def backtrack_interface(self):
        if self.encrypted_image and (not self.manual_switch_mode or self.settings['mode'] == 1):
            self.settings['mode'] = 1
            self.frame.check_encryption_parameters()
        else:
            if self.settings['mode'] == 1:
                self.frame.mode.Select(0)
            else:
                self.frame.mode.Select(self.settings['mode'])
            self.frame.row.SetValue(self.settings['row'])
            self.frame.col.SetValue(self.settings['col'])
            self.frame.shuffle.SetValue(self.settings['shuffle'])
            self.frame.rgbMapping.SetValue(self.settings['rgb_mapping'])
            self.frame.flip.SetValue(self.settings['flip'])
            self.frame.password.SetValue(self.settings['password'])
            self.frame.noiseXor.SetValue(self.settings['noise_xor'])
            self.frame.noiseFactor.SetValue(self.settings['noise_factor'])
            self.frame.update_noise_factor_num()
            self.frame.processingSettingsPanel1.Enable()
            self.frame.password.Enable()
            for i in 'rgba':
                self.xor_checkbox[i].SetValue(i in self.settings['xor_channels'])

        self.frame.imageInfo.SetLabelText(f'图片分辨率：{self.loaded_image.size[0]}x{self.loaded_image.size[1]}')
        self.frame.selectSavePath.SetPath(self.settings['saving_path'])
        self.frame.selectFormat.Select(self.settings['saving_format'])
        self.frame.saveQuality.SetValue(self.settings['quality'])
        self.frame.update_quality_num()
        self.frame.subsamplingLevel.SetValue(self.settings['subsampling'])
        self.frame.update_subsampling_num()

    def backtrack_decryption_interface(self):
        self.frame.mode.Select(1)
        self.frame.processingSettingsPanel1.Disable()
        self.frame.row.SetValue(self.encryption_data['row'])
        self.frame.col.SetValue(self.encryption_data['col'])
        self.frame.shuffle.SetValue(self.encryption_data['shuffle'])
        self.frame.rgbMapping.SetValue(self.encryption_data['rgb_mapping'])
        self.frame.flip.SetValue(self.encryption_data['flip'])
        self.frame.noiseXor.SetValue(self.encryption_data['noise_xor'])
        self.frame.noiseFactor.SetValue(self.encryption_data['noise_factor'])
        self.frame.update_noise_factor_num()
        for i in 'rgba':
            self.xor_checkbox[i].SetValue(i in self.encryption_data['xor_channels'])
        if self.encryption_data['password'] is None:
            self.encryption_data['password'] = self.frame.password_dict.get(self.encryption_data['password_base64'], None)
        if self.encryption_data['password'] is None:
            self.frame.password.SetValue('')
        else:
            self.frame.password.Disable()
            self.frame.password.SetValue(str(self.encryption_data['password']))
