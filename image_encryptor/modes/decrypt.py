"""
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2022-05-04 19:55:05
Description  : 单文件解密功能
"""
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable, Any, Union

from PIL import Image

from image_encryptor.frame.controls import (EncryptionParametersData,
                                            ProgressBar, SavingSettings)
from image_encryptor.modules.image import (PillowImage, WrappedPillowImage,
                                           array_to_image, crop_array)
from image_encryptor.modules.image_encrypt import ImageDecrypt
from image_encryptor.modules.decorator import catch_exc_and_return

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modules.image import WrappedImage
    from wx import Gauge


@catch_exc_and_return
def normal(frame: 'MainFrame', logger: Callable, gauge: 'Gauge', image: 'Image.Image', save: bool, type_conversion: Callable = ...) -> 'WrappedImage':
    encryption_data = frame.image_item.cache.encryption_parameters
    password = encryption_data.get_password()
    if password is None:
        frame.dialog.async_warning('密码字典中不存在此图像的密码')
        return image

    step_count = 0
    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        step_count += 2
    if encryption_data.XOR_channels:
        step_count += 1
    if step_count < 1:
        return WrappedPillowImage(image)
    if save:
        step_count += 1

    bar = ProgressBar(gauge, step_count)
    image = process_and_output_progress(image, encryption_data, password, bar, logger)

    if encryption_data.version >= 7:
        arr = crop_array(image[0], encryption_data.orig_height, encryption_data.orig_width)
        if save or type_conversion is Ellipsis:
            image = PillowImage(arr, (encryption_data.orig_width, encryption_data.orig_height))
        else:
            image = type_conversion(arr, (encryption_data.orig_width, encryption_data.orig_height))
    else:
        image = WrappedPillowImage(image.crop((0, 0, encryption_data.orig_width, encryption_data.orig_height)))

    if save:
        bar.next_step(1)
        logger('正在保存文件')
        _save_image(
            image, frame.image_item.path_data, frame.controls.saving_path, frame.controls.saving_format,
            frame.controls.saving_quality, frame.controls.saving_subsampling_level
        )
        bar.finish()
    bar.over()
    logger('完成')
    return image


@catch_exc_and_return
def batch(image_data, path_data: 'PathData', encryption_data, saving_settings, auto_folder: bool):
    saving_settings = SavingSettings(*saving_settings)

    image = process(Image.frombytes(*image_data), EncryptionParametersData(encryption_data))

    _save_image(
        image, path_data, saving_settings.path, saving_settings.format,
        saving_settings.quality, saving_settings.subsampling_level, auto_folder
    )


def process(image: 'Image.Image', encryption_data: 'EncryptionParametersData'):
    image_decrypt = ImageDecrypt(image, encryption_data.cutting_row, encryption_data.cutting_col, encryption_data.password if encryption_data.has_password else 100, encryption_data.version)

    if encryption_data.XOR_channels:
        image = image_decrypt.xor_pixels(encryption_data.XOR_channels, encryption_data.noise_XOR, encryption_data.noise_factor)

    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        image_decrypt.init_block_data(encryption_data.shuffle_chunks, encryption_data.flip_chunks, encryption_data.mapping_channels)
        image = image_decrypt.generate_image()

    if encryption_data.version >= 7:
        image = array_to_image(*image)
    image = image.crop((0, 0, encryption_data.orig_width, encryption_data.orig_height))
    return image


def process_and_output_progress(image: 'Image.Image', encryption_data: 'EncryptionParametersData', password: Any, bar: 'ProgressBar', logger: Callable):
    image_decrypt = ImageDecrypt(image, encryption_data.cutting_row, encryption_data.cutting_col, password, encryption_data.version)
    logger('开始处理')

    if encryption_data.XOR_channels:
        logger('正在异或解密')
        bar.next_step(1)
        image = image_decrypt.xor_pixels(encryption_data.XOR_channels, encryption_data.noise_XOR, encryption_data.noise_factor)

    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        bar.next_step(image_decrypt.base.block_num)
        logger('正在分割加密图像')
        image_decrypt.init_block_data(encryption_data.shuffle_chunks, encryption_data.flip_chunks, encryption_data.mapping_channels, bar)

        logger('正在重组')

        bar.next_step(image_decrypt.base.block_num)
        image = image_decrypt.generate_image(bar)
    return image


def _save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', saving_path: str, saving_format: str, quality: int, subsampling: int, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name.replace('-encrypted', '')}-decrypted.{saving_format}"
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