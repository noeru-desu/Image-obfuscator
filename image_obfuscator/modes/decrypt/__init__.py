"""
Author       : noeru_desu
Date         : 2022-04-17 08:22:01
LastEditors  : noeru_desu
LastEditTime : 2022-11-26 16:09:53
"""
from typing import TYPE_CHECKING
from image_obfuscator.constants import EA_VERSION

from image_obfuscator.modes.base import BaseModeInterface, Channels
from image_obfuscator.modes.decrypt.main import normal_gen, normal_gen_quietly
from image_obfuscator.modes.decrypt.settings import EncryptionParameters
from image_obfuscator.modes.decrypt.controller import DecryptModeController
from image_obfuscator.modes.decrypt.settings import Settings
from image_obfuscator.modes.decrypt.panel import ProcSettingsPanel


class ModeInterface(BaseModeInterface):
    __slots__ = ()
    settings_controller: 'DecryptModeController'

    settings_panel_cls = ProcSettingsPanel
    enable_password = True
    file_name_suffix = ('-encrypted', '-decrypted')
    mode_name = '解密模式'
    mode_qualname = 'builtin.decrypt.v1'
    always_use_orig_image = True
    can_be_set_as_default_mode = False
    requires_encryption_parameters = True
    settings_cls = Settings
    default_settings_arg = (40, 40, True, True, Channels((False, False, False, False)), False, Channels((True, True, True, False)), False, 128, 'none', 1, 1, EA_VERSION)
    encryption_parameters_cls = EncryptionParameters
    settings_controller_cls = DecryptModeController
    can_be_set_as_default_mode = False

    def proc_image(self, *args):
        return normal_gen(self.main_frame, *args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(self.main_frame, *args)
