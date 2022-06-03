"""
Author       : noeru_desu
Date         : 2022-04-16 17:43:06
LastEditors  : noeru_desu
LastEditTime : 2022-06-03 13:31:39
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.base import BaseModeInterface
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
    file_name_suffix = ('-decrypted', '-encrypted')

    def __init__(self, frame: 'MainFrame', mode_id: int):
        self.frame = frame
        self.settings_panel = frame.mode_manager.add_settings_panel(self.settings_panel_cls)
        self.settings_controller: 'EncryptModeController' = EncryptModeController(frame, self.settings_panel)
        self.settings_cls = Settings
        self.default_settings = Settings(frame.controller, self.settings_controller, (25, 25, True, True, '', False, 'rgb', False, 128, None))

    def proc_image(self, *args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)

    @property
    def encryption_settings_tuple(self):
        """当前所有加密设置的元组, 一般为生成encryption_settings_hash时使用"""
        return (
            self.settings_controller.cutting_row, self.settings_controller.cutting_col,
            self.settings_controller.shuffle_chunks, self.settings_controller.flip_chunks,
            self.settings_controller.mapping_channels, self.settings_controller.XOR_encryption,
            self.settings_controller.XOR_channels, self.settings_controller.noise_XOR,
            self.settings_controller.noise_factor, self.frame.controller.password
        )
