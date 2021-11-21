'''
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2021-11-21 17:01:58
Description  : 单文件解密功能
'''
from os import makedirs
from os.path import join, split, splitext, isdir
from typing import TYPE_CHECKING

from PIL import Image

from image_encryptor.common.modules.image_encrypt import ImageEncrypt
from image_encryptor.common.utils.utils import FakeBar
from image_encryptor.gui.frame.utils import ProgressBar
from image_encryptor.gui.modules.password_verifier import get_image_data

if TYPE_CHECKING:
    from image_encryptor.gui.frame.main_frame import MainFrame


def normal(frame: 'MainFrame', logger, gauge, image: 'Image', save: bool):
    image_data, error = get_image_data(frame.image_item.loaded_image_path, password_dict=frame.program.password_dict)
    if error is not None:
        frame.error(error, '读取加密参数时出现问题')
        return frame.image_item.initial_preview
    image_encrypt = ImageEncrypt(image, image_data['row'], image_data['col'], image_data['password'])
    logger('正在处理')

    step_count = 0
    if image_data['upset'] or image_data['flip'] or image_data['rgb_mapping']:
        step_count += 2
    if image_data['xor_rgb']:
        step_count += 1
    if save:
        step_count += 1

    bar = ProgressBar(gauge, step_count)

    if image_data['upset'] or image_data['flip'] or image_data['rgb_mapping']:
        bar.next_step(image_data['col'] * image_data['row'])
        logger('正在分割加密图像')
        image_encrypt.init_block_data(True, image_data['upset'], image_data['flip'], image_data['rgb_mapping'], bar)

        logger('正在重组')

        bar.next_step(image_data['col'] * image_data['row'])
        image = image_encrypt.generate_image(bar)

    if image_data['xor_rgb']:
        logger('正在异或解密')
        bar.next_step(1)
        image = image_encrypt.xor_pixels(image_data['xor_alpha'])

    image = image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    if save:
        bar.next_step(1)
        logger('正在保存文件')
        name, suffix = splitext(split(frame.image_item.loaded_image_path)[1])
        suffix = frame.program.EXTENSION_KEYS[frame.selectFormat.Selection]
        if suffix.lower() in ('jpg', 'jpeg'):
            image = image.convert('RGB')
        name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

        image.save(join(frame.selectSavePath.Path, name), quality=frame.saveQuality.Value, subsampling=frame.subsamplingLevel.Value)
        bar.finish()
    bar.over()
    logger('完成')
    return image


def batch(image_data, path_data, settings, encryption_data, saving_format, auto_folder):
    image = Image.frombytes(*image_data)
    image_encrypt = ImageEncrypt(image, encryption_data['row'], encryption_data['col'], encryption_data['password'])

    if encryption_data['upset'] or encryption_data['flip'] or encryption_data['rgb_mapping']:
        image_encrypt.init_block_data(True, encryption_data['upset'], encryption_data['flip'], encryption_data['rgb_mapping'], FakeBar)
        image = image_encrypt.generate_image(FakeBar)

    if encryption_data['xor_rgb']:
        image = image_encrypt.xor_pixels(encryption_data['xor_alpha'])

    image = image.crop((0, 0, int(encryption_data['width']), int(encryption_data['height'])))

    name, suffix = splitext(path_data[-1])
    suffix = saving_format
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"
    if auto_folder:
        save_dir = join(settings['saving_path'], path_data[1])
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = settings['saving_path']

    image.save(join(save_dir, name), quality=settings['quality'], subsampling=settings['subsampling'])
