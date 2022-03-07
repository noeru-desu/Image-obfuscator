"""
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2022-03-07 10:12:49
Description  : 主要针对QQ群的图片反阻止发送功能(测试中)
"""
from os import makedirs
from os.path import isdir, join, split, splitext
from traceback import format_exc
from typing import TYPE_CHECKING

from PIL import Image

from image_encryptor.frame.controls import SavingSettings
from image_encryptor.modules.image_encrypt import AntiHarmony

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData


def normal(frame: 'MainFrame', logger, gauge: 'Gauge', image: 'Image.Image', save: bool):
    try:
        return False, _normal(frame, logger, gauge, image, save)
    except Exception:
        return True, format_exc()


def batch(image_data, path_data, saving_settings, auto_folder):
    try:
        return False, _batch(image_data, path_data, SavingSettings(saving_settings), auto_folder)
    except Exception:
        return True, format_exc()


def _normal(frame: 'MainFrame', logger, gauge: 'Gauge', image, save):
    logger('开始处理')

    image = AntiHarmony(image).generate_image()

    if save:
        gauge.SetValue(50)
        logger('完成, 正在保存文件')
        name, suffix = splitext(split(frame.image_item.loaded_image_path)[1])
        suffix = frame.controls.saving_format
        name = f'{name}-anti-harmony.{suffix}'
        if suffix.lower() in ('jpg', 'jpeg'):
            image = image.convert('RGB')
        image.save(join(frame.controls.saving_path, name), quality=frame.controls.saving_quality, subsampling=frame.controls.saving_subsampling_level)
    gauge.SetValue(100)
    logger('完成')
    return image


def _batch(image_data, path_data: 'PathData', saving_settings: 'SavingSettings', auto_folder):
    image = AntiHarmony(Image.frombytes(*image_data)).generate_image()

    name, suffix = splitext(path_data.file_name)
    suffix = saving_settings.format
    name = f'{name}-anti-harmony.{suffix}'
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    if auto_folder:
        save_dir = join(saving_settings.path, path_data.relative_path)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_settings.path
    image.save(join(save_dir, name), quality=saving_settings.quality, subsampling=saving_settings.subsampling_level)
