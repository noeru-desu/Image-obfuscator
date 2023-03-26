"""
Author       : noeru_desu
Date         : 2022-11-20 17:43:06
LastEditors  : noeru_desu
LastEditTime : 2023-03-26 09:59:37
"""
from image_obfuscator.modes.base import BaseModeInterface
from image_obfuscator.modes.lsb_steganography.controller import LsbModeController
from image_obfuscator.modes.lsb_steganography.main import normal_gen, normal_gen_quietly, save_image
from image_obfuscator.modes.lsb_steganography.settings import Settings
from image_obfuscator.modes.lsb_steganography.panel import ProcSettingsPanel, DetectLsbDialog, CompressionDialog
from image_obfuscator.modes.lsb_steganography.utils import CompressedFileManager


class ModeInterface(BaseModeInterface):
    __slots__ = ('compressed_file_manager',)
    settings_controller: 'LsbModeController'

    mode_name = 'LSB隐写'
    mode_qualname = 'builtin.lsb_steganography.v1'
    always_use_orig_image = True
    settings_panel_cls = ProcSettingsPanel
    settings_cls = Settings
    default_settings_arg = ('', 0, 1, False, True, False, False, None)
    settings_controller_cls = LsbModeController
    file_name_suffix = ('', '-LSB')
    mode_constants_required = (DetectLsbDialog, CompressionDialog, CompressedFileManager)

    def __init__(self):
        super().__init__()
        self.compressed_file_manager = CompressedFileManager(self.main_frame.program_options.temp_dir)

    def proc_image(*args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)

    def save_image(self, loaded_image, image_item, settings, encryption_parameters, save_settings, relative_save_path='', quiet=False):
        return save_image(self, loaded_image, image_item, settings, encryption_parameters, save_settings, relative_save_path, quiet)
