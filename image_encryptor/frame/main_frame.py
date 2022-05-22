"""
Author       : noeru_desu
Date         : 2021-10-22 18:15:34
LastEditors  : noeru_desu
LastEditTime : 2022-05-15 12:11:52
Description  : 覆写窗口
"""
from atexit import register as at_exit
from concurrent.futures import ThreadPoolExecutor
from functools import cached_property
from inspect import isroutine
from multiprocessing import cpu_count
from os import getcwd
from typing import TYPE_CHECKING

from wx import (ACCEL_CTRL, ACCEL_NORMAL, WXK_DELETE, WXK_F5, AcceleratorEntry,
                AcceleratorTable, App)
from wx.core import EmptyString

from image_encryptor.constants import (BRANCH, EXTENSION_KEYS_STRING,
                                       SUB_VERSION_NUMBER, VERSION_INFO,
                                       VERSION_NUMBER, VERSION_TYPE)
from image_encryptor.frame.controls import (Controls, SegmentTrigger, Settings,
                                            SettingsManager)
from image_encryptor.frame.design_frame import MainFrame as MF
from image_encryptor.frame.dialog import Dialog
from image_encryptor.frame.drag_importer import DragLoadingFile, DragSavingPath
from image_encryptor.frame.image_loader import ImageLoader
from image_encryptor.frame.image_saver import ImageSaver
from image_encryptor.frame.preview_generator import PreviewGenerator
from image_encryptor.frame.tree_manager import TreeManager
from image_encryptor.modules.decorator import catch_exc_for_frame_method
from image_encryptor.modules.password_verifier import PasswordDict
from image_encryptor.utils.logger import Logger
from image_encryptor.utils.thread import ProcessTaskManager

# from image_encryptor.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from os import PathLike

    from wx import Window
    from image_encryptor.frame.tree_manager import ImageItem
    from image_encryptor.modules.argparse import Parameters


class MainFrame(MF):
    """
    主窗口类
    """
    __slots__ = (
        'startup_parameters', 'logger', 'controls', 'settings', 'dialog', 'universal_thread_pool',
        'password_dict', 'process_pool', 'tree_manager', 'image_loader', 'preview_generator',
        'image_saver', 'stop_loading_func', 'stop_reloading_func', 'image_item', 'run_path'
    )

    def __init__(self, parent: 'Window', startup_parameters: 'Parameters', run_path: 'PathLike[str]' = getcwd()):
        """
        Args:
            parent (Window): 父窗口, 可为`None`
            startup_parameters (Parameters): 启动参数实例
            run_path (str, optional): 运行路径. 默认为`os.getcwd()`.
        """
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.Disable()
        self.Show()
        if VERSION_TYPE > 0:
            self.SetTitle(f'Image Encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH}) {"[Not optimized]" if __debug__ else ""}')
        else:
            self.SetTitle(f'Image Encryptor GUI {VERSION_NUMBER} {"[Not optimized]" if __debug__ else ""}')
        self.logger = Logger('image-encryptor')
        for i in VERSION_INFO:
            self.logger.info(i)

        # 处理启动参数
        if startup_parameters.dark_mode:
            self.dark_mode()
        self.startup_parameters = startup_parameters

        # 各项实现或组件
        self.controls = Controls(self)
        self.settings = SettingsManager(self.controls)
        self.dialog = Dialog(self)
        self.universal_thread_pool = ThreadPoolExecutor(8, 'universal_thread_pool')
        self.password_dict = PasswordDict()
        self.process_pool = ProcessTaskManager(1 if cpu_count() < 4 else cpu_count() - 2)
        self.tree_manager = TreeManager(self, self.imageTreeCtrl, '已加载文件列表')
        self.image_loader = ImageLoader(self)
        self.preview_generator = PreviewGenerator(self)
        self.image_saver = ImageSaver(self)
        self.stop_loading_func = SegmentTrigger((self.set_stop_loading_signal, self.stop_loading), self.init_loading_btn)
        self.stop_reloading_func = SegmentTrigger((self.set_reloading_btn_text, self.set_stop_reloading_signal, self.stop_reloading), self.init_reloading_btn)

        # 同步启动参数至界面
        self.controls.redundant_cache_length = self.startup_parameters.maximum_redundant_cache_length
        self.controls.disable_cache = self.startup_parameters.disable_cache
        self.controls.low_memory_mode = self.startup_parameters.low_memory

        # 文件拖入
        self.imageTreeCtrl.SetDropTarget(DragLoadingFile(self))
        self.savingOptions.SetDropTarget(DragSavingPath(self))

        # hook
        at_exit(self.process_pool.shutdown, wait=False, cancel_futures=True)
        at_exit(self.universal_thread_pool.shutdown, wait=False, cancel_futures=True)

        # 快捷键
        self.SetAcceleratorTable(AcceleratorTable([
            AcceleratorEntry(ACCEL_NORMAL, WXK_DELETE, self.delBtn.Id),          # Del    - 删除选中的项目
            AcceleratorEntry(ACCEL_NORMAL, WXK_F5, self.manuallyRefreshBtn.Id),  # F5     - 手动刷新预览图
            AcceleratorEntry(ACCEL_CTRL, ord('d'), self.delBtn.Id),              # Ctrl+D - 删除选中的项目(同Del)
            AcceleratorEntry(ACCEL_CTRL, ord('r'), self.reloadingBtn.Id),        # Ctrl+R - 重载选中的项目
            AcceleratorEntry(ACCEL_CTRL, ord('s'), self.savingBtn.Id),           # Ctrl+S - 保存选中的项目
            AcceleratorEntry(ACCEL_CTRL, ord('o'), self.loadingFileBtn.Id),      # Ctrl+O - 打开图像
            AcceleratorEntry(ACCEL_CTRL, ord('v'), self.loadingClipboardBtn.Id)  # Ctrl+V - 从剪切板打开图像
        ]))

        # 准备工作
        self.run_path = run_path
        self.xorPanel.Disable()
        self.savingFormat.ToolTip = f'{self.savingFormat.GetToolTipText()}{EXTENSION_KEYS_STRING}'
        self.selectSavingPath.PickerCtrl.SetLabel('选择文件夹')

        self.image_item: 'ImageItem' = None

        self.logger.info('窗口初始化完成')

    @cached_property
    def get_frame_items(self):
        for i in set(dir(self)) - set(dir(MF)):
            target = getattr(self, i)
            if not isroutine(target) and hasattr(target, 'SetBackgroundColour'):
                yield target

    def dark_mode(self):
        self.SetBackgroundColour('Dark Grey')
        for i in self.get_frame_items:
            i.SetBackgroundColour('Dark Grey')
            i.SetForegroundColour('White')

    @classmethod
    def run(cls, startup_parameters: 'Parameters', path=getcwd()):
        """运行窗口

        Args:
            startup_parameters (Parameters): 启动参数实例
            run_path (str, optional): 运行路径. 默认为`os.getcwd()`.
        """
        app = App(useBestVisual=True)
        cls(None, startup_parameters, path).Enable()

        app.MainLoop()

    def add_password_dict(self, password: str, dialog_parent: 'Window' = ...) -> bool:
        """添加密码到密码字典

        Args:
            password (str): 需要添加的密码
            dialog_parent (Window, optional): 对话框的父窗口. 默认为`MainFrame`

        Returns:
            bool: 添加成功则返回`True`
        """
        try:
            self.password_dict[self.password_dict.get_validation_field_base85(password)] = password
            self.password_dict[self.password_dict.get_validation_field_base85(password, False)] = password
        except ValueError:
            self.dialog.async_error('密码长度超过AES加密限制, 请确保密码长度不超过32字节', '用于验证密码正确性的字符串生成时出现错误', parent=dialog_parent)
            return False
        else:
            return True

    def init_loading_btn(self):
        self.controls.loading_prograss = 0
        self.controls.loading_prograss_info = EmptyString
        self.controls.stop_loading_btn_text = '停止载入'

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
        self.controls.stop_loading_btn_text = '强制终止载入'

    def init_reloading_btn(self):
        self.controls.reloading_btn_text = '重载此项'

    def set_reloading_btn_text(self):
        self.controls.reloading_btn_text = '停止重载'

    def stop_reloading(self, force=True, dialog=True):
        if force:
            self.tree_manager.reloading_thread.interrupt_task()
            self.dialog.async_warning('已强制终止重载操作')
        elif dialog:
            self.dialog.async_warning('已停止重载操作')
        self.tree_manager.stop_reloading_signal = False
        self.stop_loading_func.init()

    def set_stop_reloading_signal(self):
        self.tree_manager.stop_reloading_signal = True
        self.controls.stop_loading_btn_text = '强制终止重载'

    @catch_exc_for_frame_method
    def apply_settings_to_all(self, settings_list: list[str] = ...):
        """将当前加密设置应用到全部

        Args:
            settings_list (list[str], optional): 需要同步的加密设置属性名. 默认为全部加密设置
        """
        if settings_list is Ellipsis:
            properties_tuple = self.settings.all.properties_tuple
            for i in self.tree_manager.all_image_item_data:
                i.settings = Settings(self.controls, properties_tuple)
        else:
            settings = ((i, getattr(self.image_item, i)) for i in settings_list)
            for i in self.tree_manager.all_image_item_data:
                for n, v in settings:
                    setattr(i, n, v)
