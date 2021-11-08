'''
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2021-11-07 21:34:17
Description  : 拖放处理
'''
from typing import TYPE_CHECKING

from wx import FileDropTarget

if TYPE_CHECKING:
    from image_encryptor.gui.frame.main_frame import MainFrame


class DragImport(FileDropTarget):
    def __init__(self, frame: 'MainFrame'):
        super().__init__()
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        try:
            if self.frame.loading_thread.is_running:
                self.frame.warning('请等待当前图片载入完成后再载入新的图片')
                return
            filenames = list(filenames)
            self.frame.program.logger.info(f'拖放导入：{filenames[0]}')
            self.frame.loading_thread.start_new(self.frame.load_image, self.callback, (filenames[0],), callback_args=(filenames[1:],))
        except RuntimeError:
            return False
        else:
            return True

    def callback(self, error, result, filenames):
        if not filenames:
            return
        self.frame.program.logger.info(f'拖放导入：{filenames[0]}')
        self.frame.loading_thread.start_new(self.frame.load_image, self.callback, (filenames[0],), callback_args=(filenames[1:],))
