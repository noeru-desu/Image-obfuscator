"""
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2023-03-27 22:21:01
"""
from atexit import register as at_exit
from concurrent.futures import ThreadPoolExecutor
from functools import cached_property
from inspect import isroutine
from os import getcwd
from traceback import format_exc
from typing import TYPE_CHECKING, Optional, Union

from wx import (ACCEL_CTRL, ACCEL_NORMAL, CURSOR_ARROW, CURSOR_WAIT, WXK_DELETE, WXK_F5, VERTICAL, HORIZONTAL, AcceleratorEntry,
                AcceleratorTable, App, Cursor, CallAfter, ICON_ERROR, STAY_ON_TOP)
from wx.core import EmptyString

from image_obfuscator.constants import (EXTENSION_KEYS_STRING, FULL_VERSION_STRING,
                                       LOGGER_LEVEL, SHORT_VERSION_STRING,
                                       VERSION_INFO, VERSION_TYPE)
from image_obfuscator.frame.controller import Controller, SegmentTrigger
from image_obfuscator.frame.design_frame import MainFrame as MF
from image_obfuscator.frame.dialog import Dialog
from image_obfuscator.frame.drag_importer import DragLoadingFile, DragSavePath
from image_obfuscator.frame.file_item import ImageItemCache, Item, PreviewCache
from image_obfuscator.frame.image_loader import ImageDiskCache, ImageLoader
from image_obfuscator.frame.image_saver import ImageSaver
from image_obfuscator.frame.mode_manager import ModeManager
from image_obfuscator.frame.preview_generator import PreviewGenerator
from image_obfuscator.frame.tree_manager import TreeManager
from image_obfuscator.frame.config import ConfigManager
from image_obfuscator.modes.base import EmptySettings, ModeConstants
from image_obfuscator.modes.mirage_tank.settings import Settings as MirageTankSettings
from image_obfuscator.modules.argparse import Options
from image_obfuscator.modules.decorator import catch_exc_for_frame_method
from image_obfuscator.modules.password_verifier import PasswordDict
from image_obfuscator.utils.logger import Logger
# TODO from image_obfuscator.utils.thread import ProcessTaskManager

# from image_obfuscator.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from os import PathLike

    from wx import Window
    from image_obfuscator.frame.tree_manager import ImageItem, FolderItem


class MainFrame(MF):
    """
    主窗口类
    """
    __slots__ = (
        'program_options', 'logger', 'controller', 'settings', 'dialog', 'universal_thread_pool',
        'password_dict', 'process_pool', 'tree_manager', 'image_loader', 'preview_generator', 'folder_item',
        'image_saver', 'stop_loading_func', 'stop_reloading_func', 'image_item', 'run_path','mode_manager',
        'config', 'disable_switching_image', 'mode_fallback_dialog', 'image_disk_cache', 'temp_dir_in_use'
    )

    def __init__(self, parent: 'Window', run_path: 'PathLike[str]' = getcwd()):
        """
        Args:
            parent (Window): 父窗口, 可为`None`
            run_path (str, optional): 运行路径. 默认为`os.getcwd()`.
        """
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.Disable()
        if VERSION_TYPE > 0:
            self.SetTitle(f'Image Obfuscator GUI {FULL_VERSION_STRING}')
        else:
            self.SetTitle(f'Image Obfuscator GUI {SHORT_VERSION_STRING}')
        self.Show()
        self.logger = Logger('image-obfuscator', LOGGER_LEVEL)
        if not __debug__:
            for i in VERSION_INFO[-2:]:
                print(i)
        for i in VERSION_INFO:
            self.logger.info(i)
        self.image_item: Optional['ImageItem'] = None
        self.folder_item: Optional['FolderItem'] = None
        self.program_options = Options()

        # 设置部分类的常量
        Item.frame = self
        PreviewCache.program_options = self.program_options

        # 实例化各功能实现
        self.dialog = Dialog(self)
        self.controller = Controller(self)
        ModeConstants.main_frame = self
        ModeConstants.main_controller = self.controller
        EmptySettings.create_settings_mapping()
        self.config = ConfigManager(self)
        self.config.load_frame_settings()
        self.mode_manager = ModeManager(self)
        self.mode_manager.load_builtin_modes()
        self.config.init()
        self.config.apply_frame_settings()
        self.password_dict = PasswordDict()
        if self.program_options.record_password_dict:
            self.config.load_password_dict()
        self.universal_thread_pool = ThreadPoolExecutor(8, 'universal_thread_pool')
        # TODO self.process_pool = ProcessTaskManager(1 if cpu_count() < 4 else cpu_count() - 2)
        self.tree_manager = TreeManager(self, self.imageTreeCtrl, '已加载文件列表')
        self.image_loader = ImageLoader(self)
        self.image_disk_cache = ImageDiskCache(self)
        self.preview_generator = PreviewGenerator(self)
        self.image_saver = ImageSaver(self)
        self.stop_loading_func = SegmentTrigger((self.set_stop_loading_signal, self.stop_loading), self.init_loading_btn)
        self.stop_reloading_func = SegmentTrigger((self.set_reloading_btn_text, self.set_stop_reloading_signal, self.stop_reloading), self.init_reloading_btn)

        # 部分记忆弹窗
        self.mode_fallback_dialog = self.dialog.choose_action_dialog('所选模式无法在未选中图像时选择', '提示', ('确定',), 0, record_btn_label='不再提示')

        # 同步程序设置至界面
        if self.program_options.dark_mode:
            self.dark_mode()
        ImageItemCache.lru_cache_recorder.maxlen = MirageTankSettings.outside_image_cache.maxlen = self.program_options.maximum_orig_image_cache
        PreviewCache.lru_cache_recorder.maxlen = self.program_options.maximum_proc_result_cache
        self.program_options.apply_to_interface(self.controller)

        # 文件拖入
        self.imageTreeCtrl.SetDropTarget(DragLoadingFile(self))
        self.saveOptions.SetDropTarget(DragSavePath(self))

        # 退出时操作
        # TODO at_exit(self.process_pool.shutdown, wait=False, cancel_futures=True)
        at_exit(self.universal_thread_pool.shutdown, wait=False, cancel_futures=True)

        # 快捷键
        self.SetAcceleratorTable(AcceleratorTable([
            AcceleratorEntry(ACCEL_NORMAL, WXK_DELETE, self.delBtn.Id),          # Del    - 删除选中的项目
            AcceleratorEntry(ACCEL_NORMAL, WXK_F5, self.manuallyRefreshBtn.Id),  # F5     - 手动刷新预览图
            AcceleratorEntry(ACCEL_CTRL, ord('d'), self.delBtn.Id),              # Ctrl+D - 删除选中的项目(同Del)
            AcceleratorEntry(ACCEL_CTRL, ord('r'), self.reloadingBtn.Id),        # Ctrl+R - 重载选中的项目
            AcceleratorEntry(ACCEL_CTRL, ord('s'), self.saveBtn.Id),             # Ctrl+S - 保存选中的项目
            AcceleratorEntry(ACCEL_CTRL, ord('o'), self.loadingFileBtn.Id),      # Ctrl+O - 打开图像
            AcceleratorEntry(ACCEL_CTRL, ord('v'), self.loadingClipboardBtn.Id)  # Ctrl+V - 从剪切板打开图像
        ]))

        # 准备工作
        self.run_path = run_path
        self.SettingsSourceUsed.EnableItem(1, False)
        self.SettingsSourceUsed.EnableItem(2, False)
        self.saveFormat.ToolTip = f'{self.saveFormat.GetToolTipText()}{EXTENSION_KEYS_STRING}'
        self.selectSavePath.PickerCtrl.SetLabel('选择文件夹')
        self.disable_switching_image = False
        self.temp_dir_in_use = self.program_options.temp_dir

        self.logger.info('窗口初始化完成')
        # self.Show()

        if self.program_options.test:
            CallAfter(self.exit, ...)

    @cached_property
    def get_frame_items(self):
        for i in set(dir(self)) - set(dir(MF)):
            if not hasattr(self, i):
                continue
            target = getattr(self, i)
            if not isroutine(target) and hasattr(target, 'SetBackgroundColour'):
                yield target

    def dark_mode(self):
        self.SetBackgroundColour('Dark Grey')
        for i in self.get_frame_items:
            i.SetBackgroundColour('Dark Grey')
            i.SetForegroundColour('White')

    @classmethod
    def run(cls, path=getcwd()):
        """运行窗口

        Args:
            program_options (Parameters): 启动参数实例
            run_path (str, optional): 运行路径. 默认为`os.getcwd()`.
        """
        app = App()
        try:
            cls(None, path).Enable()
        except BaseException:
            Dialog.standalone_dialog(format_exc(), '初始化窗口时出现错误', ICON_ERROR | STAY_ON_TOP)
            exit(3)

        app.MainLoop()

    def set_preview_layout(self, sizer_orientation: Union['VERTICAL', 'HORIZONTAL']):
        self.imagePanel.Sizer.SetOrientation(sizer_orientation)
        self.set_preview_plane_size()

    def set_preview_plane_size(self):
        size = self.controller.preview_plane_size
        self.importedBitmapPanel.SetInitialSize(size)
        self.previewedBitmapPanel.SetInitialSize(size)
        self.imagePanel.Layout()

    def add_password_dict(self, password: str, dialog_parent: 'Window' = ...) -> bool:
        """添加密码到密码字典

        Args:
            password (str): 需要添加的密码
            dialog_parent (Window, optional): 对话框的父窗口. 默认为`MainFrame`

        Returns:
            bool: 添加成功则返回`True`
        """
        if password in self.password_dict.values():
            return True
        try:
            self.password_dict[self.password_dict.get_validation_field_base85(password)] = password
            self.password_dict[self.password_dict.get_validation_field_base85(password, False)] = password
        except ValueError:
            self.dialog.async_error('密码长度超过AES加密限制, 请确保密码长度不超过32字节', '用于验证密码正确性的字符串生成时出现错误', parent=dialog_parent)
            return False
        else:
            return True

    def init_loading_btn(self):
        self.controller.loading_progress = 0
        self.controller.loading_progress_info = EmptyString
        self.controller.stop_loading_btn_text = '停止载入'

    def stop_loading(self, force=True):
        if force:
            self.image_loader.loading_thread.clear_task()
            self.image_loader.loading_thread.interrupt_task()
            self.image_loader.hide_loading_progress_plane()
            self.imageTreeCtrl.Enable()
            self.processingOptions.Enable()
            self.loadingPanel.Enable()
            self.dialog.async_warning('已强制终止载入文件')
        else:
            self.dialog.async_warning('已停止载入文件')
        self.image_loader.stop_loading_signal = False
        self.stop_loading_func.init()

    def set_stop_loading_signal(self):
        self.image_loader.loading_thread.clear_task()
        self.image_loader.stop_loading_signal = True
        self.controller.stop_loading_btn_text = '强制终止载入'

    def init_reloading_btn(self):
        self.controller.reloading_btn_text = '重载此项'

    def set_reloading_btn_text(self):
        self.controller.reloading_btn_text = '停止重载'

    def stop_reloading(self, force=True, dialog=True):
        if force:
            self.tree_manager.reloading_thread.interrupt_task()
            self.set_cursor(CURSOR_ARROW)
            self.dialog.async_warning('已强制终止重载操作')
        elif dialog:
            self.dialog.async_warning('已停止重载操作')
        self.tree_manager.stop_reloading_signal = False
        self.stop_loading_func.init()

    def set_stop_reloading_signal(self):
        self.tree_manager.stop_reloading_signal = True
        self.controller.stop_loading_btn_text = '强制终止重载'

    @catch_exc_for_frame_method
    def apply_settings_to_all(self):
        """将当前加密设置应用到全部"""
        proc_mode = self.controller.proc_mode_interface
        if not proc_mode.can_be_set_as_default_mode:
            if __debug__:
                raise ValueError('Operations not permitted by the current mode interface setting (can_be_set_as_default_mode)')
            return
        self.set_cursor(CURSOR_WAIT)
        self.disable_switching_image = True
        self.processingOptions.Disable()
        settings_tuple = self.controller.current_settings.settings_tuple
        for i in self.tree_manager.all_image_item_data:
            i.proc_mode = proc_mode
            i.settings.sync_from_tuple(settings_tuple)
        self.processingOptions.Enable()
        self.disable_switching_image = False
        self.set_cursor(CURSOR_ARROW)

    def set_cursor(self, cursor):
        self.SetCursor(Cursor(cursor))
