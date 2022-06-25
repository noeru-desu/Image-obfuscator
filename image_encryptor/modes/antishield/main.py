"""
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2022-06-24 12:12:53
Description  : 主要针对QQ群的图像反阻止发送功能
"""
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image

from image_encryptor.frame.controller import SavingSettings
from image_encryptor.modules.image_encrypt import AntiShield
from image_encryptor.modules.image import WrappedPillowImage
from image_encryptor.modules.decorator import catch_exc_and_return

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modes.base import EmptySettings
    from image_encryptor.modules.image import PillowImage, ImageData


def normal_gen(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedPillowImage':
    label_text_setter('开始处理')

    image = WrappedPillowImage(AntiShield(source).generate_image(), original)

    gauge.SetValue(100)
    label_text_setter('完成')
    return image


def normal_gen_quietly(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EmptySettings') -> 'WrappedPillowImage':
    return WrappedPillowImage(AntiShield(source).generate_image(), original)


def normal_save(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedPillowImage':
    label_text_setter('开始处理')

    image = WrappedPillowImage(AntiShield(source).generate_image(), original)

    gauge.SetValue(50)
    label_text_setter('完成, 正在保存文件')
    _save_image(
        image, frame.image_item.path_data, frame.controller.saving_path, frame.controller.saving_format,
        frame.controller.saving_quality, frame.controller.saving_subsampling_level
    )
    gauge.SetValue(100)
    label_text_setter('完成')
    return image


def batch(image_data, path_data: 'PathData', saving_settings, auto_folder):
    saving_settings = SavingSettings(saving_settings)

    image = AntiShield(Image.frombytes(*image_data)).generate_image()

    _save_image(
        image, path_data, saving_settings.path, saving_settings.format,
        saving_settings.quality, saving_settings.subsampling_level, auto_folder
    )


def _save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', saving_path: str, saving_format: str, quality: int, subsampling: int, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name}-anti-shielded.{saving_format}"
    if auto_folder:
        save_dir = join(saving_path, image_path_data.relative_saving_dir)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_path
    if saving_format.lower() in {'jpg', 'jpeg'}:
        image.convert('RGB')

    image.save(join(save_dir, name), quality=quality, subsampling=subsampling)


save_image = catch_exc_and_return(_save_image)
