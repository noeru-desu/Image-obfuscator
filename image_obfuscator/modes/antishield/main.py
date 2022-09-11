"""
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2022-09-11 17:30:29
Description  : 主要针对QQ群的图像反阻止发送功能
"""
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image
from numpy.random import randint

from image_obfuscator.modules.image import WrappedPillowImage

if TYPE_CHECKING:
    from wx import Gauge
    from image_obfuscator.modes.base import EmptySettings
    from image_obfuscator.modules.image import PillowImage, ImageData


def normal_gen(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedPillowImage':
    label_text_setter('开始处理')

    image = WrappedPillowImage(proc_image(source), original)

    gauge.SetValue(100)
    label_text_setter('完成')
    return image


def normal_gen_quietly(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EmptySettings') -> 'WrappedPillowImage':
    return WrappedPillowImage(proc_image(source), original)


def proc_image(image: 'Image.Image'):
        image = image
        right_pos = image.size[0] - 1
        button_pos = image.size[1] - 1
        image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
        image.putpixel((right_pos, 0), (randint(256), randint(256), randint(256)))
        image.putpixel((0, button_pos), (randint(256), randint(256), randint(256)))
        image.putpixel((right_pos, button_pos), (randint(256), randint(256), randint(256)))
        return image
