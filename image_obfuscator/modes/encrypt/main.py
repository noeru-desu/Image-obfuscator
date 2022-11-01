"""
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-09-11 17:42:38
"""
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image

from image_obfuscator.frame.controller import ProgressBar
from image_obfuscator.modes.encrypt.core import ImageEncrypt
from image_obfuscator.modules.image import PillowImage, WrappedPillowImage

if TYPE_CHECKING:
    from wx import Gauge
    from image_obfuscator.modes.base import EmptySettings
    from image_obfuscator.modes.encrypt.settings import Settings
    from image_obfuscator.modules.image import WrappedImage, ImageData


def normal_gen(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedImage':
    step_count = 0
    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        step_count += 2
    if settings.XOR_encryption:
        step_count += 1
    if step_count < 1:
        return WrappedPillowImage(source)

    bar = ProgressBar(gauge, step_count)
    image_encrypt = ImageEncrypt(source, settings.cutting_row, settings.cutting_col, settings.available_password)
    label_text_setter('开始处理')

    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        label_text_setter('正在分割原图')
        bar.next_step(image_encrypt.base.block_num)
        image_encrypt.init_block_data(settings.shuffle_chunks, settings.flip_chunks, settings.mapping_channels, bar)

        label_text_setter('正在重组')
        bar.next_step(image_encrypt.base.block_num)
        image = image_encrypt.generate_image(bar)

    if settings.XOR_encryption:
        bar.next_step(1)
        label_text_setter('正在异或加密')
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)

    image = return_type(*image)
    bar.over()
    label_text_setter('完成')
    return image


def normal_gen_quietly(source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EmptySettings') -> 'WrappedImage':
    if not settings.shuffle_chunks and not settings.flip_chunks and not settings.mapping_channels and not settings.XOR_encryption:
        return WrappedPillowImage(source)

    image_encrypt = ImageEncrypt(source, settings.cutting_row, settings.cutting_col, settings.available_password)

    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        image_encrypt.init_block_data(settings.shuffle_chunks, settings.flip_chunks, settings.mapping_channels)
        image = image_encrypt.generate_image()

    if settings.XOR_encryption:
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)

    image = return_type(*image)
    return image
