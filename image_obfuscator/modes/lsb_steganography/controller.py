"""
Author       : noeru_desu
Date         : 2022-11-20 13:38:35
LastEditors  : noeru_desu
LastEditTime : 2022-11-26 11:18:29
"""
from os.path import isfile, splitext
from typing import TYPE_CHECKING, Optional

from wx import BLACK

from image_obfuscator.constants import LIGHT_RED
from image_obfuscator.modes.base import BaseModeController
from image_obfuscator.modes.lsb_steganography.constants import LSB_INFO_LEN
from image_obfuscator.modes.lsb_steganography.core import cal_required_size, max_bits_to_hide
from image_obfuscator.modes.lsb_steganography.utils import cal_estimated_size
from image_obfuscator.utils.misc_utils import cal_zoom_ratio

if TYPE_CHECKING:
    from image_obfuscator.modes.lsb_steganography import ModeInterface
    from image_obfuscator.modes.lsb_steganography.panel import ProcSettingsPanel


class LsbModeController(BaseModeController):
    __slots__ = ('_compression_ratio', '_lsb_ratio')
    _instance: Optional['LsbModeController'] = None
    settings_panel: 'ProcSettingsPanel'
    mode_interface: 'ModeInterface'

    def __new__(cls: type['LsbModeController'], *_):
        return super().__new__(cls) if cls._instance is None else cls._instance

    def __init__(self):
        if self.__class__._instance is not None:
            return
        self.__class__._instance = self
        self._compression_ratio: Optional[float] = None
        self._lsb_ratio: Optional[float] = None

    @property
    def inside_file(self) -> str: return self.settings_panel.insideFile.GetPath()

    @inside_file.setter
    def inside_file(self, v: str): self.settings_panel.insideFile.SetPath(v)

    @property
    def inside_file_suffix(self) -> str: return splitext(self.inside_file)[1]

    @property
    def lsb_mode(self) -> int: return self.settings_panel.lsbMode.GetSelection()

    @lsb_mode.setter
    def lsb_mode(self, v: int): self.settings_panel.lsbMode.SetSelection(v)

    @property
    def direct_extraction(self) -> bool: return self.settings_panel.directExtraction.GetValue()

    @direct_extraction.setter
    def direct_extraction(self, v: bool): self.settings_panel.directExtraction.SetValue(v)

    @property
    def lsb_num(self) -> int: return self.settings_panel.lsbNum.GetValue()

    @lsb_num.setter
    def lsb_num(self, v: int): self.settings_panel.lsbNum.SetValue(v)

    @property
    def use_alpha(self) -> bool: return self.settings_panel.useAlpha.GetValue()

    @use_alpha.setter
    def use_alpha(self, v: bool): self.settings_panel.useAlpha.SetValue(v)

    @property
    def auto_zoom_in(self) -> bool: return self.settings_panel.autoZoomIn.GetValue()

    @auto_zoom_in.setter
    def auto_zoom_in(self, v: bool): self.settings_panel.autoZoomIn.SetValue(v)

    @property
    def auto_zoom_out(self) -> bool: return self.settings_panel.autoZoomOut.GetValue()

    @auto_zoom_out.setter
    def auto_zoom_out(self, v: bool): self.settings_panel.autoZoomOut.SetValue(v)

    @property
    def compression_ratio(self) -> Optional[float]: return self._compression_ratio

    @compression_ratio.setter
    def compression_ratio(self, v: Optional[float]):
        self._compression_ratio = v
        percentage = f'{round(v * 100, 1)}%' if isinstance(v, float) else '待压缩'
        self.settings_panel.compressionRatio.SetLabelText(percentage)

    @property
    def estimated_size(self) -> str: return self.settings_panel.estimatedSize.GetLabelText()

    @estimated_size.setter
    def estimated_size(self, v: str): self.settings_panel.estimatedSize.SetLabelText(v)

    @property
    def lsb_ratio(self) -> Optional[float]: return self._lsb_ratio

    @lsb_ratio.setter
    def lsb_ratio(self, v: Optional[float]):
        self.settings_panel.lsbRatio.SetForegroundColour(BLACK)
        self._lsb_ratio = v
        if not isinstance(v, float):
            self.settings_panel.lsbRatio.SetLabelText('待计算')
            self.estimated_size = '待计算'
            return
        self.settings_panel.lsbRatio.SetLabelText(f'{round(v * 100, 1)}%')
        image = self.main_frame.image_item.cache.loaded_image
        if not self.auto_zoom_in and v > 1:
            self.settings_panel.lsbRatio.SetForegroundColour(LIGHT_RED)
        self.estimated_size = '{0}x{1}'.format(*cal_estimated_size(image, v))
        self.settings_panel.lsbRatio.Refresh()
        self.settings_panel.textPanel.Layout()

    def refresh_lsb_ratio_color(self):
        if self.can_cal_lsb_ratio():
            if (not self.auto_zoom_in) and self.main_frame.image_item.settings.lsb_ratio > 1:
                self.settings_panel.lsbRatio.SetForegroundColour(LIGHT_RED)
            else:
                self.settings_panel.lsbRatio.SetForegroundColour(BLACK)
            self.settings_panel.lsbRatio.Refresh()

    def can_cal_lsb_ratio(self):
        return (self.main_frame.image_item is not None) and isfile(self.inside_file)

    def recal_and_display_lsb_ratio(self):
        self.lsb_ratio = lsb_ratio = self.cal_lsb_ratio()
        return lsb_ratio

    def _cal_lsb_ratio(self, image, lsb_num, use_alpha, inside_file) -> float:
        file_suffix_size = len(self.inside_file_suffix) - 1
        inside_size = self.mode_interface.compressed_file_manager.get_size(inside_file)
        return cal_zoom_ratio(max_bits_to_hide(image, lsb_num, 4 if use_alpha else 3), cal_required_size(image, inside_size, lsb_num, LSB_INFO_LEN + file_suffix_size, use_alpha))

    def cal_lsb_ratio(self) -> float:
        image = self.main_frame.image_item.cache.loaded_image
        file_suffix_size = len(self.inside_file_suffix) - 1
        inside_size = self.mode_interface.compressed_file_manager.get_size(self.inside_file)
        return cal_zoom_ratio(max_bits_to_hide(image, self.lsb_num, 4 if self.use_alpha else 3), cal_required_size(image, inside_size, self.lsb_num, LSB_INFO_LEN + file_suffix_size, self.use_alpha))
