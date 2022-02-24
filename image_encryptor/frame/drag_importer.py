"""
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2022-02-24 21:13:46
Description  : 拖放处理
"""
from os.path import isdir
from typing import TYPE_CHECKING

from wx import FileDropTarget

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class DragLoader(FileDropTarget):
    def __init__(self, frame: 'MainFrame'):
        super().__init__()
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        try:
            if self.frame.image_loader.loading_thread.is_alive:
                self.frame.dialog.async_warning('请等待当前载入任务结束后再载入新的文件')
            else:
                filenames = list(filenames)
                self.frame.image_loader.load(filenames)
        except RuntimeError:
            return False
        else:
            return True


class DragSavingPath(FileDropTarget):
    def __init__(self, frame: 'MainFrame'):
        super().__init__()
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        try:
            filenames = [i for i in filenames if isdir(i)]
            if not filenames:
                self.frame.dialog.async_warning('拖放的文件不是文件夹')
                return True
            elif len(filenames) > 1:
                self.frame.dialog.async_warning(f'您拖放了{len(filenames)}个文件夹，仅接受第一个文件夹({filenames[0]})')
            self.frame.controls.saving_path = filenames[0]
        except RuntimeError:
            return False
        else:
            return True
