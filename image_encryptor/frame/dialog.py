"""
Author       : noeru_desu
Date         : 2022-01-11 21:03:00
LastEditors  : noeru_desu
LastEditTime : 2022-08-05 12:05:53
Description  : 对话框相关
"""
from json import JSONDecodeError, dumps, loads
from typing import TYPE_CHECKING, Optional

from image_encryptor.frame.design_frame import JsonEditorDialog as JED
from image_encryptor.frame.design_frame import PasswordDialog as PD
from image_encryptor.utils.thread import SingleThreadExecutor
from wx import (CANCEL, DIRP_CHANGE_DIR, DIRP_DEFAULT_STYLE,
                DIRP_DIR_MUST_EXIST, FD_CHANGE_DIR, FD_DEFAULT_STYLE,
                FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW, HELP, ICON_ERROR,
                ICON_INFORMATION, ICON_QUESTION, ICON_WARNING, ID_CANCEL,
                ID_NO, ID_OK, ID_YES, STAY_ON_TOP, YES_NO, RED, WHITE, Colour, DirDialog,
                FileDialog, MessageDialog)
from wx.stc import (STC_JSON_BLOCKCOMMENT, STC_JSON_COMPACTIRI,
                    STC_JSON_DEFAULT, STC_JSON_ERROR, STC_JSON_ESCAPESEQUENCE,
                    STC_JSON_KEYWORD, STC_JSON_LDKEYWORD, STC_JSON_LINECOMMENT,
                    STC_JSON_NUMBER, STC_JSON_OPERATOR, STC_JSON_PROPERTYNAME,
                    STC_JSON_STRING, STC_JSON_STRINGEOL, STC_JSON_URI,
                    STC_LEX_JSON)

# from image_encryptor.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from os import PathLike

    from image_encryptor.frame.events import MainFrame
    from wx import CloseEvent, Window


class Dialog(object):
    __slots__ = ('frame', 'dialog_thread')

    def __init__(self, frame: 'MainFrame', maxlen: int = None):
        """
        Args:
            frame (MainFrame): `MainFrame`实例
            maxlen (int, optional): 异步对话框队列长度. 默认为None(无限).
        """
        self.frame = frame
        self.dialog_thread = SingleThreadExecutor('dialog-thread', maxlen)
        self.dialog_thread.set_exception_callback(lambda err, dialog: dialog(err.traceback), self.error)

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

    def question(self, message: str, title: str = '询问', additional_style: int = ..., log: bool = True, parent: 'Window' = ...) -> int:
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

    def confirmation_frame(self, message: str, title: str = '询问', style: int = YES_NO | CANCEL, yes='是', no='否', cancel='取消', help=None, parent: 'Window' = ...) -> int:
        if parent is Ellipsis:
            parent = self.frame
        if help is not None:
            style |= HELP
        with MessageDialog(parent, message, title, style=style | STAY_ON_TOP) as dialog:
            if help is not None:
                dialog.SetOKLabel(help)
            dialog.SetYesNoCancelLabels(yes, no, cancel)
            return dialog.ShowModal()

    def password_dialog(self, file_name: str, correct_base85: str, until_correct: bool = False, parent: 'Window' = ...):
        if parent is Ellipsis:
            parent = self.frame
        dialog = PasswordDialog(parent, file_name, correct_base85, until_correct)
        with dialog:
            return_code = dialog.ShowModal()
        if return_code == ID_CANCEL:
            return None
        elif return_code == ID_OK:
            return dialog.correct_password

    def json_editor_dialog(self, title_text: str = '编辑Json文本', extra_info: str = '', extra_link: str = '', extra_link_info: str = '', json_text: str = '{\n  \n}', parent: 'Window' = ...):
        if parent is Ellipsis:
            parent = self.frame
        dialog = JsonEditorDialog(parent, title_text, extra_info, extra_link, extra_link_info, json_text)
        with dialog:
            return_code = dialog.ShowModal()
        if return_code == ID_CANCEL:
            return None
        elif return_code == ID_OK:
            return dialog.user_saved_json, dialog.user_saved_dict

    """
    def _register_async_dialog(self, force: bool = False) -> bool:
        '''注册异步对话框

        Args:
            force (bool): 是否在已存在异步对话框的情况下, 仍然尝试弹出对话框

        Returns:
            bool: 是否注册完成并允许弹出对话框
        '''
        with self.lock:
            if (not force and self.async_dialog_exist) or self.async_dialog_num >= self.maximum_number:
                if queue:
                    self.queue.put()
                return False
            self.async_dialog_num += 1
            self.async_dialog_exist = True
            return True

    def _async_dialog_callback(self, future):
        with self.lock:
            self.async_dialog_num -= 1
            if self.async_dialog_num == 0:
                self.async_dialog_exist = False
    """

    def async_info(self, message: str, title: str = '信息', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if self.dialog_thread.full:
            return False
        self.dialog_thread.add_task(self.info, (message, title, additional_style, log, parent))
        return True

    def async_question(self, message: str, title: str =' 确认', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if self.dialog_thread.full:
            return False
        self.dialog_thread.add_task(self.question, (message, title, additional_style, log, parent))
        return True

    def async_warning(self, message: str, title: str= '警告', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if self.dialog_thread.full:
            return False
        self.dialog_thread.add_task(self.warning, (message, title, additional_style, log, parent))
        return True

    def async_error(self, message: str, title: str= '错误', additional_style: int = ..., log: bool = True, force: bool = False, parent: 'Window' = ...) -> bool:
        if self.dialog_thread.full:
            return False
        self.dialog_thread.add_task(self.error, (message, title, additional_style, log, parent))
        return True

    def async_confirmation_frame(self, message: str, title: str = '确认', additional_style: int = ..., yes: str = '是', no: str = '否', cancel: str = '取消', help: str = None, force: bool = False, parent: 'Window' = ...) -> bool:
        if self.dialog_thread.full:
            return False
        self.dialog_thread.add_task(self.confirmation_frame, (message, title, additional_style, yes, no, cancel, help, parent))
        return True

    @staticmethod
    def singel_dialog(message: str, title: str, style: int = None) -> int:
        with MessageDialog(None, message, title, style=style) as dialog:
            return dialog.ShowModal()


class PasswordDialog(PD):
    __slots__ = ('_parent', '_correct_base85', '_until_correct', 'correct_password')

    def __init__(self, parent: 'MainFrame', file_name: str, correct_base85: str, until_correct: bool = False):
        """
        Args:
            parent (MainFrame): MainFrame实例
            file_name (str): 显示的文件名称
            correct_base85 (str): 正确密码的验证用base85(通常由`PasswordDict.get_validation_field_base85`生成)
            until_correct (bool, optional): 是否一直接受用户输入直到密码正确. 默认为False, 为False时将在一次确认输入后关闭密码输入弹窗
        """
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self._parent = parent
        self._correct_base85 = correct_base85
        self._until_correct = until_correct
        self.correct_password: str = None
        self.SetReturnCode(ID_CANCEL)
        self.fileNameText.SetLabelText(file_name)
        self.mainPanel.Layout()

    def user_confirm(self, event):
        password = self.passwordTextCtrl.GetValue()
        if not password:
            if self._until_correct:
                self.tipText.SetLabelText('密码为空! 取消输入密码请点击[取消]')
                self.mainPanel.Layout()
            else:
                self.user_cancel(event)
        elif self._parent.add_password_dict(password, self):
            password = self._parent.password_dict.get_password(self._correct_base85)
            if password is not None:
                self.correct_password = password
                self.EndModal(ID_OK)
            elif self._until_correct:
                self.tipText.SetLabelText('密码错误! 请重新输入')
                self.mainPanel.Layout()
                self.passwordTextCtrl.Clear()
            else:
                self.user_cancel(event)
        elif self._until_correct:
            self.tipText.SetLabelText=('密码不符合要求, 请重新输入')
            self.mainPanel.Layout()
            self.passwordTextCtrl.Clear()
        else:
            self.user_cancel(event)

    def user_cancel(self, event):
        self.EndModal(ID_CANCEL)


# 样式与Scintilla的json.properties中的配置大部分相同
json_foreground_style = (
    (STC_JSON_DEFAULT, Colour(150, 150, 150)),
    (STC_JSON_ERROR, WHITE),
    (STC_JSON_NUMBER, Colour(0, 127, 127)),
    (STC_JSON_STRING, Colour(127, 0, 0)),
    (STC_JSON_STRINGEOL, WHITE),
    (STC_JSON_PROPERTYNAME, Colour(136, 10, 232)),
    (STC_JSON_ESCAPESEQUENCE, Colour(11, 152, 46)),
    (STC_JSON_LINECOMMENT, Colour(5, 187, 174)),
    (STC_JSON_BLOCKCOMMENT, Colour(5, 187, 174)),
    (STC_JSON_OPERATOR, Colour(24, 100, 74)),
    (STC_JSON_URI, Colour(24, 100, 255)),
    (STC_JSON_COMPACTIRI, Colour(209, 55, 193)),
    (STC_JSON_KEYWORD, Colour(11, 206, 167)),
    (STC_JSON_LDKEYWORD, Colour(236, 40, 6))
)


class JsonEditorDialog(JED):
    __slots__ = ('_parent', 'target_json_type', 'user_saved_json', 'user_saved_dict')

    def __init__(self, parent: 'MainFrame', title_text: str = '编辑Json文本', extra_info: str = '', extra_link: str = '', extra_link_info: str = '', json_text: str = '{\n  \n}', target_json_type=dict):
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self._parent = parent
        self.target_json_type = target_json_type
        self.user_saved_json = None
        self.user_saved_dict = None
        self.titleText.SetLabelText(title_text)
        self.extraInfoText.SetLabelText(extra_info)
        self.extraLink.SetLabelText(extra_link_info)
        self.extraLink.SetURL(extra_link)
        self.textEditor.SetValue(json_text)
        self.SetReturnCode(ID_CANCEL)
        self.set_style()
        self.Layout()

    def set_style(self):
        # 样式与Scintilla的json.properties中的配置相同(除特殊注释处)
        self.textEditor.StyleClearAll()
        self.textEditor.SetViewWhiteSpace(True)
        self.textEditor.SetLexer(STC_LEX_JSON)
        self.textEditor.SetProperty('lexer.json.allow.comments', "0")   # Python内置json标准库不支持注释(第三方库json5支持)
        self.textEditor.SetProperty('lexer.json.escape.sequence', "1")
        self.textEditor.SetKeyWords(0, 'false true null')
        self.textEditor.SetKeyWords(1, '@id @context @type @value @language @container @list @set @reverse @index @base @vocab @graph')
        for style, fore in json_foreground_style:
            self.textEditor.StyleSetForeground(style, fore)
        self.textEditor.SetWhitespaceSize(2)
        self.textEditor.StyleSetBackground(STC_JSON_STRINGEOL, RED)
        self.textEditor.StyleSetBackground(STC_JSON_ERROR, RED)
        self.textEditor.StyleSetEOLFilled(STC_JSON_STRINGEOL, True)
        self.textEditor.StyleSetBold(STC_JSON_KEYWORD, True)
        self.textEditor.StyleSetItalic(STC_JSON_LINECOMMENT, True)
        self.textEditor.StyleSetItalic(STC_JSON_BLOCKCOMMENT, True)

    def check_json_format(self, event=None) -> Optional[dict]:
        try:
            data = loads(self.textEditor.GetValue())
        except JSONDecodeError as e:
            if e.doc[e.pos] == '/':
                self._parent.dialog.async_warning(f'注释功能不被Python中的json标准库支持: 第{e.lineno}行, 第{e.colno}列 (从文本开头开始第{e.pos}个字符)\n', 'Json格式检查', parent=self)
            else:
                self._parent.dialog.async_warning(f'{e.msg}: 第{e.lineno}行, 第{e.colno}列 (从文本开头开始第{e.pos}个字符)', 'Json格式检查', parent=self)
            return None
        else:
            if not isinstance(data, dict):
                self._parent.dialog.async_warning('Json类型错误, 需要键值对，而不是数组', 'Json格式检查', parent=self)
                return None
            if event is None:
                return data
            self._parent.dialog.async_info('Json文本基础格式检查已通过', 'Json格式检查', parent=self)
        return None

    def format_json(self, event):
        data = self.check_json_format()
        if data is None:
            return
        self.textEditor.SetValue(dumps(data, indent=2))

    def clear_json(self, event):
        flag = self._parent.dialog.confirmation_frame('确定清空Json文本吗?', parent=self)
        if flag != ID_YES:
            return
        self.textEditor.SetValue('{\n  \n}')

    def apply_json(self, event):
        data = self.check_json_format()
        if data is None:
            return
        self.user_saved_dict = data
        self.user_saved_json = self.textEditor.GetValue()
        self.EndModal(ID_OK)

    def close_dialog(self, event: 'CloseEvent'):
        flag = self._parent.dialog.confirmation_frame('是否保存当前的Json文本?', parent=self)
        if flag == ID_NO:
            self.EndModal(ID_CANCEL)
        elif flag == ID_YES:
            self.apply_json(event)
        else:
            event.Veto()
