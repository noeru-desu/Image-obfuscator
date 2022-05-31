"""
Author       : noeru_desu
Date         : 2022-05-28 18:35:11
LastEditors  : noeru_desu
LastEditTime : 2022-05-31 06:29:01
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
        self.refresh_preview(event)

    def toggle_xor_panel_switch(self, event: 'CommandEvent'):
        self.xorPanel.Enable(event.IsChecked())
        self.refresh_preview(event)

    def update_noise_factor_num(self, event: 'CommandEvent' = None):
        self.noiseFactorNum.Label = str(self.noiseFactor.Value)

    def refresh_preview(self, event):
        self.TopLevelParent.refresh_preview(event)
