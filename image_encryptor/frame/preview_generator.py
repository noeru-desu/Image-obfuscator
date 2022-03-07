"""
Author       : noeru_desu
Date         : 2021-11-13 21:43:57
LastEditors  : noeru_desu
LastEditTime : 2022-03-07 10:11:33
Description  : 图片生成功能
"""
from typing import TYPE_CHECKING

import image_encryptor.processor.decryptor as decryptor
import image_encryptor.processor.encryptor as encryptor
import image_encryptor.processor.qq_anti_harmony as qq_anti_harmony
from image_encryptor.constants import (DECRYPTION_MODE, ENCRYPTION_MODE,
                                       PREVIEW_IMAGE)
from image_encryptor.utils.thread import ThreadManager

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class PreviewGenerator(object):
    __slots__ = ('frame', 'preview_thread')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.preview_thread = ThreadManager('preview-thread', True)

    def generate_preview(self):
        if not self.frame.update_password_dict():
            self.frame.controls.password = 'none'
        if self.frame.controls.proc_mode == ENCRYPTION_MODE:
            self.preview_thread.start_new(encryptor.normal, self._generate_preview_call_back, (
                self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                self.frame.image_item.cache.initial_preview if self.frame.controls.preview_source == PREVIEW_IMAGE else self.frame.image_item.cache.loaded_image,
                False
            ))
        elif self.frame.controls.proc_mode == DECRYPTION_MODE:
            self.preview_thread.start_new(decryptor.normal, self._generate_preview_call_back, (
                self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                self.frame.image_item.cache.loaded_image, False))
        else:
            self.preview_thread.start_new(qq_anti_harmony.normal, self._generate_preview_call_back, (
                self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                self.frame.image_item.cache.initial_preview if self.frame.controls.preview_source == PREVIEW_IMAGE else self.frame.image_item.cache.loaded_image,
                False))

    def _generate_preview_call_back(self, error, result):
        error, data = result
        if error:
            self.frame.dialog.error(data, '生成加密图片时出现意外错误')
            return
        self.frame.controls.regen_processed_preview(data)
