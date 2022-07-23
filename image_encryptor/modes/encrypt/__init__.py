"""
Author       : noeru_desu
Date         : 2022-04-16 17:43:06
LastEditors  : noeru_desu
LastEditTime : 2022-07-23 19:51:39
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.base import BaseModeInterface, Channels
from image_encryptor.modes.encrypt.controller import EncryptModeController
from image_encryptor.modes.encrypt.main import normal_gen, normal_gen_quietly
from image_encryptor.modes.encrypt.settings import Settings
from image_encryptor.modes.encrypt.panel import ProcSettingsPanel

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class ModeInterface(BaseModeInterface):
    __slots__ = ('frame', 'settings_controller', 'settings_cls', 'default_settings')
    default_mode = True
    mode_name = '加密模式'
    mode_qualname = 'builtin.encrypt.v1'
    add_encryption_parameters_in_file = True
    corresponding_decryption_mode = 'builtin.decrypt.v1'
    settings_panel_cls = ProcSettingsPanel
    enable_password = True
    file_name_suffix = ('-decrypted', '-encrypted')

    def __init__(self, frame: 'MainFrame', mode_id: int):
        self.frame = frame
        self.settings_panel = frame.mode_manager.add_settings_panel(self.settings_panel_cls)
        self.settings_controller: 'EncryptModeController' = EncryptModeController(frame, self.settings_panel)
        self.settings_cls = Settings
        super().__init__(frame, mode_id)
        self.default_settings = Settings((25, 25, True, True, Channels((False, False, False, False)), False, Channels((True, True, True, False)), False, 128, 'none'))

    def proc_image(self, *args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)
