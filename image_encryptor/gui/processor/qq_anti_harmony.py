'''
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2021-11-21 16:22:45
Description  : 主要针对QQ群的图片反阻止发送功能(测试中)
'''
from os import makedirs
from os.path import join, split, splitext, isdir
from typing import TYPE_CHECKING

from numpy.random import randint
from PIL import Image

if TYPE_CHECKING:
    from image_encryptor.gui.frame.main_frame import MainFrame


def normal(frame: 'MainFrame', logger, gauge, image: 'Image.Image', save: bool):
    logger('开始处理')

    image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((0, image.size[1] - 1), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(256), randint(256), randint(256)))

    if save:
        logger('完成，正在保存文件')
        name, suffix = splitext(split(frame.image_item.loaded_image_path)[1])
        suffix = frame.program.EXTENSION_KEYS[frame.selectFormat.Selection]
        name = f'{name}-anti-harmony.{suffix}'
        if suffix.lower() in ('jpg', 'jpeg'):
            image = image.convert('RGB')
        image.save(join(frame.selectSavePath.Path, name), quality=frame.saveQuality.Value, subsampling=frame.subsamplingLevel.Value)
    gauge.SetValue(100)
    logger('完成')
    return image


def batch(image_data, path_data, settings, saving_format, auto_folder):
    image = Image.frombytes(*image_data)
    image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((0, image.size[1] - 1), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(256), randint(256), randint(256)))

    name, suffix = splitext(path_data[-1])
    suffix = saving_format
    name = f'{name}-anti-harmony.{suffix}'
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    if auto_folder:
        save_dir = join(settings['saving_path'], path_data[1])
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = settings['saving_path']
    image.save(join(save_dir, name), quality=settings['quality'], subsampling=settings['subsampling'])
    return image
