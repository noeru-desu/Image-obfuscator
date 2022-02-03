'''
Author       : noeru_desu
Date         : 2022-01-27 14:22:10
LastEditors  : noeru_desu
LastEditTime : 2022-02-03 20:30:59
Description  : 事件处理覆写
'''
from typing import TYPE_CHECKING

from wx import (DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, ID_OK, DirDialog,
                FileDialog)

from image_encryptor.constants import ANTY_HARMONY_MODE, DO_NOT_REFRESH, AUTO_REFRESH, DECRYPTION_MODE, ENCRYPTION_MODE, EXTENSION_KEYS
from image_encryptor.gui.frame.main_frame import MainFrame as BasicMainFrame
from image_encryptor.gui.frame.tree_manager import FolderItem, ImageItem

if TYPE_CHECKING:
    from wx import CommandEvent, TreeEvent, TreeItemId, SizeEvent


class MainFrame(BasicMainFrame):
    def __init__(self, parent, run_path=...):
        super().__init__(parent, run_path)
        self.deleted_item = False
        self.resized = False

    def on_move_end(self, event):
        if self.resized:
            self.refresh_preview(event)
            self.resized = False
        event.Skip()

    def on_size(self, event: 'SizeEvent'):
        self.resized = True
        event.Skip()

    def manual_refresh(self, event):
        if self.controls.preview_mode == DO_NOT_REFRESH:
            return
        self.refresh_preview()

    def refresh_preview(self, event=None):
        if self.image_item is None:
            return
        if event is not None and self.controls.preview_mode != AUTO_REFRESH:
            return
        size_changed = self.controls.regen_initial_preview()
        if size_changed or self.settings.encryption_settings_md5 != self.image_item.encryption_settings_md5:
            self.image_generator.generate_preview()
        elif self.image_item.processed_preview is not None:
            self.controls.regen_processed_preview(self.image_item.processed_preview)

    def force_refresh_preview(self, event):
        if self.image_item is None:
            return
        self.controls.regen_initial_preview(True)
        self.image_generator.generate_preview()

    def load_file(self, event):
        with FileDialog(self, "选择图像", style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST) as dialog:
            if ID_OK == dialog.ShowModal():
                self.image_loader.load(dialog.GetPath())

    def load_dir(self, event):
        with DirDialog(self, "选择文件夹", style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST) as dialog:
            if ID_OK == dialog.ShowModal():
                self.image_loader.load(dialog.GetPath())

    def update_password_dict(self, event=None):
        """更新成功则返回True"""
        if self.controls.password == '':
            return False
        if event is not None:
            self.refresh_preview(event)
        if self.controls.password != 'none' and self.controls.password not in self.password_dict.values():
            try:
                password_base64 = self.password_dict.get_validation_field_base64(self.controls.password)
            except ValueError:
                self.dialog.async_error('密码长度超过AES加密限制，请确保密码长度不超过32字节', '用于验证密码正确性的字符串生成时出现错误')
                self.controls.password = ''
                return False
            else:
                self.password_dict[password_base64] = self.controls.password
                self.logger.info(f'更新密码字典[{password_base64}: {self.controls.password}](当前字典长度: {len(self.password_dict)})')
                return True
        return True

    def save_selected_image(self, event):
        self.image_saver.save_selected_image()

    def bulk_save(self, event):
        self.image_saver.bulk_save()

    def processing_mode_change(self, event):
        if self.image_item is None:
            return
        if self.controls.proc_mode != DECRYPTION_MODE:
            if self.controls.proc_mode == ANTY_HARMONY_MODE:
                self.controls.frame.processingSettingsPanel1.Disable()
                self.controls.frame.passwordCtrl.Disable()
            else:
                self.controls.frame.processingSettingsPanel1.Enable()
                self.controls.frame.passwordCtrl.Enable()
        else:
            self.image_item.check_encryption_parameters()
            if self.image_item.loading_image_data_error is not None:
                if self.image_item.settings.proc_mode != DECRYPTION_MODE:
                    self.controls.proc_mode = self.image_item.settings.proc_mode
                elif self.settings.default.proc_mode != DECRYPTION_MODE:
                    self.controls.proc_mode = self.settings.default.proc_mode
                else:
                    self.controls.proc_mode = ENCRYPTION_MODE
                self.dialog.async_warning(self.image_item.loading_image_data_error)
        self.refresh_preview(event)

    def preview_mode_change(self, event):
        if self.controls.preview_mode == DO_NOT_REFRESH:
            self.previewedBitmap.Show(False)
        else:
            self.previewedBitmap.Show(True)
            self.refresh_preview(event)

    def switch_image(self, event: 'TreeEvent'):
        image_item: 'TreeItemId' = event.GetOldItem()
        if image_item.IsOk():
            image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(image_item)
            if isinstance(image_data, ImageItem):
                settings = self.settings.all
                image_data.settings = settings
        elif self.deleted_item:
            self.deleted_item = False
        else:
            self.apply_settings_to_all()

        if not event.GetItem().IsOk():
            self.image_item = None
            self.controls.clear_preview()
            return
        image_data = self.tree_manager.selected_item_data
        if isinstance(image_data, ImageItem):
            self.image_item = image_data
            if image_data.settings.proc_mode == DECRYPTION_MODE and image_data.encrypted_image:
                image_data.encryption_data.backtrack_interface()
            else:
                image_data.settings.backtrack_interface()
            self.processingOptions.Enable()

            if self.previewMode.Selection == AUTO_REFRESH:
                self.refresh_preview(event)
            elif self.image_item.processed_preview is not None:
                self.controls.regen_processed_preview(self.image_item.processed_preview, True)
            if self.previewMode.Selection != AUTO_REFRESH:
                self.controls.regen_initial_preview()
        elif isinstance(image_data, FolderItem):
            self.image_item = None
            self.processingOptions.Disable()
            self.controls.clear_preview()

    def del_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.deleted_item = True
            self.tree_manager.del_item(self.imageTreeCtrl.Selection)

    def reload_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.stop_reloading_func.call()
            if self.tree_manager.reloading_thread.is_running:
                return
            self.tree_manager.reload_item(self.imageTreeCtrl.Selection)

    def set_settings_as_default(self, event=None):
        self.settings.default = self.settings.all

    def stop_loading_event(self, event):
        self.stop_loading_func.call()

    def check_saving_format(self, event):
        self.controls.saving_format = self.controls.saving_format.lower()
        if self.controls.saving_format in EXTENSION_KEYS:
            self.record_saving_format()
        else:
            self.dialog.async_warning('不支持的格式: {}，仅支持以下格式: \n{}'.format(self.controls.saving_format, '; '.join(i for i in EXTENSION_KEYS)), '保存格式错误')
            self.controls.saving_format = self.controls.previous_saving_format

    def record_saving_format(self, event=None):
        self.controls.previous_saving_format = self.controls.saving_format

    def stop_saving_event(self, event):
        self.image_saver.cancel()
        self.dialog.info('已取消尚未进行的任务')
        self.stopSavingBtn.Disable()

    def apply_to_all(self, event):
        self.apply_settings_to_all()

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

    def exit(self, event):
        self.logger.info('窗口退出')
        self.Destroy()
        exit()
