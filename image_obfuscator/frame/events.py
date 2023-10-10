"""
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2023-02-03 17:25:53
"""
from base64 import b85encode
from os import listdir, startfile
from os.path import isdir, sep
from pickle import dumps as pickle_dumps, HIGHEST_PROTOCOL
from typing import TYPE_CHECKING, Optional, Union

from PIL.ImageGrab import grabclipboard
from wx import VERTICAL, YES_NO, ID_YES, CallAfter

from image_obfuscator.constants import DO_NOT_REFRESH, AUTO_REFRESH, EXTENSION_KEYS, EXTENSION_KEYS_STRING, LOSSY_FORMATS, LOCAL_APPDATA_TEMP
from image_obfuscator.frame.file_item import FolderItem, ImageItem, ImageItemCache, PreviewCache
from image_obfuscator.frame.main_frame import MainFrame as BasicMainFrame
from image_obfuscator.modes.mirage_tank.settings import Settings as MirageTankSettings
from image_obfuscator.modules.decorator import catch_exc_for_frame_method
from image_obfuscator.modules.version_adapter import gen_encryption_attributes

if TYPE_CHECKING:
    from wx import CommandEvent, Event, SizeEvent, SpinEvent, TreeEvent, TreeItemId, RadioBox, Object


class MainFrame(BasicMainFrame):
    __slots__ = ('deleted_item', 'resized', 'first_choice')

    def __init__(self, parent, run_path: str = ...):
        super().__init__(parent, run_path)
        self.deleted_item = False
        self.resized = False
        self.first_choice = True

    def on_move_end(self, event):
        if self.resized:
            if self.program_options.final_layout_widgets:
                self.Layout()
            if self.image_item is not None and self.controller.preview_layout == 2 and self.controller.displayed_preview == 2:
                self.set_preview_layout(self.image_item.best_layout)
            else:
                self.set_preview_plane_size()
            self.refresh_preview(event)
            self.resized = False

    def on_maximize(self, event):
        CallAfter(self._after_maximize, event)

    def _after_maximize(self, event):
        if self.image_item is not None:
            if self.controller.preview_layout == 2 and self.controller.displayed_preview == 2:
                self.set_preview_layout(self.image_item.best_layout)
            else:
                self.set_preview_plane_size()
        self.refresh_preview(event)

    def on_size(self, event: 'SizeEvent'):
        self.resized = True
        if not self.program_options.final_layout_widgets:
            event.Skip()

    def change_displayed_preview(self, event: Union['CommandEvent', 'RadioBox']):
        match event.Selection:
            case 0:
                self.importedBitmapPanel.Show()
                self.previewedBitmapPanel.Hide()
                self.set_preview_plane_size()
            case 1:
                self.importedBitmapPanel.Hide()
                self.previewedBitmapPanel.Show()
                self.set_preview_plane_size()
            case 2:
                self.importedBitmapPanel.Show()
                self.previewedBitmapPanel.Show()
                if self.image_item is not None and self.controller.preview_layout == 2:
                    self.set_preview_layout(self.image_item.best_layout)
                else:
                    self.set_preview_plane_size()
        self.refresh_preview(event)

    def change_preview_layout(self, event):
        if self.controller.preview_layout == 2 and self.controller.displayed_preview == 2:
            if self.image_item is not None:
                self.set_preview_layout(self.image_item.best_layout)
            else:
                self.set_preview_layout(VERTICAL)
        elif self.controller.displayed_preview != 2:
            return
        else:
            self.set_preview_layout(self.controller.preview_layout_flag)
        self.refresh_preview(event)

    @catch_exc_for_frame_method
    def manually_refresh(self, event):
        if self.controller.preview_mode != DO_NOT_REFRESH:
            self.force_refresh_preview()

    @catch_exc_for_frame_method
    def settings_changed(self, event: 'Event'):
        if self.image_item is None:
            self.controller.proc_mode_interface.default_settings.sync_from_event(event)
            return
        if self.image_item.proc_mode.settings_cls is not None:
            self.image_item.settings.sync_from_event(event)
        self.refresh_preview(event)

    @catch_exc_for_frame_method
    def sync_setting(self, obj: Union['Object', int], _refresh_preview=True):
        if self.image_item is None:
            self.controller.proc_mode_interface.default_settings.sync_from_object(obj)
            return
        if self.image_item.proc_mode.settings_cls is not None:
            self.image_item.settings.sync_from_object(obj)
        if _refresh_preview:
            self.refresh_preview(...)

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
            self.dialog.async_warning('剪切板中没有图像文件路径或图像数据', '无法载入')
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
        if self.controller.password != 'none' and self.controller.password not in self.password_dict.values():
            if self.add_password_dict(self.controller.password):
                if event is not None:
                    self.settings_changed(event)
                return True
            self.controller.password = ''
            return False
        if event is not None:
            self.settings_changed(event)
        return True

    @catch_exc_for_frame_method
    def save_selected_image(self, event):
        if self.image_item is not None:
            self.image_saver.save_selected_image()
            return
        elif self.folder_item is not None:
            self.image_saver.save_selected_folder()
            return
        self.dialog.async_error('没有选择图像或文件夹')

    @catch_exc_for_frame_method
    def bulk_save(self, event):
        if not self.tree_manager.file_dict:
            self.dialog.async_error('没有载入图像')
            return
        self.image_saver.bulk_save()

    @catch_exc_for_frame_method
    def processing_mode_changed(self, event: 'CommandEvent' = ...):
        selected_mode = self.controller.proc_mode_interface
        if self.image_item is None:
            if not selected_mode.can_be_set_as_default_mode:    # 当所选模式不能被设置为默认模式时回退
                self.controller.proc_mode_interface = self.controller.previous_proc_mode
                self.mode_fallback_dialog.open_dialog()
                return
            self.controller.previous_proc_mode = self.mode_manager.default_mode = selected_mode
            self.controller.backtrack_interface(selected_mode.default_settings, selected_mode)
            return
        self.image_item.enable_available_settings_source_btn(selected_mode)
        if selected_mode.requires_encryption_parameters:    # 如果所选模式需要加密参数
            if self.image_item.is_correct_decryption_mode(selected_mode):   # 如果所选图像已有正确对应的加密参数，则直接显示
                self.image_item.proc_mode = selected_mode
                self.controller.previous_proc_mode = selected_mode
                if not self.image_item.cache.encryption_attributes_from_file:
                    self.controller.set_settings_source(2)
                self.image_item.display_encryption_attributes()
                self.refresh_preview(event)
                return
            elif not selected_mode.encryption_parameters_must_be_used:  # 如果所选模式可以使用设置面板手动指定加密参数
                pass
            elif self.image_item.cache.loading_encryption_attributes_error is not None:
                self.controller.proc_mode_interface = self.controller.previous_proc_mode
                self.dialog.async_warning(self.image_item.cache.loading_encryption_attributes_error)
                return
            else:
                self.controller.proc_mode_interface = self.controller.previous_proc_mode
                self.dialog.async_warning('此模式无法解密选中的图像')
                return
        self.image_item.proc_mode = selected_mode
        self.controller.backtrack_interface(self.image_item.settings, selected_mode)
        self.controller.previous_proc_mode = selected_mode
        self.refresh_preview(event)

    @catch_exc_for_frame_method
    def settings_source_changed(self, event: 'CommandEvent'):
        if self.image_item is None:
            if __debug__:
                raise ValueError()
            return
        match event.GetSelection():
            case 0:
                self.controller.settings_source_selected(0)
                self.controller.backtrack_interface(self.image_item.settings)
            case 1:
                if self.image_item.is_correct_decryption_mode(self.controller.proc_mode_interface):
                    self.image_item.settings_source = 1
                    self.image_item.display_encryption_attributes()
                else:
                    self.controller.set_settings_source(self.image_item.settings_source, False)
            case 2:
                if not self.image_item.encrypted_image:
                    flag = self.dialog.encryption_attributes_b85_entry_dialog()
                    if flag is None or not flag:
                        self.controller.set_settings_source(self.image_item.settings_source, False)
                        return
                self.controller.settings_source_selected(2)
                self.image_item.display_encryption_attributes()
        self.refresh_preview(event)

    @catch_exc_for_frame_method
    def preview_mode_change(self, event):
        if self.controller.preview_mode == DO_NOT_REFRESH:
            self.previewedBitmap.Show(False)
        else:
            self.previewedBitmap.Show(True)
            self.refresh_preview(event)

    def switching_image(self, event: 'TreeEvent'):
        if self.image_loader.loading_thread.in_execution or self.disable_switching_image:
            event.Veto()

    @catch_exc_for_frame_method
    def switched_image(self, event: 'TreeEvent'):
        image_item: 'TreeItemId' = event.GetOldItem()
        if image_item.IsOk() and not self.first_choice:
            image_data: 'ImageItem' = self.imageTreeCtrl.GetItemData(image_item)
            if isinstance(image_data, ImageItem):
                image_data.unselect()
        elif self.deleted_item:
            self.deleted_item = False
        if self.first_choice:
            self.first_choice = False

        self.image_item = None
        self.folder_item = None

        if not event.GetItem().IsOk():
            self.controller.clear_preview()
            return
        image_data = self.tree_manager.selected_item_data
        if isinstance(image_data, ImageItem):
            self.image_item = image_data
            image_data.on_select()
            self.controller.imported_image_id = 0
            self.controller.previous_proc_mode = image_data.proc_mode
            self.controller.gen_image_info(image_data)
            self.processingOptions.Enable()
            image_data.enable_available_settings_source_btn(sync_to_item=False)
            match image_data.settings_source:
                case 0:
                    self.controller.backtrack_interface(image_data.settings)
                case _:
                    self.controller.backtrack_interface(image_data.encryption_attributes.settings)

            if self.controller.preview_layout == 2 and self.controller.displayed_preview == 2:
                self.set_preview_layout(image_data.best_layout)
            if self.previewMode.Selection == AUTO_REFRESH:
                self.refresh_preview(event)
        elif isinstance(image_data, FolderItem):
            self.folder_item = image_data
            self.controller.gen_image_info()
            self.processingOptions.Disable()
            self.controller.clear_preview()
        else:
            self.saveProgressPanel.Disable()
            self.controller.gen_image_info()

    @catch_exc_for_frame_method
    def del_item(self, event):
        selection = self.imageTreeCtrl.Selection
        if selection.IsOk():
            self.deleted_item = True
            self.tree_manager.del_item(selection)
        if not self.tree_manager.file_dict:
            self.controller.gen_image_info()
            self.processingOptions.Enable()

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
        proc_mode = self.controller.proc_mode_interface
        if not proc_mode.can_be_set_as_default_mode:
            self.dialog.warning('当前模式不允许被设定为默认模式')
            return
        if self.image_item is not None:
            self.mode_manager.default_mode = self.image_item.proc_mode
            self.mode_manager.default_settings = self.image_item.settings.copy()

    @catch_exc_for_frame_method
    def stop_loading_event(self, event):
        self.stop_loading_func.call()

    @catch_exc_for_frame_method
    def check_save_format(self, event):
        self.controller.save_format = self.controller.save_format.lower()
        if self.controller.save_format in EXTENSION_KEYS:
            self.record_save_format()
        else:
            self.dialog.async_warning('不支持的格式: {}, 仅支持以下格式: \n{}'.format(self.controller.save_format, EXTENSION_KEYS_STRING), '保存格式错误')
            self.controller.save_format = self.controller.previous_save_format

    @catch_exc_for_frame_method
    def record_save_format(self, event=None):
        self.controller.previous_save_format = self.controller.save_format
        if self.controller.save_format in LOSSY_FORMATS:
            self.dialog.warning(
                '''当前保存格式为有损压缩格式, 这将导致加密后保存的图像在后续解密时出现不可预估的 噪点/分界线/颜色异常 等损坏
损坏程度与加密方法和下方的有损格式保存设置相关''', '有损保存风险警告'
            )

    @catch_exc_for_frame_method
    def stop_save_event(self, event):
        self.image_saver.cancel()
        self.dialog.info('已取消所有保存任务')
        self.stopSaveBtn.Disable()
        self.image_saver.hide_save_progress_plane()

    @catch_exc_for_frame_method
    def apply_to_all(self, event):
        if not self.tree_manager.file_dict:
            return
        if not self.controller.proc_mode_interface.can_be_set_as_default_mode:
            self.dialog.warning('当前模式不允许应用到全部')
            return
        self.apply_settings_to_all()

    @catch_exc_for_frame_method
    def revert_to_default(self, event):
        self.controller.backtrack_interface(self.mode_manager.default_settings, self.mode_manager.default_mode)
        if self.image_item is not None:
            self.image_item.sync_options_from_interface()
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

    @catch_exc_for_frame_method
    def get_serialized_encryption_parameters(self, event):
        if not self.controller.proc_mode_interface.add_encryption_parameters_in_file:
            self.dialog.info('当前模式不会生成加密参数', '提示')
            return
        loaded_image_size = (None, None) if self.image_item is None else self.image_item.cache.loaded_image_size
        self.dialog.text_display_dialog(
            '序列化的加密参数', '以下为序列化至字符后的当前加密参数',
            b85encode(pickle_dumps(gen_encryption_attributes(
                self.controller.proc_mode_interface.corresponding_decryption_mode,
                self.controller.proc_mode_interface.default_settings.serialize_encryption_parameters(*loaded_image_size)
                if self.image_item is None else
                self.image_item.settings.serialize_encryption_parameters(*loaded_image_size)
            ), HIGHEST_PROTOCOL)).decode('utf-8')
        )

    def update_quality_num(self, event: 'CommandEvent' = None):
        self.controller.save_quality_info = str(self.controller.save_quality)

    def update_subsampling_num(self, event: 'CommandEvent' = None):
        self.controller.save_subsampling_info = str(self.controller.save_subsampling_level)

    def change_redundant_cache_length(self, event: 'SpinEvent'):
        self.program_options.maximum_redundant_cache_length = event.Int

    def change_temp_dir(self, event):
        temp_dir = self.controller.temp_dir
        if temp_dir.startswith(self.program_options.temp_dir) and (temp_dir.count(sep) > self.program_options.temp_dir.count(sep)):
            self.dialog.async_warning('无法将当前缓存文件夹内的文件夹设为新的缓存文件夹')
            self.controller.temp_dir = temp_dir
            return
        if isdir(temp_dir):
            if listdir(temp_dir) and (
                self.dialog.confirmation_frame(
                    '所选文件夹不为空, 若将所选文件夹作为临时文件夹, 文件夹内文件将被清空\n确定要将所选文件夹作为临时文件夹吗',
                    '文件清空警告', YES_NO
                ) != ID_YES
            ):
                self.controller.temp_dir = self.program_options.temp_dir
                return
        elif self.dialog.confirmation_frame(
            '所选文件夹不存在, 要继续并自动创建文件夹吗',
            '文件夹不存在', YES_NO
        ) != ID_YES:
            self.controller.temp_dir = self.program_options.temp_dir
            return
        self.program_options.temp_dir = temp_dir
        self.dialog.info('新的缓存文件夹将在下次程序启动后被使用', '缓存文件夹预修改完成')

    def show_image_info(self, event):
        if self.image_item is not None:
            self.dialog.image_info_dialog(self.image_item)

    def toggle_no_extra_cache(self, event: 'CommandEvent'):
        self.program_options.no_extra_data_cache = event.IsChecked()

    def toggle_disable_cache(self, event: 'CommandEvent'):
        self.program_options.disable_cache = event.IsChecked()

    def toggle_record_interface_settings(self, event: 'CommandEvent'):
        self.program_options.record_interface_settings = event.IsChecked()

    def toggle_record_password_dict(self, event: 'CommandEvent'):
        self.program_options.record_password_dict = event.IsChecked()

    def toggle_final_layout_widgets(self, event: 'CommandEvent'):
        self.program_options.final_layout_widgets = event.IsChecked()

    def change_maximum_orig_image_cache(self, event: 'SpinEvent'):
        self.program_options.maximum_orig_image_cache = event.Int
        ImageItemCache.lru_cache_recorder.maxlen = MirageTankSettings.outside_image_cache.maxlen = event.Int

    def change_maximum_proc_result_cache(self, event: 'SpinEvent'):
        self.program_options.maximum_proc_result_cache = PreviewCache.lru_cache_recorder.maxlen = event.Int

    def open_config_folder(self, event):
        self.config.open_config_folder()

    def open_tamp_folder(self, event):
        startfile(self.temp_dir_in_use)

    def edit_save_args_json(self, event):
        user_input = self.dialog.json_editor_dialog(
            '编辑编码器参数的Json文本',
            '可使用的属性已在上方文档中说明, 格式: {属性名: 属性值, ...}\n可随意缩进\n示例(如果你不清楚了解这些属性代表了什么功能，请勿直接复制这段示例进行应用):\n{\n  "quality": 98,\n  "gamma": 2.2,\n  "exif": false,\n  "optimize": true\n}',
            'https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html',
            '点击查看相关的Pillow文档',
            self.controller.save_kwds_json
        )
        if user_input is not None:
            self.controller.save_kwds_json, self.controller.save_kwds_dict = user_input

    def exit(self, event):
        self.Hide()
        if not self.program_options.test:
            self.preview_generator.preview_thread.pause()
            if self.program_options.record_interface_settings:
                self.config.save_frame_settings()
            if self.program_options.record_password_dict:
                self.config.save_password_dict()
        self.logger.info('窗口退出')
        self.Destroy()
