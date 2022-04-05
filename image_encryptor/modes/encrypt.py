"""
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-04-05 18:07:36
Description  : 加密模式
"""
from json import dumps
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Any, Callable, Union

from PIL import Image

from image_encryptor.frame.controls import (ProgressBar, SavingSettings,
                                            SettingsData)
from image_encryptor.modules.image_encrypt import ImageEncrypt
from image_encryptor.modules.image import (PillowImage, WrappedPillowImage,
                                           array_to_image)
from image_encryptor.utils.misc_utils import catch_exception_and_return
if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.controls import Settings
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

        original_size = image.size

        if splitext(frame.image_item.path_data.file_name)[1] in {'jpg', 'jpeg', 'wmf', 'webp'}:
            if settings.mapping_channels:
                frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用颜色通道随机映射会导致图像在解密后出现轻微的分界线', '不可逆处理警告')
            if settings.XOR_channels:
                frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用异或加密会导致图像解密后出现严重失真', '不可逆处理警告')

    bar = ProgressBar(gauge, step_count)
    image = process_and_output_progress(image, settings, 100 if settings.password == 'none' else settings.password, bar, logger)

    if save:
        image = PillowImage(*image)
        bar.next_step(1)
        logger('完成，正在保存文件')
        save_image(
            image, frame.image_item.path_data, settings.saving_path, settings.saving_format,
            settings.saving_quality, settings.saving_subsampling_level,
            settings.encryption_parameters_data(*original_size).encryption_parameters_dict
        )
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
    original_size = image.size

    image = process(image, settings, 100 if settings.password == 'none' else settings.password)

    save_image(
        array_to_image(*image), path_data, saving_settings.path, saving_settings.format,
        saving_settings.quality, saving_settings.subsampling_level,
        settings.encryption_parameters_data(*original_size).encryption_parameters_dict,
        auto_folder
    )


def process(image: 'Image.Image', settings: 'SettingsData', password: Any):
    image_encrypt = ImageEncrypt(image, settings.cutting_row, settings.cutting_col, password)

    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        image_encrypt.init_block_data(settings.shuffle_chunks, settings.flip_chunks, settings.mapping_channels)
        image = image_encrypt.generate_image()

    if settings.XOR_encryption:
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)
    return image


def process_and_output_progress(image: 'Image.Image', settings: 'Settings', password: Any, bar: 'ProgressBar', logger: Callable):
    image_encrypt = ImageEncrypt(image, settings.cutting_row, settings.cutting_col, password)
    logger('开始处理')

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
    return image


def save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', saving_path: str, saving_format: str, quality: int, subsampling: int, encryption_parameters_data: dict, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name.replace('-decrypted', '')}-encrypted.{saving_format}"
    if auto_folder:
        save_dir = join(saving_path, image_path_data.relative_path)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_path
    output_path = join(save_dir, name)
    if saving_format.lower() in {'jpg', 'jpeg'}:
        image.convert('RGB')

    image.save(output_path, quality=quality, subsampling=subsampling)

    with open(output_path, "a") as f:
        f.write('\n{}'.format(dumps(encryption_parameters_data, separators=(',', ':'))))
