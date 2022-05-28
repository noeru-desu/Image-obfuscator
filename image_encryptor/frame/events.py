"""
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2022-05-28 20:07:01
Description  : 事件处理
"""
from typing import TYPE_CHECKING, Optional

from PIL.ImageGrab import grabclipboard

from image_encryptor.constants import DO_NOT_REFRESH, AUTO_REFRESH, EXTENSION_KEYS, EXTENSION_KEYS_STRING
from image_encryptor.frame.file_item import FolderItem, ImageItem
from image_encryptor.frame.main_frame import MainFrame as BasicMainFrame
from image_encryptor.modules.decorator import catch_exc_for_frame_method

if TYPE_CHECKING:
    from wx import CommandEvent, Event, SizeEvent, SpinEvent, TreeEvent, TreeItemId
    from image_encryptor.modules.argparse import Parameters


class MainFrame(BasicMainFrame):
    __slots__ = ('deleted_item', 'resized', 'first_choice')

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
        if self.controller.preview_mode != DO_NOT_REFRESH:
            self.force_refresh_preview()

    @catch_exc_for_frame_method
    def refresh_preview(self, event: Optional['Event'] = None):
        """刷新预览图

        Args:
            event (Event, optional): 事件实例. 默认为`None`. 为None时将忽略`preview_mode`设置, 强制刷新,
            `refresh_preview`与`force_refresh_preview`的不同之处是, 前者不会忽略图像缓存, 而后者会忽略图像缓存并重新生成预览图
        """
        if self.image_item is None:
            return
        if event is not None and self.controller.preview_mode != AUTO_REFRESH:
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
    def update_password_dict(self, event: Optional['Event'] = None):
        """更新密码字典

        Args:
            event (Event, optional): 事件实例. 默认为`None`. 为`None`时不刷新预览图.

        Returns:
            bool: 是否更新成功
        """
        if self.controller.password == '':
            return False
        if event is not None:
            self.refresh_preview(event)
        if self.controller.password != 'none' and self.controller.password not in self.password_dict.values():
            if self.add_password_dict(self.controller.password):
                return True
            self.controller.password = ''
            return False
        return True

    @catch_exc_for_frame_method
    def save_selected_image(self, event):
        self.dialog.warning('保存功能尚未完成', '正在进行重构')
        return
        self.image_saver.save_selected_image()

    @catch_exc_for_frame_method
    def bulk_save(self, event):
        self.dialog.warning('批量保存功能尚未完成', '正在进行重构')
        return
        self.image_saver.bulk_save()

    @catch_exc_for_frame_method
    def processing_mode_change(self, event):
        selected_mode = self.controller.proc_mode_interface
        if self.image_item is None and selected_mode.decryption_mode:
            self.controller.proc_mode_interface = self.controller.previous_proc_mode
            return
        elif selected_mode.requires_encryption_parameters:
            self.image_item.display_encryption_parameters()
            if self.image_item.cache.loading_encryption_attributes_error is not None:
                self.controller.proc_mode_interface = self.controller.previous_proc_mode
                self.dialog.async_warning(self.image_item.cache.loading_encryption_attributes_error)
                return
        else:
            self.controller.proc_settings_panel = selected_mode.settings_panel
            self.controller.frame.procSettingsPanelContainer.Enable(selected_mode.enable_settings_panel)
            self.controller.frame.passwordCtrl.Enable(selected_mode.enable_password)
        self.controller.previous_proc_mode = self.controller.proc_mode_interface
        self.refresh_preview(event)

    @catch_exc_for_frame_method
    def preview_mode_change(self, event):
        if self.controller.preview_mode == DO_NOT_REFRESH:
            self.previewedBitmap.Show(False)
        else:
            self.previewedBitmap.Show(True)
            self.refresh_preview(event)

    def switching_image(self, event: 'TreeEvent'):
        if self.image_loader.loading_thread.in_execution:
            event.Veto()

    @catch_exc_for_frame_method
    def switched_image(self, event: 'TreeEvent'):
        image_item: 'TreeItemId' = event.GetOldItem()
        if image_item.IsOk() and not self.first_choice:
            image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(image_item)
            if isinstance(image_data, ImageItem):
                image_data.proc_mode = self.controller.proc_mode_interface
                image_data.settings = image_data.proc_mode.instantiate_settings_cls(self.controller)
                image_data.unselect()
        elif self.deleted_item:
            self.deleted_item = False
        # else:
        #     self.apply_settings_to_all()
        if self.first_choice:
            self.first_choice = False

        if not event.GetItem().IsOk():
            self.image_item = None
            self.controller.clear_preview()
            return
        image_data = self.tree_manager.selected_item_data
        if isinstance(image_data, ImageItem):
            self.image_item = image_data
            image_data.selected = True
            self.controller.imported_image_id = 0
            self.controller.previous_proc_mode = image_data.proc_mode
            self.controller.gen_image_info(image_data)
            self.processingOptions.Enable()
            self.controller.proc_settings_panel = image_data.proc_mode.settings_panel
            if image_data.encrypted_image and image_data.encryption_parameters.decryption_mode.mode_id == image_data.proc_mode.mode_id:
                self.controller.backtrack_interface(image_data.encryption_parameters)
            else:
                self.controller.backtrack_interface(image_data.settings)

            if self.previewMode.Selection == AUTO_REFRESH:
                self.refresh_preview(event)
        elif isinstance(image_data, FolderItem):
            self.image_item = None
            self.controller.gen_image_info()
            self.processingOptions.Disable()
            self.controller.clear_preview()
        else:
            self.controller.gen_image_info()

    @catch_exc_for_frame_method
    def del_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.deleted_item = True
            self.tree_manager.del_item(self.imageTreeCtrl.Selection)
        if not self.tree_manager.file_dict:
            self.controller.gen_image_info()

    @catch_exc_for_frame_method
    def reload_item(self, event):
        if self.imageTreeCtrl.Selection.IsOk():
            self.stop_reloading_func.call()
            if self.stop_reloading_func._num == 0:
                self.tree_manager.reload_item(self.imageTreeCtrl.Selection)

    '''
    def tree_key_down(self, event: 'TreeEvent'):
        match event.GetKeyCode():
            case constants.WXK_DELETE:
                self.del_item(event)
    '''

    @catch_exc_for_frame_method
    def set_settings_as_default(self, event=None):
        self.mode_manager.default_mode = self.controller.proc_mode_interface
        self.settings.default = self.settings.all

    @catch_exc_for_frame_method
    def stop_loading_event(self, event):
        self.stop_loading_func.call()

    @catch_exc_for_frame_method
    def check_saving_format(self, event):
        self.controller.saving_format = self.controller.saving_format.lower()
        if self.controller.saving_format in EXTENSION_KEYS:
            self.record_saving_format()
        else:
            self.dialog.async_warning('不支持的格式: {}, 仅支持以下格式: \n{}'.format(self.controller.saving_format, EXTENSION_KEYS_STRING), '保存格式错误')
            self.controller.saving_format = self.controller.previous_saving_format

    @catch_exc_for_frame_method
    def record_saving_format(self, event=None):
        self.controller.previous_saving_format = self.controller.saving_format

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
        self.controller.proc_mode = self.mode_manager.default_mode
        self.image_item.settings = self.settings.default.copy()
        self.image_item.settings.backtrack_interface()
        self.refresh_preview()

    def expand_all_item(self, event):
        self.imageTreeCtrl.ExpandAll()

    def collapse_all_item(self, event):
        self.imageTreeCtrl.CollapseAll()
        if self.imageTreeCtrl.Selection.IsOk() and isinstance(self.tree_manager.selected_item_data, FolderItem):
            self.image_item = None
            self.controller.gen_image_info()
            self.processingOptions.Disable()
            self.controller.clear_preview()

    def update_quality_num(self, event: 'CommandEvent' = None):
        self.controller.saving_quality_info = str(self.controller.saving_quality)

    def update_subsampling_num(self, event: 'CommandEvent' = None):
        self.controller.saving_subsampling_info = str(self.controller.saving_subsampling_level)

    def change_redundant_cache_length(self, event: 'SpinEvent'):
        self.startup_parameters.maximum_redundant_cache_length = event.Int

    def toggle_low_memory_usage_mode(self, event: 'CommandEvent'):
        self.startup_parameters.low_memory = event.IsChecked()

    def toggle_disable_cache(self, event: 'CommandEvent'):
        self.startup_parameters.disable_cache = event.IsChecked()

    def exit(self, event):
        self.logger.info('窗口退出')
        self.Destroy()
