'''
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2021-11-13 11:36:22
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
            filenames = list(filenames)
            self.frame.image_loader.load(filenames)
        except RuntimeError:
            return False
        else:
            return True
