"""
Author       : noeru_desu
Date         : 2022-04-16 17:43:06
LastEditors  : noeru_desu
LastEditTime : 2022-08-08 09:27:19
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
    __slots__ = ()
    settings_controller: 'EncryptModeController'

    default_mode = True
    mode_name = '加密模式'
    mode_qualname = 'builtin.encrypt.v1'
    add_encryption_parameters_in_file = True
    corresponding_decryption_mode = 'builtin.decrypt.v1'
    settings_panel_cls = ProcSettingsPanel
    enable_password = True
    settings_cls = Settings
    default_settings_arg = (25, 25, True, True, Channels((False, False, False, False)), False, Channels((True, True, True, False)), False, 128, 'none')
    settings_controller_cls = EncryptModeController
    file_name_suffix = ('-decrypted', '-encrypted')

    def proc_image(self, *args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)
