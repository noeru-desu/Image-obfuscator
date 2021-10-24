'''
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2021-10-24 19:26:34
Description  : 配置窗口类
'''
from os import getcwd
from os.path import isdir
from concurrent.futures import CancelledError
from traceback import format_exc, print_exc

import wx
from PIL import Image
from wx.core import EmptyString

import image_encryptor.programs.single_file_decryptor as single_file_decryptor
import image_encryptor.programs.qq_anti_harmony as qq_anti_harmony
import image_encryptor.programs.single_file_encryptor as single_file_encryptor
from image_encryptor.frame.design_frame import MainFrame as MF
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.password_verifier import PasswordDict
from image_encryptor.utils.utils import open_image, scale


class MainFrame(MF):
    """
    主窗口类
    """
    def __init__(self, parent, run_path=getcwd()):
        super().__init__(parent)
        self.program = load_program()
        self.supported_formats_str = ''
        for i in Image.EXTENSION:
            self.supported_formats_str += f'*{i}; '
        self.run_path = run_path
        self.program.thread_pool.create_tag('preview', True)
        self.program.thread_pool.create_tag('save', False)
        self.preview_size = (0, 0)

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
    def preview_image_size(self):
        w, h = self.imagePanel.Size
        sh = self.imageStaticline.Size[1]
        return w, int((h - sh) / 2)

    def manual_refresh(self, event):
        if self.previewMode.Selection == 0:
            return
        self.refresh_preview(None)

    def refresh_preview(self, event):
        if event is not None and self.previewMode.Selection != 2:
            return
        if self.program.data.loaded_image is not None:
            if self.preview_size != self.preview_image_size:
                self.display_preview_original_image()
            self.display_preview()
        if event is not None:
            event.Skip()

    def display_preview_original_image(self):
        self.xorRgb.Selection
        size = self.preview_image_size
        if self.program.data.loaded_image is not None:
            self.program.data.preview_original_image = self.program.data.loaded_image.resize(scale(self.program.data.loaded_image, *size))
            self.preview_size = size
            self.program.logger.info(f'重新缩放预览图{self.program.data.preview_original_image.size}并显示')
            self.importedImage.SetBitmap(wx.Bitmap.FromBuffer(*self.program.data.preview_original_image.size, self.program.data.preview_original_image.convert('RGB').tobytes()))

    def display_preview_image(self, resize):
        size = self.preview_image_size
        if resize:
            self.program.data.preview_image = self.program.data.preview_image.resize(scale(self.program.data.preview_image, *size))
        self.previewedImage.SetBitmap(wx.Bitmap.FromBuffer(*self.program.data.preview_image.size, self.program.data.preview_image.convert('RGB').tobytes()))

    def load_file(self, event):
        dialog = wx.FileDialog(self, "选择图像", self.run_path, EmptyString, self.supported_formats_str, wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST)
        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            Image.MAX_IMAGE_PIXELS = self.maxImagePixels.Value if self.maxImagePixels.Value != 0 else None
            self.program.data.loaded_image, error = open_image(path)
            self._check_image(error)

    def load_select_file(self, event):
        self.program.data.loaded_image_path = self.selectFile.Path
        Image.MAX_IMAGE_PIXELS = self.maxImagePixels.Value if self.maxImagePixels.Value != 0 else None
        self.program.data.loaded_image, error = open_image(self.program.data.loaded_image_path)
        self._check_image(error)

    def _check_image(self, error):
        if error is not None:
            self.program.data.loaded_image = None
            self.error(error, '加载图片时出现错误')
        else:
            self.display_preview_original_image()
            self.imageInfo.SetLabelText(f'大小：{self.program.data.loaded_image.size[0]}x{self.program.data.loaded_image.size[1]}')
            self.previewOptions.Enable(True)
            self.saveOptions.Enable(True)

    def display_preview(self):
        self.generate_image(False)
        # self.display_preview_image(True if self.mode.Selection == 1 else False)

    def generate_image(self, save):
        tag = 'save' if save else 'preview'
        check = self.program.thread_pool.check_tag(tag)
        if check is not None:
            self.error(check, '无法执行任务')
        logger = self.saveProgressPrompt.SetLabelText if save else self.previewProgressPrompt.SetLabelText
        gauge = self.saveProgress if save else self.previewProgress
        image = self.program.data.loaded_image if save else self.program.data.preview_original_image
        self.update_password_dict()
        try:
            if self.mode.Selection == 0:
                self.program.thread_pool.add_task(tag, self.program.thread_pool.submit(single_file_encryptor.main, self, logger, gauge, image, save), self.generate_image_call_back)
            elif self.mode.Selection == 1:
                self.program.thread_pool.add_task(tag, self.program.thread_pool.submit(single_file_decryptor.main, self, logger, gauge, self.program.data.loaded_image, save), self.generate_image_call_back)
            else:
                self.program.thread_pool.add_task(tag, self.program.thread_pool.submit(qq_anti_harmony.main, self, logger, gauge, image, save), self.generate_image_call_back)
        except Exception:
            self.program.thread_pool.del_future(tag)
            print_exc()
            self.error(format_exc(), '出现意外错误')

    def update_password_dict(self, event=None):
        if event is not None:
            self.refresh_preview(event)
        if self.password.Value != 'none' and self.password.Value not in self.program.password_dict.values():
            password_base64 = PasswordDict.get_validation_field_base64(self.password.Value)
            self.program.logger.info(f'更新密码字典[{password_base64}: {self.password.Value}](当前字典长度：{len(self.program.password_dict)})')
            self.program.password_dict[PasswordDict.get_validation_field_base64(self.password.Value)] = self.password.Value

    def save_image(self, event):
        if not isdir(self.selectSavePath.Path):
            self.error('没有选择保存文件夹或选择的文件夹不存在', '保存时出现错误')
            return
        self.generate_image(True)

    def generate_image_call_back(self, futures):
        try:
            self.program.data.preview_image, save = futures.result()
        except CancelledError:
            return
        self.program.thread_pool.del_future('save' if save else 'preview', futures)
        self.display_preview_image(True)

    def preview_mode_change(self, event):
        if self.previewMode.Selection == 0:
            self.previewedImage.Show(False)
        else:
            self.previewedImage.Show(True)

    def info(self, message, title=''):
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def question(self, message, title=''):
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_QUESTION | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def warning(self, message, title=''):
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def error(self, message, title=''):
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_ERROR | wx.STAY_ON_TOP)
        if dialog.ShowModal() == wx.ID_YES:
            self.Close(True)
        dialog.Destroy()

    def exit(self, event):
        self.Destroy()
        exit()
