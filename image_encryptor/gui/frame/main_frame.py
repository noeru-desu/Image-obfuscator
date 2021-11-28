'''
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2021-11-28 15:42:43
Description  : 覆写窗口
'''
from concurrent.futures import ThreadPoolExecutor
from hashlib import md5
from multiprocessing import cpu_count
from os import getcwd
from sys import version
from typing import TYPE_CHECKING

from image_encryptor import BRANCH, SUB_VERSION_NUMBER, VERSION_BATCH, VERSION_NUMBER
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.common.utils.logger import Logger
from image_encryptor.gui.frame.design_frame import MainFrame as MF
from image_encryptor.gui.frame.drag_importer import DragLoader, DragSavingPath
from image_encryptor.gui.frame.image_generator import ImageGenerator
from image_encryptor.gui.frame.image_loader import ImageLoader
from image_encryptor.gui.frame.image_saver import ImageSaver
from image_encryptor.gui.frame.tree_manager import TreeManager
from image_encryptor.gui.frame.utils import SegmentTrigger
from image_encryptor.gui.modules.password_verifier import get_image_data
from image_encryptor.gui.utils.exit_processor import ExitProcessor
from image_encryptor.gui.utils.utils import ProcessTaskManager, scale
from PIL import Image
from wx import (CANCEL, DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, HELP, ICON_ERROR,
                ICON_INFORMATION, ICON_QUESTION, ICON_WARNING, ID_OK,
                STAY_ON_TOP, YES_NO, App, Bitmap, DirDialog, FileDialog,
                MessageDialog)
from wx.core import EmptyString

if TYPE_CHECKING:
    from wx import TreeEvent, TreeItemId


class MainFrame(MF):
    """
    主窗口类
    """

    def __init__(self, parent, run_path=getcwd()):
        super().__init__(parent)
        self.SetTitle(f'Image Encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH})')

        # 实例化组件
        self.logger = Logger('image-encryptor')
        self.logger.info(f'Python {version}')
        self.logger.info(f'You are using Image encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH}) (batch: {VERSION_BATCH})')
        self.password_dict = PasswordDict()
        self.exit_processor = ExitProcessor()
        self.process_pool = ProcessTaskManager(1 if cpu_count() < 4 else cpu_count() - 2)
        self.exit_processor.register(lambda process_pool: process_pool.shutdown(wait=False, cancel_futures=True), self.process_pool)
        self.thread_pool = ThreadPoolExecutor(cpu_count())
        self.exit_processor.register(lambda thread_pool: thread_pool.shutdown(wait=False, cancel_futures=True), self.thread_pool)
        self.imageTreeCtrl.SetDropTarget(DragLoader(self))
        self.savingOptions.SetDropTarget(DragSavingPath(self))
        self.tree_manager = TreeManager(self, self.imageTreeCtrl, '已加载文件列表')
        self.image_loader = ImageLoader(self)
        self.image_generator = ImageGenerator(self)
        self.image_saver = ImageSaver(self)
        self.stop_loading_func = SegmentTrigger((self.set_stop_loading_signal, self.stop_loading), self.init_loading_plane)

        # 准备工作
        self.xorPanel.Disable()
        self.run_path = run_path

        self.image_item = None
        self.default_settings = {
            'mode': 0,
            'row': 25,
            'col': 25,
            'shuffle': True,
            'flip': True,
            'rgb_mapping': False,
            'xor_channels': 'rgb',
            'noise_xor': False,
            'password': None,
            'saving_path': '',
            'saving_format': 21,
            'quality': 98,
            'subsampling': 0
        }

        self.get_settings = {
            'mode': lambda: self.mode.Selection,
            'row': lambda: self.row.Value,
            'col': lambda: self.col.Value,
            'shuffle': lambda: self.shuffle.Value,
            'flip': lambda: self.flip.Value,
            'rgb_mapping': lambda: self.rgbMapping.Value,
            'xor_channels': lambda: self.xor_channels,
            'noise_xor': lambda: self.noiseXor.Value,
            'noise_factor': lambda: self.noiseFactor.Value,
            'password': lambda: self.password.Value,
            'saving_path': lambda: self.selectSavePath.Path,
            'saving_format': lambda: self.selectFormat.Selection,
            'quality': lambda: self.saveQuality.Value,
            'subsampling': lambda: self.subsamplingLevel.Value
        }

        self.logger.info('窗口初始化完成')

    @classmethod
    def run(cls, path=getcwd()):
        """
        运行入口函数
        """
        app = App(useBestVisual=True)
        self = cls(None, path)

        self.Show()

        app.MainLoop()

    @property
    def settings(self):
        return {
            'mode': self.mode.Selection,
            'row': self.row.Value,
            'col': self.col.Value,
            'shuffle': self.shuffle.Value,
            'flip': self.flip.Value,
            'rgb_mapping': self.rgbMapping.Value,
            'xor_channels': self.xor_channels,
            'noise_xor': self.noiseXor.Value,
            'noise_factor': self.noiseFactor.Value,
            'password': self.password.Value,
            'saving_path': self.selectSavePath.Path,
            'saving_format': self.selectFormat.Selection,
            'quality': self.saveQuality.Value,
            'subsampling': self.subsamplingLevel.Value
        }

    @property
    def xor_channels(self):
        if not self.xor.Value:
            return ''
        channels = []
        if self.xorR.Value:
            channels.append('r')
        if self.xorG.Value:
            channels.append('g')
        if self.xorB.Value:
            channels.append('b')
        if self.xorA.Value:
            channels.append('a')
        return ''.join(channels)

    @property
    def encryption_settings(self):
        return (self.mode.Selection, self.row.Value, self.col.Value,
                self.shuffle.Value, self.flip.Value, self.rgbMapping.Value,
                self.noiseXor.Value, self.xorR.Value, self.xorG.Value,
                self.xorB.Value, self.xorA.Value, self.noiseFactor.Value,
                self.password.Value)

    @property
    def encryption_settings_summary(self):
        return md5(str(self.encryption_settings).encode()).digest()

    def show_initial_preview(self, not_regenerate=False):
        size = self.importedImagePlanel.Size
        if not_regenerate:
            self.importedImage.SetBitmap(Bitmap.FromBuffer(*self.image_item.initial_preview.size, self.image_item.initial_preview.convert('RGB').tobytes()))
            return
        if self.image_item is not None:
            initial_preview = self.image_item.loaded_image.resize(scale(self.image_item.loaded_image, *size))
            self.logger.info(f'生成预览图{initial_preview.size}')
            self.importedImage.SetBitmap(Bitmap.FromBuffer(*initial_preview.size, initial_preview.convert('RGB').tobytes()))
            self.image_item.preview_size = size
            self.image_item.initial_preview = initial_preview

    def show_processing_preview(self, resize: bool, image: Image.Image):
        size = self.previewedImagePlanel.Size
        if image is None:
            return
        if resize:
            image = image.resize(scale(image, *size))
        self.previewedImage.SetBitmap(Bitmap.FromBuffer(*image.size, image.convert('RGB').tobytes()))
        self.image_item.processed_preview = image
        self.image_item.preview_summary = self.encryption_settings_summary

    def check_encryption_parameters(self):
        if self.image_item.encrypted_image is None:
            image_data, self.image_item.loading_image_data_error = get_image_data(self.image_item.loaded_image_path, skip_password=True)
            if self.image_item.loading_image_data_error is None:
                self.image_item.encrypted_image = True
                self.image_item.encryption_data = image_data
                self.image_item.encryption_data['password'] = None
            else:
                self.image_item.encrypted_image = False
        if self.image_item.encrypted_image:
            self.image_item.backtrack_decryption_interface()

    def init_loading_plane(self):
        self.loadingPrograss.SetValue(0)
        self.loadingPrograssText.SetLabelText(EmptyString)
        self.stopLoadingBtn.SetLabelText('停止载入')

    def stop_loading(self, force=True):
        if force:
            self.image_loader.loading_thread.kill()
            self.image_loader.hide_loading_progress_plane()
            self.warning('已强制终止载入文件')
        else:
            self.warning('已停止载入文件')
        self.stop_loading_func.init()

    def set_stop_loading_signal(self):
        self.image_loader.loading_thread.set_exit_signal()
        self.stopLoadingBtn.SetLabelText('强制终止载入')

    def apply_settings_to_all(self, settings=None):
        if settings is None:
            settings = self.settings
            for i in self.tree_manager._all_item_data:
                i.settings = settings.copy()
        else:
            settings = {}
            for i in settings:
                settings[i] = self.get_settings[i]()
            for i in self.tree_manager._all_item_data:
                i.settings.update(settings)

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
        if self.image_item is not None:
            size_changed = False
            if self.importedImagePlanel.Size != self.image_item.preview_size or self.image_item.initial_preview is None:
                size_changed = True
                self.show_initial_preview()
            else:
                self.show_initial_preview(True)
            if size_changed or self.encryption_settings_summary != self.image_item.preview_summary:
                self.image_generator.generate_preview()
            elif self.image_item.processed_preview is not None:
                self.show_processing_preview(False, self.image_item.processed_preview)

    def load_file(self, event):
        dialog = FileDialog(self, "选择图像", style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST)
        if ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            self.image_loader.load(path)

    def load_dir(self, event):
        dialog = DirDialog(self, "选择文件夹", style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST)
        if ID_OK == dialog.ShowModal():
            path = dialog.GetPath()
            self.image_loader.load(path)

    def update_password_dict(self, event=None):
        if self.password.Value == '':
            return True
        if event is not None:
            self.refresh_preview(event)
        if self.password.Value != 'none' and self.password.Value not in self.password_dict.values():
            password_base64 = PasswordDict.get_validation_field_base64(self.password.Value)
            self.password_dict[password_base64] = self.password.Value
            self.logger.info(f'更新密码字典[{password_base64}: {self.password.Value}](当前字典长度：{len(self.password_dict)})')
        return False

    def save_selected_image(self, event):
        self.image_saver.save_selected_image()

    def bulk_save(self, event):
        self.image_saver.bulk_save()

    def processing_mode_change(self, event):
        if self.image_item is None:
            return
        if self.mode.Selection != 1:
            self.processingSettingsPanel1.Enable()
            self.password.Enable()
        else:
            self.check_encryption_parameters()
            if self.image_item.loading_image_data_error is not None:
                if self.image_item.settings['mode'] != 1:
                    self.mode.Select(self.image_item.settings['mode'])
                elif self.default_settings['mode'] != 1:
                    self.mode.Select(self.default_settings['mode'])
                else:
                    self.mode.Select(0)
                self.warning(self.image_item.loading_image_data_error)
        self.refresh_preview(event)

    def preview_mode_change(self, event):
        if self.previewMode.Selection == 0:
            self.previewedImage.Show(False)
        else:
            self.previewedImage.Show(True)
            self.refresh_preview(event)

    def switch_image(self, event: 'TreeEvent'):
        image_item: 'TreeItemId' = event.GetOldItem()
        if image_item.IsOk():
            image_data = self.imageTreeCtrl.GetItemData(image_item)
            if image_data is not None:
                settings = self.settings
                if settings['mode'] != image_data.settings['mode']:
                    image_data.manual_switch_mode = True
                image_data.settings = settings
        else:
            self.apply_settings_to_all(event)

        image_data = self.imageTreeCtrl.GetItemData(event.GetItem())
        if image_data is not None:
            self.image_item = image_data
            image_data.backtrack_interface()

            if self.previewMode.Selection == 2:
                self.refresh_preview(event)
            elif self.image_item.processed_preview is not None:
                self.show_processing_preview(False, self.image_item.processed_preview)
            if self.previewMode.Selection != 2:
                if self.image_item.initial_preview is None:
                    self.show_initial_preview()
                else:
                    self.show_initial_preview(True)

    def sync_saving_settings(self, event):
        if not self.autoSyncSavingSettings.Value:
            return
        for i in self.tree_manager._all_item_data:
            i.settings['saving_path'] = self.get_settings['saving_path']()
            i.settings['saving_format'] = self.get_settings['saving_format']()

    def set_settings_as_default(self, event):
        self.default_settings = self.settings

    def stop_loading_event(self, event):
        self.stop_loading_func.call()

    def stop_saving_event(self, event):
        self.image_saver.cancel()
        self.info('已取消尚未进行的任务')
        self.stopSavingBtn.Disable()

    def apply_to_all(self, event):
        self.apply_settings_to_all()

    def toggle_factor_slider_switch(self, event):
        self.noiseFactor.Enable(event.IsChecked())
        self.refresh_preview(event)

    def toggle_xor_panel_switch(self, event):
        self.xorPanel.Enable(event.IsChecked())
        self.refresh_preview(event)

    def update_quality_num(self, event):
        self.qualityNum.SetLabelText(str(event.Int))

    def update_subsampling_num(self, event):
        self.subsamplingNum.SetLabelText(str(event.Int))

    # -----
    # 提示窗
    # -----

    def info(self, message, title='信息'):
        self.logger.info(f'[{title}]{message}')
        dialog = MessageDialog(self, message, title, style=ICON_INFORMATION | STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def question(self, message, title='问题'):
        self.logger.info(f'[{title}]{message}')
        dialog = MessageDialog(self, message, title, style=ICON_QUESTION | STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def warning(self, message, title='警告'):
        self.logger.warning(f'[{title}]{message}')
        dialog = MessageDialog(self, message, title, style=ICON_WARNING | STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def error(self, message, title='错误'):
        self.logger.error(f'[{title}]{message}')
        dialog = MessageDialog(self, message, title, style=ICON_ERROR | STAY_ON_TOP)
        dialog.ShowModal()
        dialog.Destroy()

    def confirmation_frame(self, message, title='确认', style=YES_NO | CANCEL, yes='是', no='否', cancel='取消', help=None):
        if help is not None:
            style = YES_NO | CANCEL | HELP
        else:
            style = YES_NO | CANCEL
        dialog = MessageDialog(self, message, title, style=style | STAY_ON_TOP)
        if help is not None:
            dialog.SetOKLabel(help)
        dialog.SetYesNoCancelLabels(yes, no, cancel)
        frame_id = dialog.ShowModal()
        dialog.Destroy()
        return frame_id

    def exit(self, event):
        self.logger.info('窗口退出')
        self.Destroy()
        exit()
