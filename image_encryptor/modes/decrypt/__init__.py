"""
Author       : noeru_desu
Date         : 2022-04-17 08:22:01
LastEditors  : noeru_desu
LastEditTime : 2022-07-23 19:51:47
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.base import BaseModeInterface
from image_encryptor.modes.decrypt.main import normal_gen, normal_gen_quietly
from image_encryptor.modes.decrypt.settings import EncryptionParameters
from image_encryptor.modes.encrypt.controller import EncryptModeController
from image_encryptor.modes.encrypt.panel import ProcSettingsPanel

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class ModeInterface(BaseModeInterface):
    __slots__ = (
        'frame', 'mode_name', 'mode_qualname', 'decryption_mode', 'requires_encryption_parameters',
        'encryption_parameters_cls', 'enable_settings_panel', 'settings_panel', 'settings_controller'
    )
    settings_panel_cls = ProcSettingsPanel
    enable_password = True
    file_name_suffix = ('-encrypted', '-decrypted')

    def __init__(self, frame: 'MainFrame', mode_id: int):
        self.frame = frame
        self.mode_name = '解密模式'
        self.mode_qualname = 'builtin.decrypt.v1'
        self.decryption_mode = True
        self.requires_encryption_parameters = True
        self.encryption_parameters_cls = EncryptionParameters
        self.enable_settings_panel = False
        self.settings_panel = frame.mode_manager.add_settings_panel(self.settings_panel_cls)
        self.settings_controller: 'EncryptModeController' = EncryptModeController(frame, self.settings_panel)
        super().__init__(frame, mode_id)

    def proc_image(self, *args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)
