"""
Author       : noeru_desu
Date         : 2021-11-13 21:43:57
LastEditors  : noeru_desu
LastEditTime : 2022-03-20 10:28:04
Description  : 图片生成功能
"""
from typing import TYPE_CHECKING

import image_encryptor.modes.decryptor as decryptor
import image_encryptor.modes.encryptor as encryptor
import image_encryptor.modes.qq_anti_harmony as qq_anti_harmony
from image_encryptor.constants import ORIG_IMAGE
from image_encryptor.utils.image import ImageData, PillowImage
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
                self.preview_thread.start_new(encryptor.normal, self._generate_preview_call_back, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    source, False, type_conversion
                ), callback_args=(self.frame.controls.preview_source == ORIG_IMAGE,))
            case 1:
                self.preview_thread.start_new(decryptor.normal, self._generate_preview_call_back, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    self.frame.image_item.cache.loaded_image, False, PillowImage
                ), callback_args=(True,))
            case 2:
                self.preview_thread.start_new(qq_anti_harmony.normal, self._generate_preview_call_back, (
                    self.frame, self.frame.previewProgressInfo.SetLabelText, self.frame.previewProgress,
                    source, False
                ), callback_args=(self.frame.controls.preview_source == ORIG_IMAGE,))

    def _generate_preview_call_back(self, err, result, resize):
        data, error = result
        if error is not None:
            self.frame.dialog.error(error, '生成加密图片时出现意外错误')
            return
        self.frame.controls.regen_processed_preview(data, resize)
