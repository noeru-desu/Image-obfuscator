'''
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2021-10-23 11:36:43
Description  : 配置窗口类
'''
from os import getcwd
from random import randint

from PIL import Image
import wx
from wx.core import EmptyString

from image_encryptor.frame.design_frame import MainFrame as MF
from image_encryptor.modules.image_encrypt import ImageEncrypt
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.utils import scale, open_image


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

    def manual_refresh(self, event):
        if self.previewMode.Selection == 0:
            return
        self.refresh_preview(None)

    def refresh_preview(self, event):
        if event is not None and self.previewMode.Selection != 2:
            return
        if self.program.loaded_image is not None:
            if self.preview_size != self.importedImageScrolled.Size:
                self.display_preview_original_image()
            self.generate_preview()

    def display_preview_original_image(self):
        size = self.importedImageScrolled.Size
        if self.program.loaded_image is not None:
            self.program.preview_original_image = self.program.loaded_image.resize(scale(self.program.loaded_image, *size))
            self.preview_size = size
            self.program.logger.info(f'重新缩放预览图并显示{self.program.preview_original_image.size}')
            self.importedImage.SetBitmap(wx.Bitmap.FromBuffer(*self.program.preview_original_image.size, self.program.preview_original_image.convert('RGB').tobytes()))

    def display_preview_image(self):
        self.previewedImage.SetBitmap(wx.Bitmap.FromBuffer(*self.program.preview_image.size, self.program.preview_image.convert('RGB').tobytes()))

    def load_file(self, event):
        dialog = wx.FileDialog(self, "选择需要加载的图片", self.run_path, EmptyString, self.supported_formats_str, wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST)
        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            self.program.loaded_image, error = open_image(path)
            if error is not None:
                self.program.loaded_image = None
                self.error(error, '加载图片时出现错误')
            else:
                self.display_preview_original_image()
                self.processingOptions.Enable(True)

    def generate_preview(self):
        self.processingOptions.Enable(False)
        if self.mode.Selection != 2:
            image_encrypt = ImageEncrypt(self.program.preview_original_image, self.row.Value, self.col.Value, 100 if self.password.Value == 'none' else self.password.Value)
            if self.normalEncryption.IsChecked():
                self.previewProgressPrompt.SetLabelText('正在分割原图')
                bar = ProgressBar(self.previewProgress, self.row.Value * self.col.Value)
                image_encrypt.init_block_data(self.program.preview_original_image, True if self.mode.Selection == 1 else False, bar)

                self.previewProgressPrompt.SetLabelText('正在重组')
                bar = ProgressBar(self.previewProgress, self.row.Value * self.col.Value)
                image = image_encrypt.get_image(self.program.preview_original_image, self.rgbMapping.IsChecked(), bar)

            if self.xorRgb.Selection != 0:
                self.previewProgressPrompt.SetLabelText('正在异或加密，性能较低，请耐心等待')
                image = image_encrypt.xor_pixels(image, True if self.xorRgb.Selection == 2 else False)
        else:
            image = self.program.preview_original_image
            image.putpixel((0, 0), (randint(0, 255), randint(0, 255), randint(0, 255)))
            image.putpixel((image.size[0] - 1, 0), (randint(0, 255), randint(0, 255), randint(0, 255)))
            image.putpixel((0, image.size[1] - 1), (randint(0, 255), randint(0, 255), randint(0, 255)))
            image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.previewProgressPrompt.SetLabelText('完成')
        self.program.preview_image = image
        self.processingOptions.Enable(True)
        self.display_preview_image()

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


class ProgressBar(object):
    def __init__(self, target: wx.Gauge, max_value: int):
        self.target = target
        self.max_value = max_value
        self.value = 0
        self.target.SetRange(max_value)

    def update(self, value):
        self.target.SetValue(value)

    def finish(self):
        self.target.SetValue(self.max_value)
