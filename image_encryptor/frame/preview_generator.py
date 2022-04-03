"""
Author       : noeru_desu
Date         : 2021-11-13 21:43:57
LastEditors  : noeru_desu
LastEditTime : 2022-03-30 05:35:09
Description  : 图像生成功能
"""
from typing import TYPE_CHECKING

import image_encryptor.modes.decrypt as decrypt
import image_encryptor.modes.encrypt as encrypt
import image_encryptor.modes.anti_harmony as anti_harmony
from image_encryptor.constants import ORIG_IMAGE
from image_encryptor.modules.image import ImageData, PillowImage
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
        if self.frame.controls.preview_source == ORIG_IMAGE:
            source = self.frame.image_item.cache.loaded_image
            type_conversion = PillowImage
        else:
            source = self.frame.image_item.cache.initial_preview
            type_conversion = ImageData
        match self.frame.controls.proc_mode:
            case 0:
                self.preview_thread.start_new(encrypt.normal, self._generate_preview_call_back, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    source, False, type_conversion
                ))
            case 1:
                self.preview_thread.start_new(decrypt.normal, self._generate_preview_call_back, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    self.frame.image_item.cache.loaded_image, False, PillowImage
                ))
            case 2:
                self.preview_thread.start_new(anti_harmony.normal, self._generate_preview_call_back, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    source, False
                ))

    def _generate_preview_call_back(self, err, result):
        data, error = result
        if error is not None:
            self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')
            return
        self.frame.controls.display_and_cache_processed_preview(data)
