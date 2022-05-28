"""
Author       : noeru_desu
Date         : 2022-04-17 08:22:01
LastEditors  : noeru_desu
LastEditTime : 2022-05-28 19:05:07
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.base import BaseModeInterface
from image_encryptor.modes.decrypt.main import normal_gen
from image_encryptor.modes.decrypt.settings import EncryptionParameters
from image_encryptor.modes.encrypt.controller import EncryptModeController
from image_encryptor.modes.encrypt.panel import ProcSettingsPanel

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class ModeInterface(BaseModeInterface):
    __slots__ = (
        'frame', 'mode_name', 'mode_qualname', 'decryption_mode', 'requires_encryption_parameters',
        'encryption_parameters_cls', 'enable_settings_panel', 'settings_panel', 'settings_controller',
        'gen_preview'
    )
    settings_panel_cls = ProcSettingsPanel

    def __init__(self, frame: 'MainFrame', mode_id: int):
        self.frame = frame
        self.mode_name = '解密模式'
        self.mode_qualname = 'builtin.decrypt.v1'
        self.decryption_mode = True
        self.requires_encryption_parameters = True
        self.encryption_parameters_cls = EncryptionParameters
        self.enable_settings_panel = False
        self.settings_panel = frame.mode_manager.instance_settings_panel(self.settings_panel_cls)
        self.settings_controller = EncryptModeController(frame, self.settings_panel)
        self.gen_preview = normal_gen
