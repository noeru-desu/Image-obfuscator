"""
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2022-10-02 19:29:40
Description  : 单文件解密功能
"""
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image

from image_obfuscator.frame.controller import  ProgressBar
from image_obfuscator.modes.base import EmptySettings
from image_obfuscator.modules.image import (PillowImage, WrappedPillowImage,
                                            crop_array)
from image_obfuscator.modes.decrypt.core import ImageDecrypt

if TYPE_CHECKING:
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.modes.decrypt.settings import Settings
    from image_obfuscator.modes.decrypt.settings import EncryptionParameters
    from image_obfuscator.modules.image import WrappedImage, ImageData
    from wx import Gauge


def normal_gen(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EncryptionParameters', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedImage':
    parameters = settings if encryption_parameters is EmptySettings else encryption_parameters
    password = parameters.get_password()
    if password is None:
        frame.dialog.async_warning('密码字典中不存在此图像的密码')
        return None
    step_count = 0
    if parameters.shuffle_chunks or parameters.flip_chunks or parameters.mapping_channels:
        step_count += 2
    if parameters.XOR_encryption:
        step_count += 1
    if step_count < 1:
        return WrappedPillowImage(source)

    bar = ProgressBar(gauge, step_count)
    image_decrypt = ImageDecrypt(source, parameters.cutting_row, parameters.cutting_col, password, parameters.version)
    label_text_setter('开始处理')

    if parameters.XOR_encryption:
        label_text_setter('正在异或解密')
        bar.next_step(1)
        image = image_decrypt.xor_pixels(parameters.XOR_channels, parameters.noise_XOR, parameters.noise_factor)

    if parameters.shuffle_chunks or parameters.flip_chunks or parameters.mapping_channels:
        bar.next_step(image_decrypt.base.block_num)
        label_text_setter('正在分割加密图像')
        image_decrypt.init_block_data(parameters.shuffle_chunks, parameters.flip_chunks, parameters.mapping_channels, bar)

        label_text_setter('正在重组')

        bar.next_step(image_decrypt.base.block_num)
        image = image_decrypt.generate_image(bar)

    if parameters.version >= 7:
        arr = crop_array(image[0], parameters.orig_height, parameters.orig_width)
        image = return_type(arr, (parameters.orig_width, parameters.orig_height))
    else:
        image = WrappedPillowImage(image.crop((0, 0, parameters.orig_width, parameters.orig_height)))

    bar.over()
    label_text_setter('完成')
    return image


def normal_gen_quietly(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'EmptySettings', encryption_parameters: 'EncryptionParameters') -> 'WrappedImage':
    password = encryption_parameters.get_password()
    if password is None:
        frame.dialog.async_warning('密码字典中不存在此图像的密码')
        return None
    step_count = 0
    if encryption_parameters.shuffle_chunks or encryption_parameters.flip_chunks or encryption_parameters.mapping_channels:
        step_count += 2
    if encryption_parameters.XOR_encryption:
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
