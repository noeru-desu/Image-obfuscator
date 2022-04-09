"""
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2022-04-05 09:15:35
Description  : 事件处理
"""
from typing import TYPE_CHECKING

from PIL import ImageGrab
from wx import (DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, ID_OK,
                DirDialog, FileDialog)

from image_encryptor import constants
from image_encryptor.frame.file_item import FolderItem, ImageItem
from image_encryptor.frame.main_frame import MainFrame as BasicMainFrame

if TYPE_CHECKING:
    from wx import CommandEvent, SizeEvent, SpinEvent, TreeEvent, TreeItemId


class MainFrame(BasicMainFrame):
    __slots__ = ('deleted_item', 'resized', 'first_choice')

    def __init__(self, parent, run_path=...):
        super().__init__(parent, run_path)
        self.deleted_item = False
        self.resized = False
        self.first_choice = True

    def on_move_end(self, event):
        if self.resized:
            self.refresh_preview(event)
            self.resized = False
        event.Skip()

    def on_size(self, event: 'SizeEvent'):
        self.resized = True
        event.Skip()

    def manually_refresh(self, event):
        if self.controls.preview_mode != constants.DO_NOT_REFRESH:
            self.force_refresh_preview()

    def refresh_preview(self, event=None):
        if self.image_item is None:
            return
        if event is not None and self.controls.preview_mode != constants.AUTO_REFRESH:
            return
        self.image_item.display_initial_preview()
        self.image_item.display_processed_preview()

    def force_refresh_preview(self, event=None):
        if self.image_item is None:
            return
        self.image_item.display_initial_preview(False)
        self.image_item.display_processed_preview(False)

    def load_file(self, event):
        with FileDialog(self, "选择图像", style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST) as dialog:
            if ID_OK == dialog.ShowModal():
                self.image_loader.load(dialog.GetPath())

    def load_dir(self, event):
        with DirDialog(self, "选择文件夹", style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST) as dialog:
            if ID_OK == dialog.ShowModal():
                self.image_loader.load(dialog.GetPath())

    def load_image_from_clipboard(self, event):
        clipboard = ImageGrab.grabclipboard()
        if clipboard is None:
            self.dialog.async_warning('没有从剪切板导入任何图像')
        else:
            self.image_loader.load(clipboard)

    def update_password_dict(self, event=None):
        """更新成功则返回True"""
        if self.controls.password == '':
            return False
        if event is not None:
            self.refresh_preview(event)
        if self.controls.password != 'none' and self.controls.password not in self.password_dict.values():
            if self.add_password_dict(self.controls.password):
                return True
            self.controls.password = ''
            return False
        return True

    def save_selected_image(self, event):
        self.image_saver.save_selected_image()

    def bulk_save(self, event):
        self.image_saver.bulk_save()

    def processing_mode_change(self, event):
        if self.image_item is None and self.controls.proc_mode == constants.DECRYPTION_MODE:
            self.controls.proc_mode = self.controls.previous_proc_mode
            return
        elif self.controls.proc_mode != constants.DECRYPTION_MODE:
            if self.controls.proc_mode == constants.ANTY_HARMONY_MODE:
                self.controls.frame.processingSettingsPanel1.Disable()
                self.controls.frame.passwordCtrl.Disable()
            else:
                self.controls.frame.processingSettingsPanel1.Enable()
                self.controls.frame.passwordCtrl.Enable()
        else:
            self.image_item.check_encryption_parameters()
            if self.image_item.cache.loading_encryption_attributes_error is not None:
                self.controls.proc_mode = self.controls.previous_proc_mode
                self.dialog.async_warning(self.image_item.cache.loading_encryption_attributes_error)
                return
        self.controls.previous_proc_mode = self.controls.proc_mode
        self.refresh_preview(event)

    def preview_mode_change(self, event):
        if self.controls.preview_mode == constants.DO_NOT_REFRESH:
            self.previewedBitmap.Show(False)
        else:
            self.previewedBitmap.Show(True)
            self.refresh_preview(event)

    def switch_image(self, event: 'TreeEvent'):
        image_item: 'TreeItemId' = event.GetOldItem()
        if image_item.IsOk() and not self.first_choice:
            image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(image_item)
            if isinstance(image_data, ImageItem):
                settings = self.settings.all
                image_data.settings = settings
                image_data.unselect()
        elif self.deleted_item:
            self.deleted_item = False
        # else:
        #     self.apply_settings_to_all()
        if self.first_choice:
            self.first_choice = False

        if not event.GetItem().IsOk():
            self.image_item = None
            self.controls.clear_preview()
            return
        image_data = self.tree_manager.selected_item_data
        if isinstance(image_data, ImageItem):
            self.image_item = image_data
            image_data.selected = True
            self.controls.imported_image_id = 0
            self.controls.previous_proc_mode = image_data.settings.proc_mode
            self.controls.gen_image_info(image_data)
            if image_data.settings.proc_mode == constants.DECRYPTION_MODE and image_data.encrypted_image:
                image_data.cache.encryption_data.backtrack_interface()
            else:
                image_data.settings.backtrack_interface()
            self.processingOptions.Enable()

            if self.previewMode.Selection == constants.AUTO_REFRESH:
                self.refresh_preview(event)
        elif isinstance(image_data, FolderItem):
            self.image_item = None
            self.controls.gen_image_info()
            self.processingOptions.Disable()
            self.controls.clear_preview()
        else:
            self.controls.gen_image_info()

    def del_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.deleted_item = True
            self.tree_manager.del_item(self.imageTreeCtrl.Selection)
        if not self.tree_manager.file_dict:
            self.controls.gen_image_info()

    def reload_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.stop_reloading_func.call()
            if self.tree_manager.reloading_thread.is_alive:
                return
            self.tree_manager.reload_item(self.imageTreeCtrl.Selection)

    def tree_key_down(self, event: 'TreeEvent'):
        match event.GetKeyCode():
            case constants.WXK_DELETE:
                self.del_item(event)

    def set_settings_as_default(self, event=None):
        self.settings.default = self.settings.all

    def stop_loading_event(self, event):
        self.stop_loading_func.call()

    def check_saving_format(self, event):
        self.controls.saving_format = self.controls.saving_format.lower()
        if self.controls.saving_format in constants.EXTENSION_KEYS:
            self.record_saving_format()
        else:
            self.dialog.async_warning('不支持的格式: {}, 仅支持以下格式: \n{}'.format(self.controls.saving_format, constants.EXTENSION_KEYS_STRING), '保存格式错误')
            self.controls.saving_format = self.controls.previous_saving_format

    def record_saving_format(self, event=None):
        self.controls.previous_saving_format = self.controls.saving_format

    def stop_saving_event(self, event):
        self.image_saver.cancel()
        self.dialog.info('已取消尚未进行的任务')
        self.stopSavingBtn.Disable()

    def apply_to_all(self, event):
        self.apply_settings_to_all()

    def revert_to_default(self, event):
        if self.image_item is None:
            return
        self.image_item.settings = self.settings.default.copy()
        self.image_item.settings.backtrack_interface()
        self.refresh_preview()

    def toggle_factor_slider_switch(self, event: 'CommandEvent'):
        self.noiseFactor.Enable(event.IsChecked())
        self.refresh_preview(event)

    def toggle_xor_panel_switch(self, event: 'CommandEvent'):
        self.xorPanel.Enable(event.IsChecked())
        self.refresh_preview(event)

    def update_noise_factor_num(self, event: 'CommandEvent' = None):
        self.controls.noise_factor_info = str(self.controls.noise_factor)

    def update_quality_num(self, event: 'CommandEvent' = None):
        self.controls.saving_quality_info = str(self.controls.saving_quality)

    def update_subsampling_num(self, event: 'CommandEvent' = None):
        self.controls.saving_subsampling_info = str(self.controls.saving_subsampling_level)

    def change_redundant_cache_length(self, event: 'SpinEvent'):
        self.startup_parameters.maximum_redundant_cache_length = event.Int

    def toggle_low_memory_usage_mode(self, event: 'CommandEvent'):
        self.startup_parameters.low_memory = event.IsChecked()

    def toggle_disable_cache(self, event: 'CommandEvent'):
        self.startup_parameters.disable_cache = event.IsChecked()

    def exit(self, event):
        self.logger.info('窗口退出')
        self.Destroy()
