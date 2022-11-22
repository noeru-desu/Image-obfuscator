"""
Author       : noeru_desu
Date         : 2022-11-20 18:35:11
LastEditors  : noeru_desu
LastEditTime : 2022-11-22 13:34:11
"""
from os.path import isfile
from traceback import format_exc
from typing import TYPE_CHECKING

from wx import FileDropTarget, ID_CANCEL, ID_APPLY

from image_obfuscator.frame.controller import ProgressBar
from image_obfuscator.modes.lsb_steganography.auto_generated_panel import ProcSettingsPanel as BaseProcSettingsPanel
from image_obfuscator.modes.lsb_steganography.auto_generated_panel import DetectLsbDialog as DLD
from image_obfuscator.modes.lsb_steganography.main import detect
from image_obfuscator.modes.base import BaseModeSettingsPanel
from image_obfuscator.utils.thread import ThreadManager

# from image_obfuscator.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from image_obfuscator.modes.base import ModeConstants
    from image_obfuscator.modes.lsb_steganography.controller import LsbModeController


class ProcSettingsPanel(BaseModeSettingsPanel, BaseProcSettingsPanel):
    __slots__ = ()
    mode_controller: 'LsbModeController'

    def __init__(self, *args):
        # o_args = set(dir(self))
        super().__init__(*args)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.insideFile.PickerCtrl.SetLabel('选择需隐写文件')
        self.SetDropTarget(DragInsideFile(self))

    def settings_changed(self, event):
        self.main_frame.settings_changed(event)

    def recal_lsb_ratio(self, event):
        if self.mode_controller.can_cal_lsb_ratio():
            self.main_frame.image_item.settings.lsb_ratio = self.mode_controller.recal_and_display_lsb_ratio()
        self.main_frame.settings_changed(event)

    def auto_zoom_in_changed(self, event):
        self.mode_controller.refresh_lsb_ratio_color()
        self.main_frame.settings_changed(event)

    def detect_lsb(self, event):
        if self.main_frame.image_item is None:
            self.main_frame.dialog.warning('请先载入图像', '没有图像可供检测')
            return
        dialog = DetectLsbDialog(self.main_frame)
        with dialog:
            code = dialog.ShowModal()
        if code == ID_APPLY:
            self.main_frame.image_item.settings.lsb_mode = self.mode_controller.lsb_mode = 1
            self.main_frame.image_item.settings.lsb_num = self.mode_controller.lsb_num = dialog.lsb_num
            self.main_frame.image_item.settings.use_alpha = self.mode_controller.use_alpha = dialog.use_alpha
            if self.mode_controller.can_cal_lsb_ratio():
                self.main_frame.image_item.settings.lsb_ratio = self.mode_controller.recal_and_display_lsb_ratio()
            self.main_frame.refresh_preview(...)


class DetectLsbDialog(DLD):
    __slots__ = ('success', 'lsb_num', 'use_alpha', 'running', 'bar')
    mode_constants: 'ModeConstants'
    detect_thread = ThreadManager('detect-thread', True)

    def __init__(self, parent):
        # o_args = set(dir(self))
        super().__init__(parent)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.SetSize(self.BestSize)
        self.running = False
        self.success = False
        self.no_error = False
        self.lsb_num: int = ...
        self.use_alpha: bool = ...
        self.bar = ProgressBar(self.gauge)
        self.SetReturnCode(ID_CANCEL)

    def add_progress(self):
        self.bar.add()
        self.info.SetLabelText(f'正在探测可能的设置({self.bar.value}/16)')

    def start_detect(self, event):
        self.running = True
        self.startDetectBtn.Disable()
        self.bar.next_step(16)
        self.detect_thread.start_new(self._start_detect)

    def _start_detect(self):
        image = self.mode_constants.main_frame.image_item.cache.loaded_image
        self.info.SetLabelText('正在探测可能的设置(0/16)')
        for num in range(1, 9):
            if self.success:
                break
            for alpha in (True, False):
                n = detect(image, num, alpha)
                self.add_progress()
                if n == 0:
                    continue
                self.lsb_num: int = num
                self.use_alpha: bool = alpha
                if n == 1:
                    self.no_error = True
                elif n == 2:
                    self.success = True
                    break
        if self.success:
            self.bar.finish()
            self.info.SetLabelText('已探测到可用的LSB提取设置')
        elif self.no_error:
            self.info.SetLabelText('仅探测到未出错的LSB提取设置, 可能无法提取')
        else:
            self.info.SetLabelText('没有探测到可用的LSB提取设置')
            return
        self.applyBtn.Enable()

    def cancel(self, event):
        self.detect_thread.kill()
        self.EndModal(ID_CANCEL)

    def apply(self, event):
        self.EndModal(ID_APPLY)


class DragInsideFile(FileDropTarget):
    __slots__ = ('panel',)

    def __init__(self, panel: 'ProcSettingsPanel'):
        super().__init__()
        self.panel = panel

    def OnDropFiles(self, x, y, filenames):
        try:
            filenames = tuple(filter(isfile, filenames))
            if not filenames:
                self.panel.main_frame.dialog.async_warning('只可拖放单个文件')
                return True
            elif len(filenames) > 1:
                self.panel.main_frame.dialog.async_warning(f'共拖放了{len(filenames)}个文件，仅接受第一个文件({filenames[0]})')
            file = filenames[0]
            self.panel.mode_controller.inside_file = file
            self.panel.main_frame.sync_setting(self.panel.insideFile)
            if self.panel.mode_controller.can_cal_lsb_ratio():
                self.panel.main_frame.image_item.settings.lsb_ratio = self.panel.mode_controller.recal_and_display_lsb_ratio()
        except RuntimeError:
            return False
        except Exception:
            self.panel.main_frame.dialog.error(format_exc())
        else:
            return True
