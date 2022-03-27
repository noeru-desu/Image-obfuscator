"""
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-03-27 08:34:55
Description  : 单文件加密功能
"""
from json import dumps
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable

from PIL import Image

from image_encryptor.frame.controls import (ProgressBar, SavingSettings,
                                            SettingsData)
from image_encryptor.modules.image_encrypt import ImageEncrypt
from image_encryptor.modules.image import (PillowImage, WrappedPillowImage,
                                           array_to_image)
from image_encryptor.utils.misc_utils import catch_exception_and_return

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modules.image import WrappedImage


@catch_exception_and_return
def normal(frame: 'MainFrame', logger: Callable, gauge: 'Gauge', image: 'Image.Image', save: bool, type_conversion: Callable = ...) -> 'WrappedImage':
    settings = frame.settings.all

    step_count = 0
    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        step_count += 2
    if settings.XOR_encryption:
        step_count += 1
    if step_count < 1:
        return WrappedPillowImage(image)
    if save:
        step_count += 1

    password = 100 if settings.password == 'none' else settings.password
    if save:
        name, suffix = splitext(frame.image_item.path_data.file_name)
        suffix = settings.saving_format
        original_size = image.size

        if suffix in ('jpg', 'jpeg', 'wmf', 'webp'):
            if settings.mapping_channels:
                frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用颜色通道随机映射会导致图像在解密后出现轻微的分界线', '不可逆处理警告')
            if settings.XOR_channels:
                frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用异或加密会导致图像解密后出现严重失真', '不可逆处理警告')

    image_encrypt = ImageEncrypt(image, settings.cutting_row, settings.cutting_col, password)
    logger('开始处理')

    bar = ProgressBar(gauge, step_count)

    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        logger('正在分割原图')
        bar.next_step(image_encrypt.base.block_num)
        image_encrypt.init_block_data(settings.shuffle_chunks, settings.flip_chunks, settings.mapping_channels, bar)

        logger('正在重组')
        bar.next_step(image_encrypt.base.block_num)
        image = image_encrypt.generate_image(bar)

    if settings.XOR_encryption:
        bar.next_step(1)
        logger('正在异或加密')
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)

    if save:
        image = PillowImage(*image)
        bar.next_step(1)
        logger('完成，正在保存文件')
        name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
        output_path = join(settings.saving_path, name)
        if suffix.lower() in ('jpg', 'jpeg'):
            image.convert('RGB')

        image.save(output_path, quality=settings.saving_quality, subsampling=settings.saving_subsampling_level)

        with open(output_path, "a") as f:
            f.write('\n{}'.format(dumps(settings.encryption_parameters_data(*original_size).encryption_parameters_dict, separators=(',', ':'))))
        bar.finish()
    elif type_conversion is Ellipsis:
        image = PillowImage(*image)
    else:
        image = type_conversion(*image)
    bar.over()
    logger('完成')
    return image


@catch_exception_and_return
def batch(image_data, path_data: 'PathData', settings, saving_format, auto_folder: bool):
    settings = SettingsData(settings)
    if not (settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels or settings.XOR_encryption):
        return
    image = Image.frombytes(*image_data)
    saving_settings = SavingSettings(*saving_format)
    password = 100 if settings.password == 'none' else settings.password
    name, suffix = splitext(path_data.file_name)
    suffix = saving_settings.format
    original_size = image.size

    image_encrypt = ImageEncrypt(image, settings.cutting_row, settings.cutting_col, password)

    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        image_encrypt.init_block_data(settings.shuffle_chunks, settings.flip_chunks, settings.mapping_channels)
        image = image_encrypt.generate_image()

    if settings.XOR_encryption:
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)

    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    if auto_folder:
        save_dir = join(saving_settings.path, path_data.relative_path)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_settings.path
    output_path = join(save_dir, name)
    image = array_to_image(*image)
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')

    image.save(output_path, quality=saving_settings.quality, subsampling=saving_settings.subsampling_level)

    with open(output_path, "a") as f:
        f.write('\n' + dumps(settings.encryption_parameters_data(*original_size).encryption_parameters_dict, separators=(',', ':')))
