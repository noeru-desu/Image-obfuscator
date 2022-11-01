"""
Author       : noeru_desu
Date         : 2022-05-28 18:35:11
LastEditors  : noeru_desu
LastEditTime : 2022-08-08 21:07:40
"""
from typing import TYPE_CHECKING

from image_obfuscator.constants import EA_VERSION
from image_obfuscator.modes.decrypt.auto_generated_panel import ProcSettingsPanel as BaseProcSettingsPanel
from image_obfuscator.modes.base import BaseModeSettingsPanel

# from image_obfuscator.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from wx import CommandEvent


class ProcSettingsPanel(BaseModeSettingsPanel, BaseProcSettingsPanel):
    __slots__ = ()

    def __init__(self, *args):
        # o_args = set(dir(self))
        super().__init__(*args)
        # n_args = set(dir(self))
        # gen_slots_str(n_args - o_args)
        self.coreVersion.SetMax(EA_VERSION)
        self.coreVersion.SetValue(EA_VERSION)

    def settings_changed(self, event):
        self.main_frame.settings_changed(event)

    def toggle_factor_slider_switch(self, event: 'CommandEvent'):
        self.noiseFactor.Enable(event.IsChecked())
        self.main_frame.settings_changed(event)

    def toggle_xor_panel_switch(self, event: 'CommandEvent'):
        self.xorPanel.Enable(event.IsChecked())
        self.noiseFactor.Enable(self.noiseXor.IsChecked())
        self.main_frame.settings_changed(event)

    def update_noise_factor_num(self, event: 'CommandEvent' = None):
        self.noiseFactorNum.SetLabelText(str(self.noiseFactor.GetValue()))
