'''
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2022-01-30 16:41:37
Description  : 主要针对QQ群的图片反阻止发送功能(测试中)
'''
from os import makedirs
from os.path import join, split, splitext, isdir
from traceback import format_exc
from typing import TYPE_CHECKING

from numpy.random import randint
from PIL import Image

from image_encryptor.constants import EXTENSION_KEYS

if TYPE_CHECKING:
    from image_encryptor.gui.frame.controls import SavingSettings
    from image_encryptor.gui.frame.events import MainFrame


def normal(frame, logger, gauge, image: 'Image.Image', save: bool):
    try:
        return False, _normal(frame, logger, gauge, image, save)
    except Exception:
        return True, format_exc()


def batch(image_data, path_data, settings, saving_format, auto_folder):
    try:
        return False, _batch(image_data, path_data, settings, saving_format, auto_folder)
    except Exception:
        return True, format_exc()


def _normal(frame: 'MainFrame', logger, gauge, image, save):
    logger('开始处理')

    image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((0, image.size[1] - 1), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(256), randint(256), randint(256)))

    if save:
        logger('完成，正在保存文件')
        name, suffix = splitext(split(frame.image_item.loaded_image_path)[1])
        suffix = EXTENSION_KEYS[frame.controls.saving_path]
        name = f'{name}-anti-harmony.{suffix}'
        if suffix.lower() in ('jpg', 'jpeg'):
            image = image.convert('RGB')
        image.save(join(frame.controls.saving_path, name), quality=frame.controls.saving_quality, subsampling=frame.controls.saving_subsampling_level)
    gauge.SetValue(100)
    logger('完成')
    return image


def _batch(image_data, path_data, saving_settings: 'SavingSettings', auto_folder):
    image = Image.frombytes(*image_data)
    image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((0, image.size[1] - 1), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(256), randint(256), randint(256)))

    name, suffix = splitext(path_data[-1])
    suffix = saving_settings.format
    name = f'{name}-anti-harmony.{suffix}'
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    if auto_folder:
        save_dir = join(saving_settings.path, path_data[1])
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_settings.path
    image.save(join(save_dir, name), quality=saving_settings.quality, subsampling=saving_settings.subsampling_level)
    return image
