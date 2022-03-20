"""
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2022-03-20 12:27:10
Description  : 单文件解密功能
"""
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable

from PIL import Image

from image_encryptor.frame.controls import (EncryptionParametersData,
                                            ProgressBar, SavingSettings)
from image_encryptor.modules.image_encrypt import ImageDecrypt
from image_encryptor.utils.image import (PillowImage, WrappedPillowImage,
                                         array_to_image, crop_array)
from image_encryptor.utils.misc_util import catch_exception_and_return

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.utils.image import WrappedImage


@catch_exception_and_return
def normal(frame: 'MainFrame', logger: Callable, gauge: 'Gauge', image: 'Image.Image', save: bool, type_conversion: Callable = ...) -> 'WrappedImage':
    encryption_data = frame.image_item.cache.encryption_data
    if encryption_data.has_password:
        if encryption_data.password is None:
            encryption_data.password = frame.password_dict.get_password(encryption_data.password_base64)
            if encryption_data.password is None:
                frame.dialog.async_warning('密码字典中不存在此图像的密码，请输入密码')
                return image
            else:
                password = encryption_data.password
        else:
            password = encryption_data.password
    else:
        password = 100
    image_decrypt = ImageDecrypt(image, encryption_data.cutting_row, encryption_data.cutting_col, password, encryption_data.version)
    logger('正在处理')

    step_count = 0
    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        step_count += 2
    if encryption_data.XOR_channels:
        step_count += 1
    if save:
        step_count += 1

    bar = ProgressBar(gauge, step_count)

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
        name, suffix = splitext(frame.image_item.path_data.file_name)
        suffix = frame.controls.saving_format
        if suffix.lower() in ('jpg', 'jpeg'):
            image.convert('RGB')
        name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

        image.save(join(frame.controls.saving_path, name), quality=frame.controls.saving_quality, subsampling=frame.controls.saving_subsampling_level)
        bar.finish()
    bar.over()
    logger('完成')
    return image


@catch_exception_and_return
def batch(image_data, path_data: 'PathData', encryption_data, saving_settings, auto_folder: bool):
    image = Image.frombytes(*image_data)
    encryption_data = EncryptionParametersData(encryption_data)
    saving_settings = SavingSettings(*saving_settings)
    image_decrypt = ImageDecrypt(image, encryption_data.cutting_row, encryption_data.cutting_col, encryption_data.password if encryption_data.has_password else 100, encryption_data.version)

    if encryption_data.XOR_channels:
        image = image_decrypt.xor_pixels(encryption_data.XOR_channels, encryption_data.noise_XOR, encryption_data.noise_factor)

    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        image_decrypt.init_block_data(encryption_data.shuffle_chunks, encryption_data.flip_chunks, encryption_data.mapping_channels)
        image = image_decrypt.generate_image()

    if encryption_data.version >= 7:
        image = array_to_image(*image)
    image = image.crop((0, 0, encryption_data.orig_width, encryption_data.orig_height))

    name, suffix = splitext(path_data.file_name)
    suffix = saving_settings.format
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"
    if auto_folder:
        save_dir = join(saving_settings.path, path_data.relative_path)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_settings.path

    image.save(join(save_dir, name), quality=saving_settings.quality, subsampling=saving_settings.subsampling_level)
