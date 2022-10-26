"""
Author       : noeru_desu
Date         : 2022-01-11 21:03:00
LastEditors  : noeru_desu
LastEditTime : 2022-10-26 11:05:11
Description  : 对话框相关
"""
from base64 import b85decode
from json import JSONDecodeError, dumps, loads
from pickle import loads as pickle_loads
from threading import Lock
from typing import TYPE_CHECKING, Optional, Sequence

from pyperclip import copy as clipboard_copy, paste as clipboard_paste
from wx import (ALIGN_RIGHT, ALL, CANCEL, DIRP_CHANGE_DIR, DIRP_DEFAULT_STYLE,
                DIRP_DIR_MUST_EXIST, EVT_BUTTON, FD_CHANGE_DIR,
                FD_DEFAULT_STYLE, FD_FILE_MUST_EXIST, FD_OPEN, FD_PREVIEW,
                HELP, HORIZONTAL, ICON_ERROR, ICON_INFORMATION, ICON_QUESTION,
                ICON_WARNING, ID_CANCEL, ID_NO, ID_OK, ID_YES, RED,
                STAY_ON_TOP, WHITE, YES_NO, BoxSizer, Button, CallAfter,
                Colour, DirDialog, FileDialog, IsMainThread, MessageDialog)
from wx.stc import (STC_JSON_BLOCKCOMMENT, STC_JSON_COMPACTIRI,
                    STC_JSON_DEFAULT, STC_JSON_ERROR, STC_JSON_ESCAPESEQUENCE,
                    STC_JSON_KEYWORD, STC_JSON_LDKEYWORD, STC_JSON_LINECOMMENT,
                    STC_JSON_NUMBER, STC_JSON_OPERATOR, STC_JSON_PROPERTYNAME,
                    STC_JSON_STRING, STC_JSON_STRINGEOL, STC_JSON_URI,
                    STC_LEX_JSON)

from image_obfuscator.frame.design_frame import JsonEditorDialog as JED
from image_obfuscator.frame.design_frame import ModifiedChoiceDialog as MCD
from image_obfuscator.frame.design_frame import MultiLineTextEntryDialog as MLTED
from image_obfuscator.frame.design_frame import PasswordDialog as PD
from image_obfuscator.frame.design_frame import TextDisplayDialog as TDD
from image_obfuscator.modules.version_adapter import check_version
from image_obfuscator.utils.thread import SingleThreadExecutor

# from image_obfuscator.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from os import PathLike

    from image_obfuscator.frame.events import MainFrame
    from wx import CloseEvent, CommandEvent, Window


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

    def json_editor_dialog(self, title_text: str = '编辑Json文本', extra_info: str = '', extra_link: str = '', extra_link_info: str = '', json_text: str = '{\n\t\n}', parent: 'Window' = ...):
        if parent is Ellipsis:
            parent = self.frame
        dialog = JsonEditorDialog(parent, title_text, extra_info, extra_link, extra_link_info, json_text)
        with dialog:
            return_code = dialog.ShowModal()
        if return_code == ID_CANCEL:
            return None
        elif return_code == ID_OK:
            return dialog.user_saved_json, dialog.user_saved_dict

    def text_display_dialog(self, title: str = '文本展示', extra_info: str = '', main_text: str = '', parent: 'Window' = ...):
        if parent is Ellipsis:
            parent = self.frame
        dialog = TextDisplayDialog(parent, title, extra_info, main_text)
        with dialog:
            dialog.ShowModal()

    def encryption_attributes_b85_entry_dialog(self):
        dialog = EncryptionAttributesB85EntryDialog(self.frame, '请输入序列化后的加密参数字段', '请输入序列化后的加密参数字段')
        with dialog:
            return_code = dialog.ShowModal()
        return dialog.succeeded if return_code == ID_OK else None

    def choose_action_dialog(self, message: str, title: str = '选择操作', actions: Sequence[str] = ('是', '否'), default_action: int = ..., recordable=True, parent: 'Window' = ...):
        if parent is Ellipsis:
            parent = self.frame
        return ChooseActionDialog(parent, message, title, actions, default_action, recordable)

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
    def standalone_dialog(message: str, title: str, style: int = None) -> int:
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


# 样式与Scintilla的json.settings中的配置大部分相同
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
    __slots__ = ('_parent', 'target_json_type', 'user_saved_json', 'user_saved_dict', 'o_json_text')

    def __init__(self, parent: 'MainFrame', title_text: str = '编辑Json文本', extra_info: str = '', extra_link: str = '', extra_link_info: str = '', json_text: str = '{\n\t\n}', target_json_type=dict):
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self._parent = parent
        self.target_json_type = target_json_type
        self.o_json_text = json_text
        self.user_saved_json: Optional[str] = None
        self.user_saved_dict: Optional[dict] = None
        self.titleText.SetLabelText(title_text)
        self.extraInfoText.SetLabelText(extra_info)
        self.extraLink.SetLabelText(extra_link_info)
        self.extraLink.SetURL(extra_link)
        self.textEditor.SetValue(json_text)
        self.SetReturnCode(ID_CANCEL)
        self.set_style()
        self.Layout()

    def set_style(self):
        # 样式与Scintilla的json.settings中的配置相同(除特殊注释处)
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
        value = self.textEditor.GetValue()
        if not value:
            self.textEditor.SetValue('{\n\t\n}')
            value = '{\n\t\n}'
        try:
            data = loads(value)
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
        self.textEditor.SetValue('{\n\t\n}')

    def apply_json(self, event):
        data = self.check_json_format()
        if data is None:
            return
        self.user_saved_dict = data
        self.user_saved_json = self.textEditor.GetValue()
        self.EndModal(ID_OK)

    def close_dialog(self, event: 'CloseEvent'):
        if self.o_json_text == self.textEditor.GetValue():
            self.EndModal(ID_CANCEL)
            return
        flag = self._parent.dialog.confirmation_frame('是否保存当前的Json文本?', parent=self)
        if flag == ID_NO:
            self.EndModal(ID_CANCEL)
        elif flag == ID_YES:
            self.apply_json(event)
        else:
            event.Veto()


class TextDisplayDialog(TDD):
    __slots__ = ()

    def __init__(self, parent: 'MainFrame', title: str = '文本展示', extra_info: str = '', main_text: str = ''):
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.SetTitle(title)
        self.extraInfo.SetLabelText(extra_info)
        self.text.SetValue(main_text)
        self.SetReturnCode(ID_CANCEL)
        self.Layout()

    def copy_text(self, event):
        clipboard_copy(self.text.GetValue())
        self.actionTip.Show()
        self.Layout()


class MultiLineTextEntryDialog(MLTED):
    __slots__ = ('user_input', '_parent')
    _parent: 'MainFrame'

    def __init__(self, parent: 'MainFrame', title: str = '文本输入', extra_info: str = ''):
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self._parent = parent
        self.SetTitle(title)
        self.extraInfo.SetLabelText(extra_info)
        self.SetReturnCode(ID_CANCEL)
        self.Layout()
        self.user_input = None

    def confirm(self, event):
        self.user_input = self.text.GetValue()

    def cancel(self, event):
        self.EndModal(ID_CANCEL)


class EncryptionAttributesB85EntryDialog(MultiLineTextEntryDialog):
    __slots__ = ('succeeded',)

    def __init__(self, parent: 'MainFrame', title: str = '文本输入', extra_info: str = ''):
        super().__init__(parent, title, extra_info)
        clipboard = clipboard_paste()
        try:
            data = b85decode(clipboard)
        except Exception:
            return
        else:
            if data.startswith(b'\x80'):
                self.text.SetValue(clipboard)

    def confirm(self, event):
        text = self.text.GetValue().rstrip('\r\n\t\000')
        if not text:
            self._parent.dialog.warning('请输入加密参数', parent=self)
            return
        try:
            attributes_dict = pickle_loads(b85decode(text))
        except Exception as e:
            self._parent.dialog.warning(f'{repr(e)}\n加载当前输入的加密参数时出现错误, 请检查输入的序列化字段是否正确且完整', '加载当前输入的加密参数时出现问题', parent=self)
            return
        attributes_dict, err = check_version(attributes_dict)
        if err is not None:
            self._parent.dialog.warning(f'检查当前输入的加密参数时出现错误: {err}', parent=self)
            return
        self.succeeded = self._parent.image_item.load_encryption_attributes(attributes_dict, err, False)
        self.EndModal(ID_OK)


class ModifiedChoiceDialog(MCD):
    __slots__ = (
        'action', 'record'
    )

    def __init__(self, parent: 'Window', message: str, title: str = '选择操作', actions: Sequence[str] = ('是', '否'), default_action: int = ..., recordable=True):
        super().__init__(parent)
        if not recordable:
            self.remember.Hide()
        self.SetTitle(title)
        self.info.SetLabelText(message)
        sizer = BoxSizer(HORIZONTAL)
        for i, j in enumerate(actions):
            btn = Button(self, label=j)
            sizer.Add(btn, 0, ALL, 2)
            btn.Bind(EVT_BUTTON, self.choice)
            btn.action = i
        self.GetSizer().Add(sizer, 0, ALIGN_RIGHT, 5)
        self.Layout()
        self.SetSize(self.GetBestSize())
        if default_action is Ellipsis:
            default_action = len(actions) - 1
        self.action = default_action
        self.record = False
        self.SetReturnCode(ID_CANCEL)

    def choice(self, event: 'CommandEvent'):
        self.action = event.GetEventObject().action
        self.record = self.remember.GetValue()
        self.EndModal(ID_OK)


class ChooseActionDialog(object):
    __slots__ = (
        'parent', 'message', 'title', 'actions', 'default_action', 'record',
        '_dialog', 'lock', 'recordable'
    )

    def __init__(self, parent: 'Window', message: str, title: str = '选择操作', actions: Sequence[str] = ('是', '否'), default_action: int = ..., recordable=True) -> None:
        self.parent = parent
        self.message = message
        self.title = title
        self.actions = actions
        self.default_action = default_action
        self.recordable = recordable
        self.record = None
        self._dialog = None
        self.lock = Lock()

    def _open_dialog(self, parent, message, title, default_action, recordable):
        self._dialog = ModifiedChoiceDialog(parent, message, title, self.actions, default_action, recordable)
        with self._dialog:
            self._dialog.ShowModal()
        self.lock.release()

    def open_dialog(self, parent: 'Window' = ..., message: str = ..., title: str = ..., default_action: int = ..., recordable: bool = ...):
        if self.record is not None:
            return self.record
        if parent is Ellipsis:
            parent = self.parent
        if message is Ellipsis:
            message = self.message
        if title is Ellipsis:
            title = self.title
        if default_action is Ellipsis:
            default_action = self.default_action
        if recordable is Ellipsis:
            recordable = self.recordable
        if IsMainThread():
            self._open_dialog(parent, message, title, default_action, recordable)
        else:
            self.lock.acquire()
            CallAfter(self._open_dialog, parent, message, title, default_action, recordable)
            self.lock.acquire()
            self.lock.release()
        if self._dialog.record:
            self.record = self._dialog.action
        return self._dialog.action
