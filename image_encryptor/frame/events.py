"""
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2022-05-02 16:18:33
Description  : 事件处理
"""
from typing import TYPE_CHECKING

from PIL.ImageGrab import grabclipboard

from image_encryptor import constants
from image_encryptor.frame.file_item import FolderItem, ImageItem
from image_encryptor.frame.main_frame import MainFrame as BasicMainFrame
from image_encryptor.utils.misc_utils import catch_exc_for_frame_method

if TYPE_CHECKING:
    from wx import CommandEvent, SizeEvent, SpinEvent, TreeEvent, TreeItemId
    from image_encryptor.modules.argparse import Parameters


class MainFrame(BasicMainFrame):
    __slots__ = ('deleted_item', 'resized', 'first_choice')

    @catch_exc_for_frame_method
    def __init__(self, parent, startup_parameters: 'Parameters', run_path: str = ...):
        super().__init__(parent, startup_parameters, run_path)
        self.deleted_item = False
        self.resized = False
        self.first_choice = True

    def on_move_end(self, event):
        if self.resized:
            self.refresh_preview(event)
            self.resized = False

    def on_size(self, event: 'SizeEvent'):
        self.resized = True
        event.Skip()

    @catch_exc_for_frame_method
    def manually_refresh(self, event):
        if self.controls.preview_mode != constants.DO_NOT_REFRESH:
            self.force_refresh_preview()

    @catch_exc_for_frame_method
    def refresh_preview(self, event=None):
        if self.image_item is None:
            return
        if event is not None and self.controls.preview_mode != constants.AUTO_REFRESH:
            return
        self.image_item.display_initial_preview()
        self.image_item.display_processed_preview()

    @catch_exc_for_frame_method
    def force_refresh_preview(self, event=None):
        if self.image_item is None:
            return
        self.image_item.display_initial_preview(False)
        self.image_item.display_processed_preview(False)

    @catch_exc_for_frame_method
    def load_file(self, event):
        path = self.dialog.select_file('选择图像')
        if path is not None:
            self.image_loader.load(path)

    @catch_exc_for_frame_method
    def load_dir(self, event):
        path = self.dialog.select_dir('选择文件夹')
        if path is not None:
            self.image_loader.load(path)

    @catch_exc_for_frame_method
    def load_image_from_clipboard(self, event):
        clipboard = grabclipboard()
        if clipboard is None:
            self.dialog.async_warning('没有从剪切板导入任何图像')
        else:
            self.image_loader.load(clipboard)

    @catch_exc_for_frame_method
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

    @catch_exc_for_frame_method
    def save_selected_image(self, event):
        self.image_saver.save_selected_image()

    @catch_exc_for_frame_method
    def bulk_save(self, event):
        self.image_saver.bulk_save()

    @catch_exc_for_frame_method
    def processing_mode_change(self, event):
        if self.image_item is None and self.controls.proc_mode == constants.DECRYPTION_MODE:
            self.controls.proc_mode = self.controls.previous_proc_mode
            return
        elif self.controls.proc_mode != constants.DECRYPTION_MODE:
            if self.controls.proc_mode == constants.ANTY_HARMONY_MODE:
                self.controls.frame.processingSettingsPanel.Disable()
                self.controls.frame.passwordCtrl.Disable()
            else:
                self.controls.frame.processingSettingsPanel.Enable()
                self.controls.frame.passwordCtrl.Enable()
        else:
            self.image_item.display_encryption_parameters()
            if self.image_item.cache.loading_encryption_attributes_error is not None:
                self.controls.proc_mode = self.controls.previous_proc_mode
                self.dialog.async_warning(self.image_item.cache.loading_encryption_attributes_error)
                return
        self.controls.previous_proc_mode = self.controls.proc_mode
        self.refresh_preview(event)

    @catch_exc_for_frame_method
    def preview_mode_change(self, event):
        if self.controls.preview_mode == constants.DO_NOT_REFRESH:
            self.previewedBitmap.Show(False)
        else:
            self.previewedBitmap.Show(True)
            self.refresh_preview(event)

    @catch_exc_for_frame_method
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
                image_data.cache.encryption_parameters.backtrack_interface()
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

    @catch_exc_for_frame_method
    def del_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.deleted_item = True
            self.tree_manager.del_item(self.imageTreeCtrl.Selection)
        if not self.tree_manager.file_dict:
            self.controls.gen_image_info()

    @catch_exc_for_frame_method
    def reload_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.stop_reloading_func.call()
            if self.tree_manager.reloading_thread.is_alive:
                return
            self.tree_manager.reload_item(self.imageTreeCtrl.Selection)

    '''
    def tree_key_down(self, event: 'TreeEvent'):
        match event.GetKeyCode():
            case constants.WXK_DELETE:
                self.del_item(event)
    '''

    @catch_exc_for_frame_method
    def set_settings_as_default(self, event=None):
        self.settings.default = self.settings.all

    @catch_exc_for_frame_method
    def stop_loading_event(self, event):
        self.stop_loading_func.call()

    @catch_exc_for_frame_method
    def check_saving_format(self, event):
        self.controls.saving_format = self.controls.saving_format.lower()
        if self.controls.saving_format in constants.EXTENSION_KEYS:
            self.record_saving_format()
        else:
            self.dialog.async_warning('不支持的格式: {}, 仅支持以下格式: \n{}'.format(self.controls.saving_format, constants.EXTENSION_KEYS_STRING), '保存格式错误')
            self.controls.saving_format = self.controls.previous_saving_format

    @catch_exc_for_frame_method
    def record_saving_format(self, event=None):
        self.controls.previous_saving_format = self.controls.saving_format

    @catch_exc_for_frame_method
    def stop_saving_event(self, event):
        self.image_saver.cancel()
        self.dialog.info('已取消尚未进行的任务')
        self.stopSavingBtn.Disable()

    @catch_exc_for_frame_method
    def apply_to_all(self, event):
        self.apply_settings_to_all()

    @catch_exc_for_frame_method
    def revert_to_default(self, event):
        if self.image_item is None:
            return
        self.image_item.settings = self.settings.default.copy()
        self.image_item.settings.backtrack_interface()
        self.refresh_preview()

    def expand_all_item(self, event):
        self.imageTreeCtrl.ExpandAll()

    def collapse_all_item(self, event):
        self.imageTreeCtrl.CollapseAll()
        if self.imageTreeCtrl.Selection.IsOk() and isinstance(self.tree_manager.selected_item_data, FolderItem):
            self.image_item = None
            self.controls.gen_image_info()
            self.processingOptions.Disable()
            self.controls.clear_preview()

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
