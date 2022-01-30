'''
Author       : noeru_desu
Date         : 2022-01-27 14:22:10
LastEditors  : noeru_desu
LastEditTime : 2022-01-30 17:13:56
Description  : 事件处理覆写
'''
from typing import TYPE_CHECKING

from wx import (DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, ID_OK, DirDialog,
                FileDialog)

from image_encryptor.constants import DO_NOT_REFRESH, AUTO_REFRESH, DECRYPTION_MODE, ENCRYPTION_MODE
from image_encryptor.gui.frame.main_frame import MainFrame as BasicMainFrame

if TYPE_CHECKING:
    from wx import CommandEvent, TreeEvent, TreeItemId, SizeEvent

    from image_encryptor.gui.frame.tree_manager import ImageItem


class MainFrame(BasicMainFrame):
    def __init__(self, parent, run_path=...):
        super().__init__(parent, run_path)
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
        if event is not None and self.controls.preview_mode != AUTO_REFRESH:  # 2为自动刷新
            return
        size_changed = self.controls.regen_initial_preview()
        if size_changed or self.settings.encryption_settings_md5 != self.image_item.encryption_settings_md5:
            self.image_generator.generate_preview()
        elif self.image_item.processed_preview is not None:
            self.controls.regen_processed_preview(self.image_item.processed_preview)

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
            password_base64 = self.password_dict.get_validation_field_base64(self.controls.password)
            self.password_dict[password_base64] = self.controls.password
            self.logger.info(f'更新密码字典[{password_base64}: {self.controls.password}](当前字典长度: {len(self.password_dict)})')
        return True

    def save_selected_image(self, event):
        self.image_saver.save_selected_image()

    def bulk_save(self, event):
        self.image_saver.bulk_save()

    def processing_mode_change(self, event):
        if self.image_item is None:
            return
        if self.controls.proc_mode != DECRYPTION_MODE:
            self.processingSettingsPanel1.Enable()
            self.passwordCtrl.Enable()
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
        # TODO
        image_item: 'TreeItemId' = event.GetOldItem()
        if image_item.IsOk():
            image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(image_item)
            if image_data is not None:
                settings = self.settings.all
                '''if settings.proc_mode != image_data.settings.proc_mode:
                    image_data.manual_switch_mode = True'''
                image_data.settings = settings
        else:
            self.apply_settings_to_all()

        image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(event.GetItem())
        if image_data is not None:
            self.image_item = image_data
            if image_data.settings.proc_mode == DECRYPTION_MODE and image_data.encrypted_image:
                image_data.encryption_data.backtrack_interface()
            else:
                image_data.settings.backtrack_interface()

            if self.previewMode.Selection == AUTO_REFRESH:
                self.refresh_preview(event)
            elif self.image_item.processed_preview is not None:
                self.controls.regen_processed_preview(self.image_item.processed_preview, True)
            if self.previewMode.Selection != AUTO_REFRESH:
                self.controls.regen_initial_preview()

    def set_settings_as_default(self, event=None):
        self.settings.default = self.settings.all

    def stop_loading_event(self, event):
        self.stop_loading_func.call()

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
