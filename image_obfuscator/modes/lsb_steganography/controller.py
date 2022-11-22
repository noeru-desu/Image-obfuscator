"""
Author       : noeru_desu
Date         : 2022-11-20 13:38:35
LastEditors  : noeru_desu
LastEditTime : 2022-11-22 09:45:12
"""
from os.path import isfile, splitext
from typing import TYPE_CHECKING, Optional, Union

from wx import BLACK

from image_obfuscator.constants import LIGHT_RED
from image_obfuscator.modes.base import BaseModeController
from image_obfuscator.modes.lsb_steganography.core import cal_required_size, max_bits_to_hide
from image_obfuscator.utils.misc_utils import cal_zoom_ratio

if TYPE_CHECKING:
    from image_obfuscator.modes.lsb_steganography.panel import ProcSettingsPanel


class LsbModeController(BaseModeController):
    __slots__ = ()
    _instance: Optional['LsbModeController'] = None
    settings_panel: 'ProcSettingsPanel'

    def __new__(cls: type['LsbModeController'], *_):
        return super().__new__(cls) if cls._instance is None else cls._instance

    def __init__(self):
        if self.__class__._instance is not None:
            return
        self.__class__._instance = self

    @property
    def inside_file(self) -> str: return self.settings_panel.insideFile.GetPath()

    @inside_file.setter
    def inside_file(self, v: str): self.settings_panel.insideFile.SetPath(v)

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
    def lsb_ratio(self) -> str: return self.settings_panel.lsbRatio.GetLabelText()

    @lsb_ratio.setter
    def lsb_ratio(self, v: Union[float, str]):
        if not isinstance(v, float):
            self.settings_panel.lsbRatio.SetLabelText('待计算')
            self.settings_panel.lsbRatio.SetForegroundColour(BLACK)
            return
        self.settings_panel.lsbRatio.SetLabelText(f'{round(v * 100, 1)}%')
        if (not self.auto_zoom_in) and v > 1:
            self.settings_panel.lsbRatio.SetForegroundColour(LIGHT_RED)
        else:
            self.settings_panel.lsbRatio.SetForegroundColour(BLACK)
        self.settings_panel.lsbRatio.Refresh()

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

    @staticmethod
    def _cal_lsb_ratio(image, lsb_num, use_alpha, inside_file) -> float:
        file_suffix_size = len(splitext(inside_file)[1]) - 1
        return cal_zoom_ratio(max_bits_to_hide(image, lsb_num, 4 if use_alpha else 3), cal_required_size(image, inside_file, lsb_num, 4 + file_suffix_size, use_alpha))

    def cal_lsb_ratio(self) -> float:
        image = self.main_frame.image_item.cache.loaded_image
        file_suffix_size = len(splitext(self.inside_file)[1]) - 1
        return cal_zoom_ratio(max_bits_to_hide(image, self.lsb_num, 4 if self.use_alpha else 3), cal_required_size(image, self.inside_file, self.lsb_num, 4 + file_suffix_size, self.use_alpha))
