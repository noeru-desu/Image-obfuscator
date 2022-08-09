"""
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2022-08-08 13:08:13
Description  : 主要针对QQ群的图像反阻止发送功能
"""
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image

from image_encryptor.frame.controller import SaveSettings
from image_encryptor.modules.image_encrypt import AntiShield
from image_encryptor.modules.image import WrappedPillowImage
from image_encryptor.modules.decorator import catch_exc_and_return

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modes.base import EmptySettings
    from image_encryptor.modules.image import PillowImage, ImageData


def normal_gen(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedPillowImage':
    label_text_setter('开始处理')

    image = WrappedPillowImage(AntiShield(source).generate_image(), original)

    gauge.SetValue(100)
    label_text_setter('完成')
    return image


def normal_gen_quietly(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EmptySettings') -> 'WrappedPillowImage':
    return WrappedPillowImage(AntiShield(source).generate_image(), original)


def normal_save(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedPillowImage':
    label_text_setter('开始处理')

    image = WrappedPillowImage(AntiShield(source).generate_image(), original)

    gauge.SetValue(50)
    label_text_setter('完成, 正在保存文件')
    _save_image(
        image, frame.image_item.path_data, frame.controller.save_path, frame.controller.save_format,
        frame.controller.save_quality, frame.controller.save_subsampling_level
    )
    gauge.SetValue(100)
    label_text_setter('完成')
    return image


def batch(image_data, path_data: 'PathData', save_settings, auto_folder):
    save_settings = SaveSettings(save_settings)

    image = AntiShield(Image.frombytes(*image_data)).generate_image()

    _save_image(
        image, path_data, save_settings.path, save_settings.format,
        save_settings.quality, save_settings.subsampling_level, auto_folder
    )


def _save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', save_path: str, save_format: str, quality: int, subsampling: int, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name}-anti-shielded.{save_format}"
    if auto_folder:
        save_dir = join(save_path, image_path_data.relative_save_dir)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = save_path
    if save_format.lower() in {'jpg', 'jpeg'}:
        image.convert('RGB')

    image.save(join(save_dir, name), quality=quality, subsampling=subsampling)


save_image = catch_exc_and_return(_save_image)
