"""
Author       : noeru_desu
Date         : 2022-05-28 18:35:11
LastEditors  : noeru_desu
LastEditTime : 2022-08-17 16:58:08
Description  : 
"""
from os.path import isfile
from traceback import format_exc
from typing import TYPE_CHECKING

from wx import BLACK, WHITE, FileDropTarget

from image_obfuscator.modes.mirage_tank.auto_generated_panel import ProcSettingsPanel as BaseProcSettingsPanel
from image_obfuscator.modes.base import BaseModeSettingsPanel

# from image_obfuscator.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from wx import CommandEvent
    from image_obfuscator.modes.mirage_tank.controller import MirageTankModeController


class ProcSettingsPanel(BaseModeSettingsPanel, BaseProcSettingsPanel):
    __slots__ = ()
    mode_controller: 'MirageTankModeController'

    def __init__(self, *args):
        # o_args = set(dir(self))
        super().__init__(*args)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.outsideImage.PickerCtrl.SetLabel('选择表图')
        self.outsideColorScale.Disable()
        self.insideColorScale.Disable()
        self.SetDropTarget(DragOutsideImage(self))

    def settings_changed(self, event):
        self.main_frame.settings_changed(event)

    def toggle_colorful_mode(self, event: 'CommandEvent'):
        self.outsideColorScale.Enable(event.IsChecked())
        self.insideColorScale.Enable(event.IsChecked())
        self.main_frame.settings_changed(event)

    def toggle_bg(self, event):
        if self.mode_controller.black_preview_bg:
            self.toggleBg.SetLabelText('切换至\n白底预览')
            self.main_controller.set_preview_panel_bg(BLACK)
        else:
            self.toggleBg.SetLabelText('切换至\n黑底预览')
            self.main_controller.set_preview_panel_bg(WHITE)


class DragOutsideImage(FileDropTarget):
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
            self.panel.mode_controller.outside_image_path = file
            self.panel.main_frame.sync_setting(self.panel.outsideImage)
        except RuntimeError:
            return False
        except Exception:
            self.panel.main_frame.dialog.error(format_exc())
        else:
            return True
