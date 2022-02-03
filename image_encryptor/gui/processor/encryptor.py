'''
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-02-03 13:48:31
Description  : 单文件加密功能
'''
from json import dumps
from os import makedirs
from os.path import isdir, join, split, splitext
from traceback import format_exc
from typing import TYPE_CHECKING

from image_encryptor.common.modules.image_encrypt import ImageEncrypt
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.common.modules.version_adapter import get_encryption_parameters
from image_encryptor.common.utils.utils import FakeBar
from image_encryptor.gui.frame.controls import ProgressBar, SettingsData, SavingSettings
from PIL import Image

if TYPE_CHECKING:
    from image_encryptor.gui.frame.events import MainFrame


def normal(frame: 'MainFrame', logger, gauge, image: 'Image.Image', save: bool):
    try:
        return False, _normal(frame, logger, gauge, image, save)
    except Exception:
        return True, format_exc()


def batch(image_data, path_data, settings, saving_format, auto_folder):
    try:
        return False, _batch(image_data, path_data, SettingsData(settings), SavingSettings(*saving_format), auto_folder)
    except Exception:
        return True, format_exc()


def _normal(frame: 'MainFrame', logger, gauge, image: 'Image.Image', save):
    settings = frame.settings.all
    password = 100 if settings.password == 'none' else settings.password
    if save:
        has_password = settings.password != 'none'
        name, suffix = splitext(split(frame.image_item.loaded_image_path)[1])
        suffix = settings.saving_format
        original_size = image.size

        if suffix in ('jpg', 'jpeg', 'wmf', 'webp'):
            if settings.RGB_mapping:
                frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用RGB(A)随机映射会导致图片在解密后出现轻微的分界线', '不可逆处理警告')
            if settings.XOR_channels:
                frame.dialog.warning('注意: 当前保存格式为有损压缩格式，在此情况下，使用异或加密会导致图片解密后出现严重失真', '不可逆处理警告')

    step_count = 0
    if settings.shuffle_chunks or settings.flip_chunks or settings.RGB_mapping:
        step_count += 2
    if settings.XOR_channels:
        step_count += 1
    if save:
        step_count += 1

    image_encrypt = ImageEncrypt(image, settings.cutting_row, settings.cutting_col, password)
    logger('开始处理')

    bar = ProgressBar(gauge, step_count)

    if settings.shuffle_chunks or settings.flip_chunks or settings.RGB_mapping:
        block_num = settings.cutting_row * settings.cutting_col
        logger('正在分割原图')
        bar.next_step(block_num)
        image_encrypt.init_block_data(False, settings.shuffle_chunks, settings.flip_chunks, settings.RGB_mapping, bar)

        logger('正在重组')
        bar.next_step(block_num)
        image = image_encrypt.generate_image(bar)

    if settings.XOR_channels:
        bar.next_step(1)
        logger('正在异或加密')
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)

    if save:
        bar.next_step(1)
        logger('完成，正在保存文件')
        name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
        output_path = join(settings.saving_path, name)
        if suffix.lower() in ('jpg', 'jpeg'):
            image.convert('RGB')

        image.save(output_path, quality=settings.saving_quality, subsampling=settings.saving_subsampling_level)

        parameters = {
            'col': settings.cutting_col,
            'row': settings.cutting_row,
            'shuffle': settings.shuffle_chunks,
            'flip': settings.flip_chunks,
            'rgb_mapping': settings.RGB_mapping,
            'xor_channels': settings.XOR_channels,
            'noise_xor': settings.noise_XOR,
            'noise_factor': settings.noise_factor
        }

        password_base64 = PasswordDict.get_validation_field_base64(password) if has_password else 0
        with open(output_path, "a") as f:
            f.write('\n' + dumps(get_encryption_parameters(*original_size, parameters, has_password, password_base64), separators=(',', ':')))
        bar.finish()
    bar.over()
    logger('完成')
    return image


def _batch(image_data, path_data, settings: 'SettingsData', saving_settings: 'SavingSettings', auto_folder):
    image = Image.frombytes(*image_data)
    password = 100 if settings.password == 'none' else settings.password
    has_password = settings.password != 'none'
    name, suffix = splitext(path_data[-1])
    suffix = saving_settings.format
    original_size = image.size

    image_encrypt = ImageEncrypt(image, settings.cutting_row, settings.cutting_col, password)

    if settings.shuffle_chunks or settings.flip_chunks or settings.RGB_mapping:
        image_encrypt.init_block_data(False, settings.shuffle_chunks, settings.flip_chunks, settings.RGB_mapping, FakeBar)
        image = image_encrypt.generate_image(FakeBar)

    if settings.XOR_channels:
        image = image_encrypt.xor_pixels(settings.XOR_channels, settings.noise_XOR, settings.noise_factor)

    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    if auto_folder:
        save_dir = join(saving_settings.path, path_data[1])
        if not isdir(save_dir):
            makedirs(save_dir)
    else:
        save_dir = saving_settings.path
    output_path = join(save_dir, name)
    if suffix.lower() in ('jpg', 'jpeg'):
        image.convert('RGB')

    image.save(output_path, quality=saving_settings.quality, subsampling=saving_settings.subsampling_level)

    parameters = {
        'col': settings.cutting_col,
        'row': settings.cutting_row,
        'shuffle': settings.shuffle_chunks,
        'flip': settings.flip_chunks,
        'rgb_mapping': settings.RGB_mapping,
        'xor_channels': settings.XOR_channels,
        'noise_xor': settings.noise_XOR,
        'noise_factor': settings.noise_factor
    }

    password_base64 = PasswordDict.get_validation_field_base64(password) if has_password else 0
    with open(output_path, "a") as f:
        f.write('\n' + dumps(get_encryption_parameters(*original_size, parameters, has_password, password_base64), separators=(',', ':')))
