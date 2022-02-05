'''
Author       : noeru_desu
Date         : 2022-01-11 21:03:00
LastEditors  : noeru_desu
LastEditTime : 2022-02-05 14:56:06
Description  : 对话框相关
'''
from threading import Lock
from typing import TYPE_CHECKING

from wx import (CANCEL, DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, HELP, ICON_ERROR,
                ICON_INFORMATION, ICON_QUESTION, ICON_WARNING, ID_OK,
                STAY_ON_TOP, YES_NO, DirDialog, FileDialog, MessageDialog)

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class Dialog(object):
    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.async_dialog_exist = False
        self.async_dialog_num = 0
        self.maximum_number = 5
        self.lock = Lock()

    def dialog(self, message, title, style):
        with MessageDialog(self.frame, message, title, style=style) as dialog:
            return dialog.ShowModal()

    def select_file(self, title, wildcard='', style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST):
        with FileDialog(self.frame, title, style=style, wildcard=wildcard) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()

    def select_dir(self, title, style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST):
        with DirDialog(self.frame, title, style=style) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()

    def info(self, message, title='信息', additional_style=None, log=True):
        style = ICON_INFORMATION | STAY_ON_TOP
        if additional_style is not None:
            style |= additional_style
        if log:
            self.frame.logger.info(f'[{title}]{message}')
        return self.dialog(message, title, style)

    def question(self, message, title='确认', additional_style=None, log=True):
        style = ICON_QUESTION | STAY_ON_TOP
        if additional_style is not None:
            style |= additional_style
        if log:
            self.frame.logger.info(f'[{title}]{message}')
        return self.dialog(message, title, style)

    def warning(self, message, title='警告', additional_style=None, log=True):
        style = ICON_WARNING | STAY_ON_TOP
        if additional_style is not None:
            style |= additional_style
        if log:
            self.frame.logger.warning(f'[{title}]{message}')
        return self.dialog(message, title, style)

    def error(self, message, title='错误', additional_style=None, log=True):
        style = ICON_ERROR | STAY_ON_TOP
        if additional_style is not None:
            style |= additional_style
        if log:
            self.frame.logger.error(f'[{title}]{message}')
        return self.dialog(message, title, style)

    def confirmation_frame(self, message, title='确认', style=YES_NO | CANCEL, yes='是', no='否', cancel='取消', help=None):
        if help is not None:
            style = YES_NO | CANCEL | HELP
        else:
            style = YES_NO | CANCEL
        with MessageDialog(self.frame, message, title, style=style | STAY_ON_TOP) as dialog:
            if help is not None:
                dialog.SetOKLabel(help)
            dialog.SetYesNoCancelLabels(yes, no, cancel)
            return dialog.ShowModal()

    def _register_async_dialog(self, force):
        """注册成功则返回True，反之则返回False"""
        with self.lock:
            if (not force and self.async_dialog_exist) or self.async_dialog_num >= self.maximum_number:
                return False
            else:
                self.async_dialog_num += 1
                self.async_dialog_exist = True
                return True

    def _async_dialog_callback(self, future):
        with self.lock:
            self.async_dialog_num -= 1
            if self.async_dialog_num == 0:
                self.async_dialog_exist = False

    def async_select_file(self, title, wildcard='', style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.select_file, title, wildcard, style).add_done_callback(self._async_dialog_callback)
        return True

    def async_select_dir(self, title, style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.select_dir, title, style).add_done_callback(self._async_dialog_callback)
        return True

    def async_info(self, message, title='信息', additional_style=None, log=True, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.info, message, title, additional_style, log).add_done_callback(self._async_dialog_callback)
        return True

    def async_question(self, message, title='确认', additional_style=None, log=True, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.question, message, title, additional_style, log).add_done_callback(self._async_dialog_callback)
        return True

    def async_warning(self, message, title='警告', additional_style=None, log=True, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.warning, message, title, additional_style, log).add_done_callback(self._async_dialog_callback)
        return True

    def async_error(self, message, title='错误', additional_style=None, log=True, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.error, message, title, additional_style, log).add_done_callback(self._async_dialog_callback)
        return True

    def async_confirmation_frame(self, message, title='确认', additional_style=None, yes='是', no='否', cancel='取消', help=None, force=False):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.confirmation_frame, message, title, additional_style, yes, no, cancel, help).add_done_callback(self._async_dialog_callback)
        return True


def singel_dialog(message, title, style=None):
    with MessageDialog(None, message, title, style=style) as dialog:
        return dialog.ShowModal()
