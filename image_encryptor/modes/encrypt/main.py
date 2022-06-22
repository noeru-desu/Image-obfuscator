"""
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-06-22 11:38:22
Description  : 加密模式
"""
from json import dumps
from os import makedirs
from os.path import isdir, join, splitext
from typing import TYPE_CHECKING, Any, Callable, Union, Type

from PIL import Image

from image_encryptor.frame.controller import ProgressBar, SavingSettings
from image_encryptor.modules.image_encrypt import ImageEncrypt
from image_encryptor.modules.image import (PillowImage, WrappedPillowImage,
                                           array_to_image)
from image_encryptor.modules.decorator import catch_exc_and_return
from image_encryptor.modes.encrypt.settings import SettingsData

if TYPE_CHECKING:
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.file_item import PathData
    from image_encryptor.modes.encrypt.settings import Settings
    from image_encryptor.modules.image import WrappedImage, ImageData


def normal_gen(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedImage':
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


def normal_gen_quietly(frame: 'MainFrame', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings') -> 'WrappedImage':
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


def normal_save(frame: 'MainFrame', source: 'Image.Image', settings: 'Settings', label_text_setter: Callable, gauge: 'Gauge') -> 'PillowImage':
    step_count = 1
    if settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels:
        step_count += 2
    if settings.XOR_encryption:
        step_count += 1
    if step_count < 2:
        return WrappedPillowImage(source)

    original_size = source.size

    if splitext(frame.image_item.path_data.file_name)[1] in ('jpg', 'jpeg', 'wmf', 'webp'):
        if settings.mapping_channels:
            frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用颜色通道随机映射会导致图像在解密后出现轻微的分界线', '不可逆处理警告')
        if settings.XOR_channels:
            frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用异或加密会导致图像解密后出现严重失真', '不可逆处理警告')

    bar = ProgressBar(gauge, step_count)
    image_encrypt = ImageEncrypt(source, settings.cutting_row, settings.cutting_col, settings.password)
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

    image = PillowImage(*image)
    bar.next_step(1)
    label_text_setter('完成，正在保存文件')
    _save_image(
        image, frame.image_item.path_data, settings.saving_path, settings.saving_format,
        settings.saving_quality, settings.saving_subsampling_level,
        settings.encryption_parameters_data(*original_size).encryption_parameters_data
    )
    bar.finish()
    bar.over()
    label_text_setter('完成')
    return image


def batch(image_data, path_data: 'PathData', settings, saving_format, auto_folder: bool):
    settings = SettingsData(settings)
    if not (settings.shuffle_chunks or settings.flip_chunks or settings.mapping_channels or settings.XOR_encryption):
        return
    image = Image.frombytes(*image_data)
    saving_settings = SavingSettings(*saving_format)
    original_size = image.size

    image = process(image, settings, settings.available_password)

    _save_image(
        array_to_image(*image), path_data, saving_settings.path, saving_settings.format,
        saving_settings.quality, saving_settings.subsampling_level,
        settings.encryption_parameters_data(*original_size).encryption_parameters_data,
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


def _save_image(image: Union['Image.Image', 'PillowImage'], image_path_data: 'PathData', saving_path: str, saving_format: str, quality: int, subsampling: int, encryption_parameters_data: dict, auto_folder=False):
    name, _ = splitext(image_path_data.file_name)
    name = f"{name.replace('-decrypted', '')}-encrypted.{saving_format}"
    if auto_folder:
        save_dir = join(saving_path, image_path_data.relative_saving_dir)
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


save_image = catch_exc_and_return(_save_image)
