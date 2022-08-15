"""
Author       : noeru_desu
Date         : 2022-05-28 18:35:11
LastEditors  : noeru_desu
LastEditTime : 2022-08-15 08:44:02
Description  : 
"""
from typing import TYPE_CHECKING

from wx import BLACK, WHITE

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
