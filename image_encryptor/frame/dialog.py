"""
Author       : noeru_desu
Date         : 2022-01-11 21:03:00
LastEditors  : noeru_desu
LastEditTime : 2022-03-06 16:36:43
Description  : 对话框相关
"""
from threading import Lock
from typing import TYPE_CHECKING

from wx import (CANCEL, DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, HELP, ICON_ERROR,
                ICON_INFORMATION, ICON_QUESTION, ICON_WARNING, ID_OK,
                STAY_ON_TOP, YES_NO, ID_CANCEL, DirDialog, FileDialog, MessageDialog)

from image_encryptor.frame.design_frame import PasswordDialog as PD

# from image_encryptor.utils.misc_util import gen_slots_str

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class Dialog(object):
    __slots__ = ('frame', 'async_dialog_exist', 'async_dialog_num', 'maximum_number', 'lock')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.async_dialog_exist = False
        self.async_dialog_num = 0
        self.maximum_number = 5
        self.lock = Lock()

    def dialog(self, message, title, style, parent=...):
        if parent is Ellipsis:
            parent = self.frame
        with MessageDialog(parent, message, title, style=style) as dialog:
            return dialog.ShowModal()

    def select_file(self, title, wildcard='', style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST, parent=...):
        if parent is Ellipsis:
            parent = self.frame
        with FileDialog(parent, title, style=style, wildcard=wildcard) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()

    def select_dir(self, title, style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST, parent=...):
        if parent is Ellipsis:
            parent = self.frame
        with DirDialog(parent, title, style=style) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()

    def info(self, message, title='信息', additional_style=..., log=True, parent=...):
        style = ICON_INFORMATION | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.info(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def question(self, message, title='确认', additional_style=..., log=True, parent=...):
        style = ICON_QUESTION | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.info(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def warning(self, message, title='警告', additional_style=..., log=True, parent=...):
        style = ICON_WARNING | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.warning(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def error(self, message, title='错误', additional_style=..., log=True, parent=...):
        style = ICON_ERROR | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.error(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def confirmation_frame(self, message, title='确认', style=YES_NO | CANCEL, yes='是', no='否', cancel='取消', help=None, parent=...):
        if parent is Ellipsis:
            parent = self.frame
        style = YES_NO | CANCEL | HELP if help is not None else YES_NO | CANCEL
        with MessageDialog(parent, message, title, style=style | STAY_ON_TOP) as dialog:
            if help is not None:
                dialog.SetOKLabel(help)
            dialog.SetYesNoCancelLabels(yes, no, cancel)
            return dialog.ShowModal()

    def password_dialog(self, file_name, correct_base64, until_correct=False, parent=...):
        if parent is Ellipsis:
            parent = self.frame
        dialog = PasswordDialog(parent, file_name, correct_base64, until_correct)
        with dialog:
            return_code = dialog.ShowModal()
        if return_code == ID_CANCEL:
            return None
        elif return_code == ID_OK:
            return dialog.correct_password

    def _register_async_dialog(self, force):
        """注册成功则返回True，反之则返回False"""
        with self.lock:
            if (not force and self.async_dialog_exist) or self.async_dialog_num >= self.maximum_number:
                return False
            self.async_dialog_num += 1
            self.async_dialog_exist = True
            return True

    def _async_dialog_callback(self, future):
        with self.lock:
            self.async_dialog_num -= 1
            if self.async_dialog_num == 0:
                self.async_dialog_exist = False

    def async_select_file(self, title, wildcard='', style=FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.select_file, title, wildcard, style, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_select_dir(self, title, style=DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.select_dir, title, style, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_info(self, message, title='信息', additional_style=..., log=True, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.info, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_question(self, message, title='确认', additional_style=..., log=True, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.question, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_warning(self, message, title='警告', additional_style=..., log=True, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.warning, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_error(self, message, title='错误', additional_style=..., log=True, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.error, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_confirmation_frame(self, message, title='确认', additional_style=..., yes='是', no='否', cancel='取消', help=None, force=False, parent=...):
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.confirmation_frame, message, title, additional_style, yes, no, cancel, help, parent).add_done_callback(self._async_dialog_callback)
        return True

    @staticmethod
    def singel_dialog(message, title, style=None):
        with MessageDialog(None, message, title, style=style) as dialog:
            return dialog.ShowModal()


class PasswordDialog(PD):
    __slots__ = ('_parent', '_correct_base64', '_until_correct', 'correct_password')

    def __init__(self, parent: 'MainFrame', file_name, correct_base64, until_correct=False):
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self._parent = parent
        self._correct_base64 = correct_base64
        self._until_correct = until_correct
        self.correct_password: str = None
        self.SetReturnCode(ID_CANCEL)
        self.fileNameText.LabelText = file_name
        self.mainPanel.Layout()

    def user_confirm(self, event):
        password = self.passwordTextCtrl.Value
        if not password:
            if self._until_correct:
                self.tipText.LabelText = '密码为空! 取消输入密码请点击[取消]'
                self.mainPanel.Layout()
            else:
                self.user_cancel(event)
        elif self._parent.add_password_dict(password, self):
            password = self._parent.password_dict.get_password(self._correct_base64)
            if password is not None:
                self.correct_password = password
                self.EndModal(ID_OK)
            elif self._until_correct:
                self.tipText.LabelText = '密码错误! 请重新输入'
                self.mainPanel.Layout()
                self.passwordTextCtrl.Clear()
            else:
                self.user_cancel(event)
        elif self._until_correct:
            self.tipText.LabelText = '密码不符合要求, 请重新输入'
            self.mainPanel.Layout()
            self.passwordTextCtrl.Clear()
        else:
            self.user_cancel(event)

    def user_cancel(self, event):
        self.EndModal(ID_CANCEL)
