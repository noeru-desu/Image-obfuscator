"""
Author       : noeru_desu
Date         : 2022-04-17 13:38:35
LastEditors  : noeru_desu
LastEditTime : 2022-08-15 08:08:19
"""
from typing import TYPE_CHECKING, Optional

from wx import BLACK, WHITE

from image_obfuscator.modes.base import BaseModeController

if TYPE_CHECKING:
    from image_obfuscator.modes.mirage_tank.panel import ProcSettingsPanel


class MirageTankModeController(BaseModeController):
    "控制器"
    __slots__ = ()
    _instance: Optional['MirageTankModeController'] = None
    settings_panel: 'ProcSettingsPanel'

    def __new__(cls: type['MirageTankModeController'], *_):
        return super().__new__(cls) if cls._instance is None else cls._instance

    def __init__(self):
        if self.__class__._instance is not None:
            return
        self.__class__._instance = self

    @property
    def outside_image_path(self) -> str: return self.settings_panel.outsideImage.GetPath()

    @outside_image_path.setter
    def outside_image_path(self, v: str): self.settings_panel.outsideImage.SetPath(v)

    @property
    def outside_brightness_scale(self) -> float: return self.settings_panel.outsideBrightnessScale.GetValue()

    @outside_brightness_scale.setter
    def outside_brightness_scale(self, v: float): self.settings_panel.outsideBrightnessScale.SetValue(v)

    @property
    def inside_brightness_scale(self) -> float: return self.settings_panel.insideBrightnessScale.GetValue()

    @inside_brightness_scale.setter
    def inside_brightness_scale(self, v: float): self.settings_panel.insideBrightnessScale.SetValue(v)

    @property
    def outside_color_scale(self) -> float: return self.settings_panel.outsideColorScale.GetValue()

    @outside_color_scale.setter
    def outside_color_scale(self, v: float): self.settings_panel.outsideColorScale.SetValue(v)

    @property
    def inside_color_scale(self) -> float: return self.settings_panel.insideColorScale.GetValue()

    @inside_color_scale.setter
    def inside_color_scale(self, v: float): self.settings_panel.insideColorScale.SetValue(v)

    @property
    def damier_mode(self) -> bool: return self.settings_panel.damierMode.GetValue()

    @damier_mode.setter
    def damier_mode(self, v: bool): self.settings_panel.damierMode.SetValue(v)

    @property
    def colorful_mode(self) -> bool: return self.settings_panel.colorfulMode.GetValue()

    @colorful_mode.setter
    def colorful_mode(self, v: bool):
        self.settings_panel.colorfulMode.SetValue(v)
        self.settings_panel.outsideColorScale.Enable(v)
        self.settings_panel.insideColorScale.Enable(v)

    @property
    def resize_method(self) -> int:
        return self.settings_panel.resizeMethod.GetSelection()

    @resize_method.setter
    def resize_method(self, v: int):
        self.settings_panel.resizeMethod.SetSelection(v)

    @property
    def accuracy(self) -> int:
        return self.settings_panel.accuracy.GetSelection()

    @accuracy.setter
    def accuracy(self, v: int):
        self.settings_panel.accuracy.SetSelection(v)

    @property
    def black_preview_bg(self) -> bool:
        return self.settings_panel.toggleBg.GetValue()

    @black_preview_bg.setter
    def black_preview_bg(self, v: bool):
        self.settings_panel.toggleBg.SetValue(v)
        if v:
            self.settings_panel.toggleBg.SetLabelText('切换至\n白底预览')
            self.main_controller.set_preview_panel_bg(BLACK)
        else:
            self.settings_panel.toggleBg.SetLabelText('切换至\n黑底预览')
            self.main_controller.set_preview_panel_bg(WHITE)
