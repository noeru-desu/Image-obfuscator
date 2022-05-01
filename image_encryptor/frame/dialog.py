"""
Author       : noeru_desu
Date         : 2022-01-11 21:03:00
LastEditors  : noeru_desu
LastEditTime : 2022-05-01 13:02:17
Description  : 对话框相关
"""
from threading import Lock
from types import EllipsisType
from typing import TYPE_CHECKING, Optional

from wx import (CANCEL, DIRP_DEFAULT_STYLE, DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR,
                FD_DEFAULT_STYLE, FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, HELP, ICON_ERROR,
                ICON_INFORMATION, ICON_QUESTION, ICON_WARNING, ID_CANCEL,
                ID_OK, STAY_ON_TOP, YES_NO, DirDialog, FileDialog,
                MessageDialog)

from image_encryptor.frame.design_frame import PasswordDialog as PD
# from image_encryptor.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from os import PathLike
    from wx import Window
    from image_encryptor.frame.events import MainFrame


class Dialog(object):
    __slots__ = ('frame', 'async_dialog_exist', 'async_dialog_num', 'maximum_number', 'lock')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.async_dialog_exist = False
        self.async_dialog_num = 0
        self.maximum_number = 5
        self.lock = Lock()

    def dialog(self, message: str, title: str, style: int, parent: 'Window' = ...) -> int:
        if parent is Ellipsis:
            parent = self.frame
        with MessageDialog(parent, message, title, style=style) as dialog:
            return dialog.ShowModal()

    def select_file(self, title: str, wildcard: str = '', style: int = FD_DEFAULT_STYLE | FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST, parent: 'Window' = ...) -> Optional['PathLike[str]']:
        if parent is Ellipsis:
            parent = self.frame
        with FileDialog(parent, title, style=style, wildcard=wildcard) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()

    def select_dir(self, title: str, style: int =DIRP_DEFAULT_STYLE | DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST, parent: 'Window' = ...) -> Optional['PathLike[str]']:
        if parent is Ellipsis:
            parent = self.frame
        with DirDialog(parent, title, style=style) as dialog:
            if ID_OK == dialog.ShowModal():
                return dialog.GetPath()

    def info(self, message: str, title: str = '信息', additional_style: int = ..., log: bool = True, parent: 'Window' = ...) -> int:
        style = ICON_INFORMATION | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.info(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def question(self, message: str, title: str = '确认', additional_style: int = ..., log: bool = True, parent: 'Window' = ...) -> int:
        style = ICON_QUESTION | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.info(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def warning(self, message: str, title: str = '警告', additional_style: int = ..., log: bool = True, parent: 'Window' = ...) -> int:
        style = ICON_WARNING | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.warning(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def error(self, message: str, title: str = '错误', additional_style: int = ..., log: bool = True, parent: 'Window' = ...) -> int:
        style = ICON_ERROR | STAY_ON_TOP
        if additional_style is not Ellipsis:
            style |= additional_style
        if log:
            self.frame.logger.error(f'[{title}]{message}')
        return self.dialog(message, title, style, parent)

    def confirmation_frame(self, message: str, title: str = '确认', style: int = YES_NO | CANCEL, yes='是', no='否', cancel='取消', help=None, parent: 'Window' = ...) -> int:
        if parent is Ellipsis:
            parent = self.frame
        if help is not None:
            style |= HELP
        with MessageDialog(parent, message, title, style=style | STAY_ON_TOP) as dialog:
            if help is not None:
                dialog.SetOKLabel(help)
            dialog.SetYesNoCancelLabels(yes, no, cancel)
            return dialog.ShowModal()

    def password_dialog(self, file_name: str, correct_base64: str, until_correct: bool = False, parent: 'Window' = ...):
        if parent is Ellipsis:
            parent = self.frame
        dialog = PasswordDialog(parent, file_name, correct_base64, until_correct)
        with dialog:
            return_code = dialog.ShowModal()
        if return_code == ID_CANCEL:
            return None
        elif return_code == ID_OK:
            return dialog.correct_password

    def _register_async_dialog(self, force: bool) -> bool:
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

    def async_select_file(self, title: str, wildcard: str = '', style: int = FD_OPEN | FD_CHANGE_DIR | FD_PREVIEW | FD_FILE_MUST_EXIST, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.select_file, title, wildcard, style, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_select_dir(self, title: str, style: int = DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.select_dir, title, style, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_info(self, message: str, title: str = '信息', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.info, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_question(self, message: str, title: str =' 确认', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.question, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_warning(self, message: str, title: str= '警告', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.warning, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_error(self, message: str, title: str= '错误', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.error, message, title, additional_style, log, parent).add_done_callback(self._async_dialog_callback)
        return True

    def async_confirmation_frame(self, message: str, title: str = '确认', additional_style: int = ..., yes: str = '是', no: str = '否', cancel: str = '取消', help: str = None, force: bool = False, parent: 'Window' = ...) -> bool:
        if not self._register_async_dialog(force):
            return False
        self.frame.universal_thread_pool.submit(self.confirmation_frame, message, title, additional_style, yes, no, cancel, help, parent).add_done_callback(self._async_dialog_callback)
        return True

    @staticmethod
    def singel_dialog(message: str, title: str, style: int = None) -> int:
        with MessageDialog(None, message, title, style=style) as dialog:
            return dialog.ShowModal()


class PasswordDialog(PD):
    __slots__ = ('_parent', '_correct_base64', '_until_correct', 'correct_password')

    def __init__(self, parent: 'MainFrame', file_name: str, correct_base64: str, until_correct: bool = False):
        """
        Args:
            parent (MainFrame): MainFrame实例
            file_name (str): 显示的文件名称
            correct_base64 (str): 正确密码的验证用base64(通常由`PasswordDict.get_validation_field_base64`生成)
            until_correct (bool, optional): 是否一直接受用户输入直到密码正确. 默认为False, 为False时将在一次确认输入后关闭密码输入弹窗
        """
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
