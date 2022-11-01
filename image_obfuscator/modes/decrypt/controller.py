"""
Author       : noeru_desu
Date         : 2022-04-17 13:38:35
LastEditors  : noeru_desu
LastEditTime : 2022-08-13 15:08:27
"""
from typing import TYPE_CHECKING, Optional

from image_obfuscator.modes.encrypt.controller import EncryptModeController

if TYPE_CHECKING:
    from image_obfuscator.modes.base import ModeConstants
    from image_obfuscator.modes.decrypt.panel import ProcSettingsPanel


class DecryptModeController(EncryptModeController):
    "控制器"
    __slots__ = ()
    _instance: Optional['DecryptModeController'] = None
    mode_constants: 'ModeConstants' = ...
    settings_panel: 'ProcSettingsPanel'

    @property
    def core_version(self) -> int:
        return self.settings_panel.coreVersion.GetValue()

    @core_version.setter
    def core_version(self, v: int):
        self.settings_panel.coreVersion.SetValue(v)

    @property
    def orig_width(self) -> int:
        return self.settings_panel.origWidth.GetValue()

    @orig_width.setter
    def orig_width(self, v: int):
        self.settings_panel.origWidth.SetValue(v)

    @property
    def orig_height(self) -> int:
        return self.settings_panel.origHeight.GetValue()

    @orig_height.setter
    def orig_height(self, v: int):
        self.settings_panel.origHeight.SetValue(v)
