"""
Author       : noeru_desu
Date         : 2021-11-06 19:06:56
LastEditors  : noeru_desu
LastEditTime : 2022-04-30 08:04:53
Description  : 拖放处理
"""
from os.path import isdir
from traceback import format_exc
from typing import TYPE_CHECKING

from wx import FileDropTarget

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class DragLoadingFile(FileDropTarget):
    __slots__ = ('frame',)

    def __init__(self, frame: 'MainFrame'):
        super().__init__()
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        try:
            if self.frame.image_loader.loading_thread.is_alive:
                self.frame.dialog.async_warning('请等待当前载入任务结束后再载入新的文件')
            else:
                filenames = tuple(filenames)
                self.frame.image_loader.load(filenames)
        except RuntimeError:
            return False
        except Exception:
            self.frame.dialog.error(format_exc())
        else:
            return True


class DragSavingPath(FileDropTarget):
    __slots__ = ('frame',)

    def __init__(self, frame: 'MainFrame'):
        super().__init__()
        self.frame = frame

    def OnDropFiles(self, x, y, filenames):
        try:
            filenames = [i for i in filenames if isdir(i)]
            if not filenames:
                self.frame.dialog.async_warning('拖放的目标不是文件夹')
                return True
            elif len(filenames) > 1:
                self.frame.dialog.async_warning(f'共拖放了{len(filenames)}个文件夹，仅接受第一个文件夹({filenames[0]})')
            self.frame.controls.saving_path = filenames[0]
        except RuntimeError:
            return False
        except Exception:
            self.frame.dialog.error(format_exc())
        else:
            return True
