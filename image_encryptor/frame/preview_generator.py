"""
Author       : noeru_desu
Date         : 2021-11-13 21:43:57
LastEditors  : noeru_desu
LastEditTime : 2022-05-29 17:53:22
Description  : 图像生成功能
"""
from typing import TYPE_CHECKING

from image_encryptor.constants import ORIG_IMAGE
from image_encryptor.modules.image import ImageData, PillowImage
from image_encryptor.utils.thread import SingleThreadExecutor

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class PreviewGenerator(object):
    __slots__ = ('frame', 'preview_thread')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.preview_thread = SingleThreadExecutor('preview-thread', 1)

    def generate_preview(self):
        self.frame.controller.standardized_password_ctrl()
        with self.preview_thread.thread.lock:
            if not self.preview_thread.idle:
                self.preview_thread.interrupt_task()
        image_item = self.frame.image_item
        mode_interface = self.frame.controller.proc_mode_interface
        if image_item.encrypted_image and mode_interface.mode_id == image_item.encryption_parameters.decryption_mode.mode_id:
            settings = image_item.cache.encryption_parameters.settings
        else:
            settings = self.frame.settings.all
        if mode_interface.decryption_mode or self.frame.controller.preview_source == ORIG_IMAGE:
            self.preview_thread.add_task(mode_interface.proc_image, (
                self.frame, image_item.cache.loaded_image, True, PillowImage,
                settings, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress
            ), cb=self._generate_preview_call_back)
        else:
            self.preview_thread.add_task(mode_interface.proc_image, (
                self.frame, image_item.cache.initial_preview, False, ImageData,
                settings, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress
            ), cb=self._generate_preview_call_back)

    def _generate_preview_call_back(self, result):
        data, error = result
        if error is not None:
            self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')
            return
        self.frame.controller.display_and_cache_processed_preview(data)
