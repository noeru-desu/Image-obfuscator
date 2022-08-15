"""
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-08-15 08:23:48
Description  : 加密模式
"""
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image

from image_obfuscator.modes.mirage_tank.settings import Settings
from image_obfuscator.modes.mirage_tank.core import gray_mode, colorful_mode
from image_obfuscator.modules.image import cal_best_size

if TYPE_CHECKING:
    from wx import Gauge
    from image_obfuscator.modes.base import EmptySettings
    from image_obfuscator.modes.encrypt.settings import Settings
    from image_obfuscator.modules.image import WrappedImage, ImageData, PillowImage


def normal_gen(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedImage':
    outside_image = settings.outside_image
    if outside_image is None:
        return None
    gauge.SetValue(0)
    label_text_setter('正在处理')
    image = return_type(colorful_mode(
        source, outside_image, settings.outside_brightness_scale / 100, settings.inside_brightness_scale / 100,
        settings.outside_color_scale / 100, settings.inside_color_scale / 100, settings.damier_mode, settings.resize_method,
        settings.accuracy
    ) if settings.colorful_mode else gray_mode(
        source, outside_image, settings.outside_brightness_scale / 100, settings.inside_brightness_scale / 100,
        settings.damier_mode, settings.resize_method, settings.accuracy
    ))
    gauge.SetValue(gauge.Range)
    label_text_setter('完成')
    return image


def normal_gen_quietly(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EmptySettings') -> 'WrappedImage':
    if settings.outside_image is None:
        return None
    image = return_type(colorful_mode(
        source, settings.outside_image, settings.outside_brightness_scale / 100, settings.inside_brightness_scale / 100,
        settings.outside_color_scale / 100, settings.inside_color_scale / 100, settings.damier_mode, settings.resize_method,
        settings.accuracy
    ) if settings.colorful_mode else gray_mode(
        source, settings.outside_image, settings.outside_brightness_scale / 100, settings.inside_brightness_scale / 100,
        settings.damier_mode, settings.resize_method, settings.accuracy
    ))
    return image
