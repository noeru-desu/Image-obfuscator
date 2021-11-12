'''
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2021-11-12 17:28:48
Description  : 配置窗口类
'''
from hashlib import md5
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
from image_encryptor.common.utils.utils import open_image
from image_encryptor.gui.frame.drag import DragImport
from image_encryptor.gui.frame.design_frame import MainFrame as MF
from image_encryptor.gui.frame.tree import TreeManager, ImageItem
from image_encryptor.gui.modules.loader import load_program
from image_encryptor.gui.modules.password_verifier import get_image_data
from image_encryptor.gui.utils.thread import ThreadManager
from image_encryptor.gui.utils.utils import ProgressBar, scale, walk_file


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
        self.preview_thread = ThreadManager('preview-thread', True)
        self.loading_thread = ThreadManager('loading-thread')
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

    def _check_image(self, error, prompt=True, show_preview=True):
        if error is not None:
            self.loaded_image = None
            if prompt:
                self.error(error, '加载图片时出现错误')
            return False
        else:
            if show_preview:
                self.show_initial_preview()
                self.imageInfo.SetLabelText(f'大小：{self.loaded_image.size[0]}x{self.loaded_image.size[1]}')
            return True

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
            self.imageTreeCtrl.Expand(self.tree_manager.file_dict[dir])
            self.warning('已存在同路径文件\n已自动跳转到相应位置')
            return
        elif dir in self.tree_manager.root_dir_dict:
            self.imageTreeCtrl.SelectItem(self.tree_manager.root_dir_dict[dir])
            self.imageTreeCtrl.Expand(self.tree_manager.root_dir_dict[dir])
            self.warning('已存在同路径文件夹\n已自动跳转到相应位置')
            return
        elif dir in self.tree_manager.dir_dict:
            self.imageTreeCtrl.SelectItem(self.tree_manager.dir_dict[dir])
            self.imageTreeCtrl.Expand(self.tree_manager.dir_dict[dir])
            self.warning('已存在同路径文件夹\n已自动跳转到相应位置')
            return
        self.loadingPanel.Hide()
        self.loadingPrograssPanel.Show()
        self.settingsPanel.Layout()
        Image.MAX_IMAGE_PIXELS = self.maxImagePixels.Value if self.maxImagePixels.Value != 0 else None
        if isdir(dir):
            self.preview_thread.set_exit_signal(False)
            frame_id = self.confirmation_frame('是否将文件夹内子文件夹中的文件也进行载入？', '选择')
            if frame_id == wx.ID_YES:
                topdown = True
            elif frame_id == wx.ID_NO:
                topdown = False
            else:
                self.loadingPrograssPanel.Hide()
                self.loadingPanel.Show()
                self.settingsPanel.Layout()
                return
            file_num, files = walk_file(dir, topdown)
            self.loadingPrograssText.SetLabelText(f'0/{file_num} - 0%')
            finish_num = 0
            bar = ProgressBar(self.loadingPrograss, 1)
            bar.next_step(file_num)
            for r, fl in files:
                for n in fl:
                    absolute_path = join(dir, r, n)
                    self.loaded_image, error = open_image(absolute_path)
                    if self._check_image(error, False, False):
                        self.tree_manager.add_file(dir, r, n, ImageItem(self.loaded_image, absolute_path, self.default_settings), False)
                        self.loaded_image_path = absolute_path
                    finish_num += 1
                    self.loadingPrograssText.SetLabelText(f"{finish_num}/{file_num} - {format(finish_num / file_num * 100, '.2f')}%")
                    bar.update(bar.value + 1)
                    if self.preview_thread.exit_signal:
                        self.stop_loading(None, False)
                        return
            self.loadingPrograssText.SetLabelText(f'{file_num}/{file_num} - 100%')
            bar.over()
        elif isfile(dir):
            self.loadingPrograssText.SetLabelText('0/1 - 0%')
            self.loadingPrograss.SetValue(0)
            self.loaded_image, error = open_image(dir)
            if self._check_image(error, show_preview=False):
                self.tree_manager.add_file(dir, data=ImageItem(self.loaded_image, dir, self.default_settings))
            self.loaded_image_path = dir
            self.loadingPrograssText.SetLabelText('1/1 - 100%')
            self.loadingPrograss.SetValue(100)
        # self.imageTreeCtrl.SelectItem(list(self.tree_manager.file_dict.values())[-1])
        self.loadingPrograssPanel.Hide()
        self.loadingPanel.Show()
        self.settingsPanel.Layout()

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
            if self.loading_thread.is_running:
                self.warning('请等待当前图片载入完成后再载入新的图片')
                return
            self.loading_thread.start_new(self.load_image, args=(path,))

    def load_dir(self, event):
        dialog = wx.DirDialog(self, "选择文件夹", self.run_path, wx.DIRP_CHANGE_DIR | wx.DIRP_DIR_MUST_EXIST)
        if wx.ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            if self.loading_thread.is_running:
                self.warning('请等待当前图片载入完成后再载入新的图片')
                return
            self.loading_thread.start_new(self.load_image, args=(path,))

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
            self.loading_thread.kill()
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
