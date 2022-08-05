"""
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2022-06-24 12:15:28
Description  : 单文件解密功能
"""
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image

from image_encryptor.frame.controller import  ProgressBar, SaveSettings
from image_encryptor.modules.image import (PillowImage, WrappedPillowImage,
                                           array_to_image, crop_array)
from image_encryptor.modules.image_encrypt import ImageDecrypt
from image_encryptor.modules.decorator import catch_exc_and_return

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modes.base import EmptySettings
    from image_encryptor.modes.decrypt.settings import EncryptionParameters, EncryptionParametersData
    from image_encryptor.modules.image import WrappedImage, ImageData
    from wx import Gauge


def normal_gen(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EncryptionParameters', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedImage':
    password = encryption_parameters.get_password()
    if password is None:
        frame.dialog.async_warning('密码字典中不存在此图像的密码')
        return WrappedPillowImage(source, cacheable=False)
    step_count = 0
    if encryption_parameters.shuffle_chunks or encryption_parameters.flip_chunks or encryption_parameters.mapping_channels:
        step_count += 2
    if encryption_parameters.XOR_channels:
        step_count += 1
    if step_count < 1:
        return WrappedPillowImage(source)

    bar = ProgressBar(gauge, step_count)
    image_decrypt = ImageDecrypt(source, encryption_parameters.cutting_row, encryption_parameters.cutting_col, password, encryption_parameters.version)
    label_text_setter('开始处理')

    if encryption_parameters.XOR_encryption:
        label_text_setter('正在异或解密')
        bar.next_step(1)
        image = image_decrypt.xor_pixels(encryption_parameters.XOR_channels, encryption_parameters.noise_XOR, encryption_parameters.noise_factor)

    if encryption_parameters.shuffle_chunks or encryption_parameters.flip_chunks or encryption_parameters.mapping_channels:
        bar.next_step(image_decrypt.base.block_num)
        label_text_setter('正在分割加密图像')
        image_decrypt.init_block_data(encryption_parameters.shuffle_chunks, encryption_parameters.flip_chunks, encryption_parameters.mapping_channels, bar)

        label_text_setter('正在重组')

        bar.next_step(image_decrypt.base.block_num)
        image = image_decrypt.generate_image(bar)

    if encryption_parameters.version >= 7:
        arr = crop_array(image[0], encryption_parameters.orig_height, encryption_parameters.orig_width)
        image = return_type(arr, (encryption_parameters.orig_width, encryption_parameters.orig_height))
    else:
        image = WrappedPillowImage(image.crop((0, 0, encryption_parameters.orig_width, encryption_parameters.orig_height)))

    bar.over()
    label_text_setter('完成')
    return image


def normal_gen_quietly(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EncryptionParameters') -> 'WrappedImage':
    password = encryption_parameters.get_password()
    if password is None:
        frame.dialog.async_warning('密码字典中不存在此图像的密码')
        return WrappedPillowImage(source, cacheable=False)
    step_count = 0
    if encryption_parameters.shuffle_chunks or encryption_parameters.flip_chunks or encryption_parameters.mapping_channels:
        step_count += 2
    if encryption_parameters.XOR_channels:
        step_count += 1
    if step_count < 1:
        return WrappedPillowImage(source)

    image_decrypt = ImageDecrypt(source, encryption_parameters.cutting_row, encryption_parameters.cutting_col, password, encryption_parameters.version)

    if encryption_parameters.XOR_encryption:
        image = image_decrypt.xor_pixels(encryption_parameters.XOR_channels, encryption_parameters.noise_XOR, encryption_parameters.noise_factor)

    if encryption_parameters.shuffle_chunks or encryption_parameters.flip_chunks or encryption_parameters.mapping_channels:
        image_decrypt.init_block_data(encryption_parameters.shuffle_chunks, encryption_parameters.flip_chunks, encryption_parameters.mapping_channels,)
        image = image_decrypt.generate_image()

    if encryption_parameters.version >= 7:
        arr = crop_array(image[0], encryption_parameters.orig_height, encryption_parameters.orig_width)
        image = return_type(arr, (encryption_parameters.orig_width, encryption_parameters.orig_height))
    else:
        image = WrappedPillowImage(image.crop((0, 0, encryption_parameters.orig_width, encryption_parameters.orig_height)))

    return image


def normal_save(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], encryption_data: 'EncryptionParameters', label_text_setter: Callable, gauge: 'Gauge') -> 'PillowImage':
    password = encryption_data.get_password()
    if password is None:
        frame.dialog.async_warning('密码字典中不存在此图像的密码')
        return WrappedPillowImage(source, cacheable=False)
    step_count = 1
    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        step_count += 2
    if encryption_data.XOR_channels:
        step_count += 1
    if step_count < 2:
        return WrappedPillowImage(source)

    bar = ProgressBar(gauge, step_count)
    image_decrypt = ImageDecrypt(source, encryption_data.cutting_row, encryption_data.cutting_col, password, encryption_data.version)
    label_text_setter('开始处理')

    if encryption_data.XOR_channels:
        label_text_setter('正在异或解密')
        bar.next_step(1)
        image = image_decrypt.xor_pixels(encryption_data.XOR_channels, encryption_data.noise_XOR, encryption_data.noise_factor)

    if encryption_data.shuffle_chunks or encryption_data.flip_chunks or encryption_data.mapping_channels:
        bar.next_step(image_decrypt.base.block_num)
        label_text_setter('正在分割加密图像')
        image_decrypt.init_block_data(encryption_data.shuffle_chunks, encryption_data.flip_chunks, encryption_data.mapping_channels, bar)

        label_text_setter('正在重组')

        bar.next_step(image_decrypt.base.block_num)
        image = image_decrypt.generate_image(bar)

    if encryption_data.version >= 7:
        arr = crop_array(image[0], encryption_data.orig_height, encryption_data.orig_width)
        image = return_type(arr, (encryption_data.orig_width, encryption_data.orig_height))
    else:
        image = WrappedPillowImage(image.crop((0, 0, encryption_data.orig_width, encryption_data.orig_height)))

    bar.next_step(1)
    label_text_setter('正在保存文件')
    _save_image(
        image, frame.image_item.path_data, frame.controller.save_path, frame.controller.save_format,
        frame.controller.save_quality, frame.controller.save_subsampling_level
    )
    bar.finish()
    bar.over()
    label_text_setter('完成')
    return image


def batch(image_data, path_data: 'PathData', encryption_data, save_settings, auto_folder: bool):
    save_settings = SaveSettings(*save_settings)

    image = process(Image.frombytes(*image_data), EncryptionParametersData(encryption_data))

    _save_image(
        image, path_data, save_settings.path, save_settings.format,
        save_settings.quality, save_settings.subsampling_level, auto_folder
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


def _save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', save_path: str, save_format: str, quality: int, subsampling: int, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name.replace('-encrypted', '')}-decrypted.{save_format}"
    if auto_folder:
        save_dir = join(save_path, image_path_data.relative_save_dir)
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = save_path
    if save_format.lower() in {'jpg', 'jpeg'}:
        image.convert('RGB')

    image.save(join(save_dir, name), quality=quality, subsampling=subsampling)


save_image = catch_exc_and_return(_save_image)