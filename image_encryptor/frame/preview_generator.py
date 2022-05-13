"""
Author       : noeru_desu
Date         : 2021-11-13 21:43:57
LastEditors  : noeru_desu
LastEditTime : 2022-05-13 20:26:56
Description  : 图像生成功能
"""
from typing import TYPE_CHECKING

import image_encryptor.modes.decrypt as decrypt
import image_encryptor.modes.encrypt as encrypt
import image_encryptor.modes.anti_shielded as anti_shielded
from image_encryptor.constants import ProcModes, ORIG_IMAGE
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
        if not self.frame.update_password_dict():
            self.frame.controls.password = 'none'
        if self.frame.controls.preview_source == ORIG_IMAGE:
            source = self.frame.image_item.cache.loaded_image
            type_conversion = PillowImage
        else:
            source = self.frame.image_item.cache.initial_preview
            type_conversion = ImageData
        with self.preview_thread.thread.lock:
            if not self.preview_thread.idle:
                self.preview_thread.interrupt_task()
        match self.frame.controls.proc_mode:
            case ProcModes.encryption_mode:
                self.preview_thread.add_task(encrypt.normal, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    source, False, type_conversion
                ), cb=self._generate_preview_call_back)
            case ProcModes.decryption_mode:
                self.preview_thread.add_task(decrypt.normal, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    self.frame.image_item.cache.loaded_image, False, PillowImage
                ), cb=self._generate_preview_call_back)
            case ProcModes.anti_shielded_mode:
                self.preview_thread.add_task(anti_shielded.normal, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    source, False, self.frame.controls.preview_source == ORIG_IMAGE
                ), cb=self._generate_preview_call_back)

    def _generate_preview_call_back(self, result):
        data, error = result
        if error is not None:
            self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')
            return
        self.frame.controls.display_and_cache_processed_preview(data)
