'''
Author       : noeru_desu
Date         : 2021-11-13 21:43:57
LastEditors  : noeru_desu
LastEditTime : 2021-11-27 21:54:12
Description  : 图片生成功能
'''
from typing import TYPE_CHECKING

import image_encryptor.gui.processor.qq_anti_harmony as qq_anti_harmony
import image_encryptor.gui.processor.decryptor as decryptor
import image_encryptor.gui.processor.encryptor as encryptor
from image_encryptor.gui.utils.thread import ThreadManager

if TYPE_CHECKING:
    from image_encryptor.gui.frame.main_frame import MainFrame


class ImageGenerator(object):
    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.preview_thread = ThreadManager('preview-thread', True)
        self.frame.logger.info('ImageGenerator实例化完成')

    def generate_preview(self):
        if self.frame.update_password_dict():
            self.frame.password.SetValue('none')
        if self.frame.mode.Selection == 0:
            self.preview_thread.start_new(encryptor.normal, self._generate_preview_call_back, (self.frame, self.frame.previewProgressPrompt.SetLabelText, self.frame.previewProgress, self.frame.image_item.initial_preview, False))
        elif self.frame.mode.Selection == 1:
            self.preview_thread.start_new(decryptor.normal, self._generate_preview_call_back, (self.frame, self.frame.previewProgressPrompt.SetLabelText, self.frame.previewProgress, self.frame.image_item.loaded_image, False))
        else:
            self.preview_thread.start_new(qq_anti_harmony.normal, self._generate_preview_call_back, (self.frame, self.frame.previewProgressPrompt.SetLabelText, self.frame.previewProgress, self.frame.image_item.initial_preview, False))

    def _generate_preview_call_back(self, error, result):
        error, data = result
        if error:
            self.frame.error(data, '生成加密图片时出现意外错误')
            return
        self.frame.show_processing_preview(True, data)
