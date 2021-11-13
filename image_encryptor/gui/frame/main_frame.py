'''
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2021-11-13 11:59:12
Description  : 配置窗口类
'''
from hashlib import md5
from os import getcwd
from os.path import isdir
from traceback import format_exc

import wx
from PIL import Image
from wx.core import EmptyString

import image_encryptor.gui.processor.qq_anti_harmony as qq_anti_harmony
import image_encryptor.gui.processor.single_file_decryptor as single_file_decryptor
import image_encryptor.gui.processor.single_file_encryptor as single_file_encryptor
from image_encryptor import BRANCH, VERSION_NUMBER, SUB_VERSION_NUMBER
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.gui.frame.design_frame import MainFrame as MF
from image_encryptor.gui.frame.drag import DragImport
from image_encryptor.gui.frame.image_loader import ImageLoader
from image_encryptor.gui.frame.tree import TreeManager, ImageItem
from image_encryptor.gui.modules.loader import load_program
from image_encryptor.gui.modules.password_verifier import get_image_data
from image_encryptor.gui.utils.thread import ThreadManager
from image_encryptor.gui.utils.utils import scale


class MainFrame(MF):
    """
    主窗口类
    """

    def __init__(self, parent, run_path=getcwd()):
        super().__init__(parent)
        self.SetTitle(f'Image Encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH})')
        self.program = load_program()
        self.drop = DragImport(self)
        self.SetDropTarget(self.drop)
        self.tree_manager = TreeManager(self, self.imageTreeCtrl, '已加载文件列表')
        # 准备
        self.supported_formats_str = ''
        for i in Image.EXTENSION:
            self.supported_formats_str += f'*{i}; '
        self.run_path = run_path
        self.image_loader = ImageLoader(self)
        self.preview_thread = ThreadManager('preview-thread', True)
        self.program.thread_pool.create_tag('load', True)
        self.program.thread_pool.create_tag('save', False)

        self.preview_size = (0, 0)
        self.loaded_image = None
        self.initial_preview = None
        self.processed_preview = None
        self.loaded_image_path = None
        self.encrypted_image = None
        self.encryption_data = None
        self.preview_summary = None
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

        self.BACKTRACK = 5
        self.SWITCH_PAGE = 6

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
        return *self.data, self.settings

    @property
    def data(self):
        return self.initial_preview, self.processed_preview, self.preview_size, self.preview_summary, self.encrypted_image, self.encryption_data

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

    @property
    def encryption_settings_summary(self):
        return md5(str(list(self.settings.values())[:-2]).encode()).digest()

    def show_initial_preview(self, not_regenerate=False):
        size = self.importedImagePlanel.Size
        if not_regenerate:
            self.importedImage.SetBitmap(wx.Bitmap.FromBuffer(*self.initial_preview.size, self.initial_preview.convert('RGB').tobytes()))
            return
        if self.loaded_image is not None:
            initial_preview = self.loaded_image.resize(scale(self.loaded_image, *size))
            self.program.logger.info(f'生成预览图{initial_preview.size}')
            self.importedImage.SetBitmap(wx.Bitmap.FromBuffer(*initial_preview.size, initial_preview.convert('RGB').tobytes()))
            self.preview_size = size
            self.initial_preview = initial_preview

    def show_processing_preview(self, resize: bool, image: Image.Image):
        size = self.previewedImagePlanel.Size
        if image is None:
            return
        if resize:
            image = image.resize(scale(image, *size))
        self.previewedImage.SetBitmap(wx.Bitmap.FromBuffer(*image.size, image.convert('RGB').tobytes()))
        self.processed_preview = image
        self.preview_summary = self.encryption_settings_summary

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

    def check_encryption_parameters(self):
        if self.encrypted_image is None:
            image_data, error = get_image_data(self.loaded_image_path, skip_password=True)
            if error is None:
                self.encrypted_image = True
                self.encryption_data = image_data
        if self.encrypted_image:
            self.mode.Select(1)
            self.processingSettingsPanel1.Enable(False)
            self.xorRgb.Enable(False)
            self.row.SetValue(self.encryption_data['row'])
            self.col.SetValue(self.encryption_data['col'])
            self.upset.SetValue(self.encryption_data['upset'])
            self.rgbMapping.SetValue(self.encryption_data['rgb_mapping'])
            self.flip.SetValue(self.encryption_data['flip'])
            if self.encryption_data['xor_rgb'] and self.encryption_data['xor_alpha']:
                self.xorRgb.Select(2)
            elif self.encryption_data['xor_rgb']:
                self.xorRgb.Select(1)
            else:
                self.xorRgb.Select(0)

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
            size_changed = False
            if self.importedImagePlanel.Size != self.preview_size or self.initial_preview is None:
                size_changed = True
                self.show_initial_preview()
            else:
                self.show_initial_preview(True)
            if size_changed or self.encryption_settings_summary != self.preview_summary:
                self.generate_image(False)
            elif self.processed_preview is not None:
                self.show_processing_preview(False, self.processed_preview)

    def load_file(self, event):
        dialog = wx.FileDialog(self, "选择图像", self.run_path, EmptyString, self.supported_formats_str, wx.FD_OPEN | wx.FD_CHANGE_DIR | wx.FD_PREVIEW | wx.FD_FILE_MUST_EXIST)
        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            self.image_loader.load(path)

    def load_dir(self, event):
        dialog = wx.DirDialog(self, "选择文件夹", self.run_path, wx.DIRP_CHANGE_DIR | wx.DIRP_DIR_MUST_EXIST)
        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            self.image_loader.load(path)

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
        if self.loaded_image is None:
            self.error('没有载入图片')
            return
        elif not isdir(self.selectSavePath.Path):
            self.error('没有选择保存文件夹或选择的文件夹不存在', '保存时出现错误')
            return
        self.generate_image(True)

    def processing_mode_change(self, event):
        if self.loaded_image is None:
            return
        if self.mode.Selection != 1:
            self.processingSettingsPanel1.Enable(True)
            self.xorRgb.Enable(True)
        else:
            self.check_encryption_parameters()
        self.refresh_preview(event)

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

            if self.processed_preview is not None:
                self.show_processing_preview(False, self.processed_preview)
            if self.previewMode.Selection == 2:
                self.refresh_preview(event)
            else:
                if self.initial_preview is None:
                    self.show_initial_preview()
                else:
                    self.show_initial_preview(True)

    def apply_settings_to_all(self, event):
        settings = self.settings
        for i in self.tree_manager.file_dict.values():
            self.imageTreeCtrl.GetItemData(i).settings = settings

    def set_settings_as_default(self, event):
        self.default_settings = self.settings

    def stop_loading(self, event, force=True):
        if force:
            self.image_loader.loading_thread.kill()
        self.loadingPrograssPanel.Hide()
        self.loadingPanel.Show()
        self.settingsPanel.Layout()
        if force:
            self.warning('已强制终止载入文件')
        else:
            self.warning('已停止载入文件')

    def set_stop_loading_signal(self, event):
        self.preview_thread.set_exit_signal()

    # -----
    # 提示窗
    # -----

    def info(self, message, title='信息'):
        self.program.logger.info(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_INFORMATION | wx.STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def question(self, message, title='问题'):
        self.program.logger.info(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_QUESTION | wx.STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def warning(self, message, title='警告'):
        self.program.logger.warning(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def error(self, message, title='错误'):
        self.program.logger.error(f'[{title}]{message}')
        dialog = wx.MessageDialog(self, message, title, style=wx.ICON_ERROR | wx.STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def confirmation_frame(self, message, title='确认', style=wx.YES_NO | wx.CANCEL, yes='是', no='否', cancel='取消'):
        dialog = wx.MessageDialog(self, message, title, style=style | wx.STAY_ON_TOP)
        dialog.SetYesNoCancelLabels(yes, no, cancel)
        frame_id = dialog.ShowModal()
        dialog.Destroy()
        return frame_id

    def exit(self, event):
        self.program.logger.info('窗口退出')
        self.Destroy()
        exit()
