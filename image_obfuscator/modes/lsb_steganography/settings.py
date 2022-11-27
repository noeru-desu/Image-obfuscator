"""
Author       : noeru_desu
Date         : 2022-11-20 08:40:06
LastEditors  : noeru_desu
LastEditTime : 2022-11-25 11:15:56
"""
from typing import TYPE_CHECKING, Callable, Iterable, Any, Optional

from image_obfuscator.modes.base import BaseSettings
from image_obfuscator.modes.lsb_steganography.constants import LSB_RATIO, COMPRESSION_RATIO

if TYPE_CHECKING:
    from image_obfuscator.modes.lsb_steganography import ModeInterface
    from image_obfuscator.modes.lsb_steganography.controller import LsbModeController
    from image_obfuscator.modes.lsb_steganography.panel import ProcSettingsPanel


class Settings(BaseSettings):
    __slots__ = (
        'inside_file_path', 'lsb_mode', 'lsb_num', 'use_alpha',
        'auto_zoom_in', 'auto_zoom_out', 'lsb_ratio', 'direct_extraction',
        'compression_ratio'
    )
    SETTING_NAMES = (
        'inside_file_path', 'lsb_mode', 'lsb_num', 'use_alpha',
        'auto_zoom_in', 'auto_zoom_out', 'direct_extraction',
        'compression_ratio'
    )
    mode_interface: 'ModeInterface'
    settings_panel: 'ProcSettingsPanel'
    mode_controller: 'LsbModeController'

    def __init__(self, settings: Iterable[Any] = None, data = None):
        self.lsb_ratio: Optional[float] = None
        if settings is None:
            self.sync_from_interface()
        else:
            self.sync_from_tuple(settings)
        self.compression_ratio: Optional[float] = None
        super().__init__()

    @classmethod
    def gen_settings_mapping_kwargs(cls) -> dict[int, tuple[str, Callable]]:
        mode_controller: 'LsbModeController' = cls.mode_constants.mode_controller
        settings_panel: 'ProcSettingsPanel' = cls.mode_constants.settings_panel
        return {
            hash(settings_panel.insideFile): ('inside_file_path', lambda event: mode_controller.inside_file),
            hash(settings_panel.lsbNum): ('lsb_num', lambda event: mode_controller.lsb_num),
            hash(settings_panel.autoZoomIn): ('auto_zoom_in', lambda event: mode_controller.auto_zoom_in),
            hash(settings_panel.autoZoomOut): ('auto_zoom_out', lambda event: mode_controller.auto_zoom_out),
            hash(settings_panel.lsbMode): ('lsb_mode', lambda event: mode_controller.lsb_mode),
            hash(settings_panel.useAlpha): ('use_alpha', lambda event: mode_controller.use_alpha),
            hash(settings_panel.directExtraction): ('direct_extraction', lambda event: mode_controller.direct_extraction),
            LSB_RATIO: ('lsb_ratio', lambda event: mode_controller.lsb_ratio),
            COMPRESSION_RATIO: ('compression_ratio', lambda event: mode_controller.compression_ratio)
        }

    def sync_from_interface(self):
        self.inside_file_path = self.mode_controller.inside_file
        self.lsb_mode = self.mode_controller.lsb_mode
        self.lsb_num = self.mode_controller.lsb_num
        self.use_alpha = self.mode_controller.use_alpha
        self.auto_zoom_in = self.mode_controller.auto_zoom_in
        self.auto_zoom_out = self.mode_controller.auto_zoom_out
        self.direct_extraction = self.mode_controller.direct_extraction
        self.compression_ratio = self.mode_controller.compression_ratio
        if self.mode_controller.can_cal_lsb_ratio():
            self.lsb_ratio = self.mode_controller.recal_and_display_lsb_ratio()

    def backtrack_interface(self):
        self.mode_controller.inside_file = self.inside_file_path
        self.mode_controller.lsb_mode = self.lsb_mode
        self.mode_controller.lsb_num = self.lsb_num
        self.mode_controller.use_alpha = self.use_alpha
        self.mode_controller.auto_zoom_in = self.auto_zoom_in
        self.mode_controller.auto_zoom_out = self.auto_zoom_out
        self.mode_controller.direct_extraction = self.direct_extraction
        if (compressed_file := self.mode_interface.compressed_file_manager.get_compressed_file(self.inside_file_path)) is not None:
            compression_ratio = compressed_file.compression_ratio
        else:
            compression_ratio = None
        self.mode_controller.compression_ratio = compression_ratio
        if (self.lsb_ratio is None or self.compression_ratio != compression_ratio) and self.mode_controller.can_cal_lsb_ratio():
            self.lsb_ratio = self.mode_controller.cal_lsb_ratio()
        self.compression_ratio = compression_ratio
        self.mode_controller.lsb_ratio = self.lsb_ratio
