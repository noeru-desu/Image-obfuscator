"""
Author       : noeru_desu
Date         : 2022-04-17 08:40:06
LastEditors  : noeru_desu
LastEditTime : 2022-11-12 15:55:44
"""
from typing import TYPE_CHECKING, Callable, Iterable, Any
from os.path import isfile

from wx import BLACK, WHITE

from image_obfuscator.modes.base import BaseSettings
from image_obfuscator.modules.image import open_image
from image_obfuscator.utils.misc_utils import LRUCache

if TYPE_CHECKING:
    from PIL.Image import Image
    from image_obfuscator.modes.base import ModeConstants
    from image_obfuscator.modes.mirage_tank.controller import MirageTankModeController
    from image_obfuscator.modes.mirage_tank.panel import ProcSettingsPanel


class OutsideImageCache(LRUCache):
    mode_constants: 'ModeConstants'

    def __init__(self, maxlen=10) -> None:
        super().__init__(maxlen)

    def get(self, path):
        if path in self.dict:
            self.record(path)
            return self.dict[path]
        return self.load(path)

    def load(self, path):
        if not isfile(path):
            self.remove(path)
            return None
        image, error = open_image(path)
        if error is not None:
            self.remove(path)
            self.mode_constants.main_frame.dialog.async_error(error, '载入所选表图时出现错误')
            return None
        if not self.mode_constants.main_frame.startup_parameters.low_memory:
            self.record(path, image)
        return image


class Settings(BaseSettings):
    __slots__ = SETTING_NAMES = (
        'outside_image_path', 'outside_brightness_scale', 'inside_brightness_scale',
        'outside_color_scale', 'inside_color_scale', 'damier_mode', 'colorful_mode',
        'resize_method', 'accuracy', 'replace_image'
    )
    settings_panel: 'ProcSettingsPanel'
    mode_controller: 'MirageTankModeController'
    outside_image_cache = OutsideImageCache()

    def __init__(self, settings: Iterable[Any] = None, data = None):
        self.outside_image_path = None
        if settings is None:
            self.sync_from_interface()
        else:
            self.sync_from_tuple(settings)
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
            hash(settings_panel.accuracy): ('accuracy', lambda event: mode_controller.accuracy),
            hash(settings_panel.replaceImage): ('replace_image', lambda event: mode_controller.replace_image)
        }

    def sync_from_interface(self):
        self.outside_image_path = self.mode_controller.outside_image_path
        self.outside_brightness_scale = self.mode_controller.outside_brightness_scale
        self.inside_brightness_scale = self.mode_controller.inside_brightness_scale
        self.outside_color_scale = self.mode_controller.outside_color_scale
        self.inside_color_scale = self.mode_controller.inside_color_scale
        self.damier_mode = self.mode_controller.damier_mode
        self.colorful_mode = self.mode_controller.colorful_mode
        self.resize_method = self.mode_controller.resize_method
        self.accuracy = self.mode_controller.accuracy
        self.replace_image = self.mode_controller.replace_image

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
        self.mode_controller.replace_image = self.replace_image
        if self.replace_image:
            self.settings_panel.outsideImage.PickerCtrl.SetLabel('选择里图')
        else:
            self.settings_panel.outsideImage.PickerCtrl.SetLabel('选择表图')
        self.main_controller.set_preview_panel_bg(BLACK if self.settings_panel.toggleBg.GetValue() else WHITE)

    @property
    def outside_image(self) -> 'Image':
        image = self.outside_image_cache.get(self.outside_image_path)
        if image is None:
            self.mode_controller.outside_image_path = self.outside_image_path = ''
        return image

    @property
    def _outside_image_path(self): pass

    @_outside_image_path.setter
    def _outside_image_path(self, v):
        self.outside_image_path = v
