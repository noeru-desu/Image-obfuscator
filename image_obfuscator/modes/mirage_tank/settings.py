"""
Author       : noeru_desu
Date         : 2022-04-17 08:40:06
LastEditors  : noeru_desu
LastEditTime : 2022-08-15 08:24:28
Description  : 
"""
from typing import TYPE_CHECKING, Callable, Iterable, Any
from os.path import isfile

from wx import BLACK, WHITE

from image_obfuscator.modes.base import BaseSettings
from image_obfuscator.modules.image import open_image

if TYPE_CHECKING:
    from PIL.Image import Image
    from image_obfuscator.modes.mirage_tank.controller import MirageTankModeController
    from image_obfuscator.modes.mirage_tank.panel import ProcSettingsPanel


class Settings(BaseSettings):
    __slots__ = (
        '_outside_image', 'outside_image_path', 'outside_brightness_scale', 'inside_brightness_scale',
        'outside_color_scale', 'inside_color_scale', 'damier_mode', 'colorful_mode',
        'resize_method', 'accuracy'
    )
    SETTING_NAMES = (
        'outside_image_path', 'outside_brightness_scale', 'inside_brightness_scale',
        'outside_color_scale', 'inside_color_scale', 'damier_mode', 'colorful_mode',
        'resize_method', 'accuracy'
    )
    DATA_NAMES = ('_outside_image',)
    settings_panel: 'ProcSettingsPanel'
    mode_controller: 'MirageTankModeController'

    def __init__(self, settings: Iterable[Any] = None, data = None):
        self.outside_image_path = None
        self._outside_image = None
        if settings is None:
            self.sync_from_interface()
        else:
            self.sync_from_tuple(settings)
        if data is not None:
            self.sync_data_from_tuple(data)
        super().__init__()

    @classmethod
    def gen_settings_mapping_kwargs(cls) -> dict[int, tuple[str, Callable]]:
        mode_controller: 'MirageTankModeController' = cls.mode_constants.mode_controller
        settings_panel: 'ProcSettingsPanel' = cls.mode_constants.settings_panel
        return {
            hash(settings_panel.outsideImage): ('_outside_image_path', lambda event: mode_controller.outside_image_path),
            hash(settings_panel.outsideBrightnessScale): ('outside_brightness_scale', lambda event: mode_controller.outside_brightness_scale),
            hash(settings_panel.insideBrightnessScale): ('inside_brightness_scale', lambda event: mode_controller.inside_brightness_scale),
            hash(settings_panel.outsideColorScale): ('outside_color_scale', lambda event: mode_controller.outside_color_scale),
            hash(settings_panel.insideColorScale): ('inside_color_scale', lambda event: mode_controller.inside_color_scale),
            hash(settings_panel.damierMode): ('damier_mode', lambda event: mode_controller.damier_mode),
            hash(settings_panel.colorfulMode): ('colorful_mode', lambda event: mode_controller.colorful_mode),
            hash(settings_panel.resizeMethod): ('resize_method', lambda event: mode_controller.resize_method),
            hash(settings_panel.accuracy): ('accuracy', lambda event: mode_controller.accuracy)
        }

    def sync_from_interface(self):
        if self.outside_image_path != self.mode_controller.outside_image_path:
            self._outside_image = None
        self.outside_image_path = self.mode_controller.outside_image_path
        self.outside_brightness_scale = self.mode_controller.outside_brightness_scale
        self.inside_brightness_scale = self.mode_controller.inside_brightness_scale
        self.outside_color_scale = self.mode_controller.outside_color_scale
        self.inside_color_scale = self.mode_controller.inside_color_scale
        self.damier_mode = self.mode_controller.damier_mode
        self.colorful_mode = self.mode_controller.colorful_mode
        self.resize_method = self.mode_controller.resize_method
        self.accuracy = self.mode_controller.accuracy
        if self.outside_image_path:
            self.load_outside_image()

    def backtrack_interface(self):
        self.mode_controller.outside_image_path = self.outside_image_path
        self.mode_controller.outside_brightness_scale = self.outside_brightness_scale
        self.mode_controller.inside_brightness_scale = self.inside_brightness_scale
        self.mode_controller.outside_color_scale = self.outside_color_scale
        self.mode_controller.inside_color_scale = self.inside_color_scale
        self.mode_controller.damier_mode = self.damier_mode
        self.mode_controller.colorful_mode = self.colorful_mode
        self.mode_controller.resize_method = self.resize_method
        self.mode_controller.accuracy = self.accuracy
        self.main_controller.set_preview_panel_bg(BLACK if self.settings_panel.toggleBg.GetValue() else WHITE)

    def load_outside_image(self):
        if not isfile(self.outside_image_path):
            self._outside_image = None
            self.mode_controller.outside_image_path = self.outside_image_path = ''
            return None
        self._outside_image, error = open_image(self.outside_image_path)
        if error is not None:
            self._outside_image = None
            self.main_frame.dialog.async_error(error, '载入所选表图时出现错误')
            self.mode_controller.outside_image_path = self.outside_image_path = ''
        return self._outside_image

    @property
    def outside_image(self) -> 'Image':
        # ! 未对低内存占用模式进行支持
        if self._outside_image is None:
            self.load_outside_image()
        return self._outside_image

    @outside_image.setter
    def outside_image(self, v: 'Image'):
        self._outside_image = v

    @property
    def _outside_image_path(self): pass

    @_outside_image_path.setter
    def _outside_image_path(self, v):
        self.outside_image_path = v
        self.load_outside_image()
