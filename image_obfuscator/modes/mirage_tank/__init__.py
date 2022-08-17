"""
Author       : noeru_desu
Date         : 2022-04-16 17:43:06
LastEditors  : noeru_desu
LastEditTime : 2022-08-17 13:10:26
Description  : 
"""
from image_obfuscator.modes.base import BaseModeInterface
from image_obfuscator.modes.mirage_tank.controller import MirageTankModeController
from image_obfuscator.modes.mirage_tank.main import normal_gen, normal_gen_quietly
from image_obfuscator.modes.mirage_tank.settings import Settings
from image_obfuscator.modes.mirage_tank.panel import ProcSettingsPanel


class ModeInterface(BaseModeInterface):
    __slots__ = ()
    settings_controller: 'MirageTankModeController'

    mode_name = '幻影坦克(Beta)'
    mode_qualname = 'builtin.mirage_tank.v1'
    decryption_mode = True
    can_be_set_as_default_mode = True
    settings_panel_cls = ProcSettingsPanel
    settings_cls = Settings
    default_settings_arg = (None, '', 100, 18, 50, 70, False, False, 1)
    settings_controller_cls = MirageTankModeController
    file_name_suffix = ('', '-MirageTank')

    def proc_image(self, *args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)
