"""
Author       : noeru_desu
Date         : 2022-05-28 18:35:11
LastEditors  : noeru_desu
LastEditTime : 2022-06-25 20:11:49
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.encrypt.auto_generated_panel import ProcSettingsPanel as BaseProcSettingsPanel

# from image_encryptor.utils.debugging_utils import gen_slots_str

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame
    from wx import CommandEvent


class ProcSettingsPanel(BaseProcSettingsPanel):
    __slots__ = ()
    TopLevelParent: 'MainFrame'

    # def __init__(self, *args):
    #     o_args = set(dir(self))
    #     super().__init__(*args)
    #     n_args = set(dir(self))
    #     gen_slots_str(n_args - o_args)

    def toggle_factor_slider_switch(self, event: 'CommandEvent'):
        self.noiseFactor.Enable(event.IsChecked())
        self.settings_changed(event)

    def toggle_xor_panel_switch(self, event: 'CommandEvent'):
        self.xorPanel.Enable(event.IsChecked())
        self.settings_changed(event)

    def update_noise_factor_num(self, event: 'CommandEvent' = None):
        self.noiseFactorNum.SetLabelText(str(self.noiseFactor.GetValue()))

    def settings_changed(self, event):
        self.TopLevelParent.settings_changed(event)