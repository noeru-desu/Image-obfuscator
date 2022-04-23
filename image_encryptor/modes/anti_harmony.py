"""
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2022-04-23 17:19:20
Description  : 主要针对QQ群的图像反阻止发送功能
"""
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable, Union

from PIL import Image

from image_encryptor.frame.controls import SavingSettings
from image_encryptor.modules.image_encrypt import AntiHarmony
from image_encryptor.modules.image import WrappedPillowImage
from image_encryptor.utils.misc_utils import catch_exception_and_return

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modules.image import PillowImage


@catch_exception_and_return
def normal(frame: 'MainFrame', logger: Callable, gauge: 'Gauge', image: 'Image.Image', save: bool) -> 'WrappedPillowImage':
    logger('开始处理')

    image = WrappedPillowImage(AntiHarmony(image).generate_image())

    if save:
        gauge.SetValue(50)
        logger('完成, 正在保存文件')
        save_image(
            image, frame.image_item.path_data, frame.controls.saving_path, frame.controls.saving_format,
            frame.controls.saving_quality, frame.controls.saving_subsampling_level
        )
    gauge.SetValue(100)
    logger('完成')
    return image


@catch_exception_and_return
def batch(image_data, path_data: 'PathData', saving_settings, auto_folder):
    saving_settings = SavingSettings(saving_settings)

    image = AntiHarmony(Image.frombytes(*image_data)).generate_image()

    save_image(
        image, path_data, saving_settings.path, saving_settings.format,
        saving_settings.quality, saving_settings.subsampling_level, auto_folder
    )


def _save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', saving_path: str, saving_format: str, quality: int, subsampling: int, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name}-anti-harmony.{saving_format}"
    if auto_folder:
        save_dir = join(saving_path, image_path_data.relative_path)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_path
    if saving_format.lower() in {'jpg', 'jpeg'}:
        image.convert('RGB')

    image.save(join(save_dir, name), quality=quality, subsampling=subsampling)


save_image = catch_exception_and_return(_save_image)
