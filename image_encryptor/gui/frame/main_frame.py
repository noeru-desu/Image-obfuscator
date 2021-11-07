'''
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2021-11-07 16:48:53
Description  : 配置窗口类
'''
from os import getcwd
from os.path import isdir, isfile, join
from traceback import format_exc

import wx
from PIL import Image
from wx.core import EmptyString

import image_encryptor.gui.processor.qq_anti_harmony as qq_anti_harmony
import image_encryptor.gui.processor.single_file_decryptor as single_file_decryptor
import image_encryptor.gui.processor.single_file_encryptor as single_file_encryptor
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.common.utils.utils import open_image, walk_file
from image_encryptor.gui.frame.drag import DragImport
from image_encryptor.gui.frame.design_frame import MainFrame as MF
from image_encryptor.gui.frame.tree import TreeManager, ImageItem
from image_encryptor.gui.modules.loader import load_program
from image_encryptor.gui.utils.thread import ThreadManager
from image_encryptor.gui.utils.utils import scale


class MainFrame(MF):
    """
    主窗口类
    """

    def __init__(self, parent, run_path=getcwd()):
        super().__init__(parent)
        self.program = load_program()
        self.drop = DragImport(self)
        self.SetDropTarget(self.drop)
        self.tree_manager = TreeManager(self, self.imageTreeCtrl, '已加载文件列表')
        # 准备
        self.supported_formats_str = ''
        for i in Image.EXTENSION:
            self.supported_formats_str += f'*{i}; '
        self.run_path = run_path
        self.preview_thread = ThreadManager('preview-thread')
        self.program.thread_pool.create_tag('load', True)
        self.program.thread_pool.create_tag('save', False)

        self.preview_image_size = (0, 0)
        self.loaded_image = None
        self.initial_preview = None
        self.processed_preview = None
        self.loaded_image_path = None
        self.default_settings = {
            'mode': 0,
            'row': 25,
            'col': 25,
            'upset': True,
            'flip': True,
            'rgb_mapping': False,
            'xor': 0,
            'save_path': '',
            'save_format': 21
        }

    @classmethod
    def run(cls, path=getcwd()):
        """
        运行入口函数
        """
        app = wx.App()
        self = cls(None, path)

        self.Show()

        app.MainLoop()

    @property
    def data_snapshot(self):
        return (self.initial_preview, self.processed_preview, self.settings)

    @property
    def settings(self):
        return {
            'mode': self.mode.Selection,
            'row': self.row.Value,
            'col': self.col.Value,
            'upset': self.upset.IsChecked(),
            'flip': self.flip.IsChecked(),
            'rgb_mapping': self.rgbMapping.IsChecked(),
            'xor': self.xorRgb.Selection,
            'save_path': self.selectSavePath.Path,
            'save_format': self.selectFormat.Selection
        }

    def show_initial_preview(self):
        size = self.importedImagePlanel.Size
        if self.loaded_image is not None:
            initial_preview = self.loaded_image.resize(scale(self.loaded_image, *size))
            self.program.logger.info(f'生成预览图{initial_preview.size}')
            self.importedImage.SetBitmap(wx.Bitmap.FromBuffer(*initial_preview.size, initial_preview.convert('RGB').tobytes()))
            self.initial_preview = initial_preview

    def show_processing_preview(self, resize: bool, image: Image.Image):
        size = self.previewedImagePlanel.Size
        if resize:
            image = image.resize(scale(image, *size))
        self.previewedImage.SetBitmap(wx.Bitmap.FromBuffer(*image.size, image.convert('RGB').tobytes()))
        self.processed_preview = image

    def _check_image(self, error, prompt=True):
        if error is not None:
            self.loaded_image = None
            if prompt:
                self.error(error, '加载图片时出现错误')
            return False
        else:
            self.show_initial_preview()
            self.imageInfo.SetLabelText(f'大小：{self.loaded_image.size[0]}x{self.loaded_image.size[1]}')
            self.previewOptions.Enable(True)
            self.saveOptions.Enable(True)
            return True

    def display_preview(self):
        self.generate_image(False)

    def generate_image(self, save):
        logger = self.saveProgressPrompt.SetLabelText if save else self.previewProgressPrompt.SetLabelText
        gauge = self.saveProgress if save else self.previewProgress
        image = self.loaded_image if save else self.initial_preview
        if self.update_password_dict():
            self.password.SetValue('none')
        try:
            if self.mode.Selection == 0:
                self.preview_thread.start_new(single_file_encryptor.main, self.generate_image_call_back, (self, logger, gauge, image, save))
            elif self.mode.Selection == 1:
                self.preview_thread.start_new(single_file_decryptor.main, self.generate_image_call_back, (self, logger, gauge, self.loaded_image, save))
            else:
                self.preview_thread.start_new(qq_anti_harmony.main, self.generate_image_call_back, (self, logger, gauge, image, save))
        except Exception:
            self.error(format_exc(), '生成加密图片时出现意外错误')

    def generate_image_call_back(self, error, image):
        if error is not None:
            self.error(repr(error), '生成加密图片时出现意外错误')
            return
        self.show_processing_preview(True, image)

    def load_image(self, dir):
        if dir in self.tree_manager.file_dict:
            self.imageTreeCtrl.SelectItem(self.tree_manager.file_dict[dir])
            self.warning('已存在同路径文件\n已自动跳转到相应位置')
            return
        elif dir in self.tree_manager.root_dir_dict:
            self.imageTreeCtrl.SelectItem(self.tree_manager.root_dir_dict[dir])
            self.warning('已存在同路径文件夹\n已自动跳转到相应位置')
            return
        elif dir in self.tree_manager.dir_dict:
            self.imageTreeCtrl.SelectItem(self.tree_manager.dir_dict[dir])
            self.warning('已存在同路径文件夹\n已自动跳转到相应位置')
            return
        Image.MAX_IMAGE_PIXELS = self.maxImagePixels.Value if self.maxImagePixels.Value != 0 else None
        if isdir(dir):
            for r, fl in walk_file(dir, True):
                for n in fl:
                    absolute_path = join(dir, r, n)
                    self.loaded_image, error = open_image(absolute_path)
                    if self._check_image(error, False):
                        self.tree_manager.add_file(dir, r, n, ImageItem(self.loaded_image, None, None, absolute_path, self.default_settings), False)
                    self.loaded_image_path = absolute_path
        elif isfile(dir):
            self.loaded_image, error = open_image(dir)
            if self._check_image(error):
                self.tree_manager.add_file(dir, data=ImageItem(self.loaded_image, None, None, dir, self.default_settings))
            self.loaded_image_path = dir
        self.imageTreeCtrl.SelectItem(list(self.tree_manager.file_dict.values())[-1])

    # -------
    # 事件交互
    # -------

    def manual_refresh(self, event):
        if self.previewMode.Selection == 0:
            return
        self.refresh_preview(None)

    def refresh_preview(self, event):
        if event is not None and self.previewMode.Selection != 2:
            return
        if self.loaded_image is not None:
            if self.importedImagePlanel.Size != self.preview_image_size:
                self.show_initial_preview()
            self.display_preview()

    def load_file(self, event):
        dialog = wx.FileDialog(self, "选择图像", self.run_path, EmptyString, self.supported_formats_str, wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST)
        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            if self.program.thread_pool.check_tag('load') is not None:
                self.warning('请等待当前图片载入完成后再载入新的图片')
                return
            self.program.thread_pool.add_task('load', self.program.thread_pool.submit(self.load_image, path))

    def load_select_file(self, event):
        if self.program.thread_pool.check_tag('load') is not None:
            self.warning('请等待当前图片载入完成后再载入新的图片')
            return
        self.program.thread_pool.add_task('load', self.program.thread_pool.submit(self.load_image, self.selectFile.Path))

    def update_password_dict(self, event=None):
        if self.password.Value == '':
            return True
        if event is not None:
            self.refresh_preview(event)
        if self.password.Value != 'none' and self.password.Value not in self.program.password_dict.values():
            password_base64 = PasswordDict.get_validation_field_base64(self.password.Value)
            self.program.password_dict[password_base64] = self.password.Value
            self.program.logger.info(f'更新密码字典[{password_base64}: {self.password.Value}](当前字典长度：{len(self.program.password_dict)})')
        return False

    def save_image(self, event):
        if not isdir(self.selectSavePath.Path):
            self.error('没有选择保存文件夹或选择的文件夹不存在', '保存时出现错误')
            return
        self.generate_image(True)

    def preview_mode_change(self, event):
        if self.previewMode.Selection == 0:
            self.previewedImage.Show(False)
        else:
            self.previewedImage.Show(True)

    def switch_image(self, event: 'wx.TreeEvent'):
        image_item = event.GetOldItem()
        if image_item.IsOk():
            image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(image_item)
            if image_data is not None:
                image_data.update(*self.data_snapshot)

        image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(event.GetItem())
        if image_data is not None:
            image_data.backtrack_interface(self)

    def apply_settings_to_all(self, event):
        settings = self.settings
        for i in self.tree_manager.file_dict.values():
            self.imageTreeCtrl.GetItemData(i).settings = settings

    def set_settings_as_default(self, event):
        self.default_settings = self.settings

    # -----
    # 提示窗
    # -----

    def info(self, message, title='信息'):
        self.program.logger.info(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def question(self, message, title='问题'):
        self.program.logger.info(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_QUESTION | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def warning(self, message, title='警告'):
        self.program.logger.warning(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def error(self, message, title='错误'):
        self.program.logger.error(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_ERROR | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def exit(self, event):
        self.program.logger.info('窗口退出')
        self.Destroy()
        exit()
