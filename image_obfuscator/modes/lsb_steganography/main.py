"""
Author       : noeru_desu
Date         : 2021-11-20 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2022-11-26 09:42:53
"""
from os.path import isfile, splitext, join
from math import ceil
from typing import TYPE_CHECKING, Callable, Union, Type

from PIL import Image
from orjson import loads

from image_obfuscator.constants import SKIP_CUSTOM_SAVE, SKIP_DISPLAY_PREVIEW
from image_obfuscator.modes.lsb_steganography.settings import Settings
from image_obfuscator.modes.lsb_steganography.core import encode, decode
from image_obfuscator.modes.lsb_steganography.utils import gen_lsb_info_json
from image_obfuscator.modules.image import WrappedPillowImage

if TYPE_CHECKING:
    from wx import Gauge
    from image_obfuscator.frame.image_saver import SaveSettings
    from image_obfuscator.frame. file_item import ImageItem
    from image_obfuscator.modes.base import EmptySettings
    from image_obfuscator.modes.lsb_steganography import ModeInterface
    from image_obfuscator.modes.lsb_steganography.settings import Settings
    from image_obfuscator.modules.image import WrappedImage, ImageData, PillowImage


def normal_gen(interface: 'ModeInterface', source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EmptySettings', label_text_setter: Callable, gauge: 'Gauge') -> 'WrappedImage':
    gauge.SetValue(0)
    label_text_setter('正在处理')
    if settings.lsb_mode == 0:
        image = encode_mode(interface, source, settings)
    else:
        image = decode_mode(interface, source, settings, True)
    gauge.SetValue(gauge.Range)
    label_text_setter('完成')
    return image


def encode_mode(interface: 'ModeInterface', outside: 'Image.Image', settings: 'Settings'):
    if not isfile(settings.inside_file_path):
        settings.inside_file_path = interface.settings_controller.inside_file = ''
        settings.compression_ratio = interface.settings_controller.compression_ratio = None
        return
    if settings.lsb_ratio is None:
        settings.lsb_ratio = interface.settings_controller._cal_lsb_ratio(outside, settings.lsb_num, settings.use_alpha, settings.inside_file_path)
    if settings.lsb_ratio > 1:
        if settings.auto_zoom_in:
            outside = outside.resize((ceil(outside.size[0] * settings.lsb_ratio), ceil(outside.size[1] * settings.lsb_ratio)))
        else:
            return
    elif settings.lsb_ratio < 1:
        if settings.auto_zoom_out:
            outside = outside.resize((ceil(outside.size[0] * settings.lsb_ratio), ceil(outside.size[1] * settings.lsb_ratio)))
    if not settings.use_alpha:
        alpha = outside.getchannel('A')
        outside = outside.convert('RGB')
    outside_data = interface.compressed_file_manager.open_file(settings.inside_file_path)
    if not isinstance(outside_data, bytes):
        compressor = outside_data.compressor
        outside_data = outside_data.load_compressed_data()
    else:
        compressor = 0
    lsb_info = gen_lsb_info_json(compressor, settings.inside_file_path)
    image = encode(outside, outside_data, settings.lsb_num, lsb_info + b'\xdd\xcc\xbb\xaa', settings.use_alpha)
    if not settings.use_alpha:
        image.putalpha(alpha)
    return WrappedPillowImage(image)


def decode_mode(interface: 'ModeInterface', outside: 'Image.Image', settings: 'Settings', test: bool = False):
    if not settings.use_alpha:
        outside = outside.convert('RGB')
    try:
        file_data, extra_data = decode(outside, settings.lsb_num, settings.use_alpha)
    except Exception as e:
        if test:
            interface.main_frame.dialog.async_error(
                '尝试提取时出现以下错误: \n(注: 程序运行正常, 这不是Bug)\n'
                '{}\n请检查设置是否正确\n已自动切换到 写入 模式'.format(repr(e).replace("\\n", " ")), '无法提取')
            interface.settings_controller.lsb_mode = 0
            interface.main_frame.sync_setting(interface.settings_panel.lsbMode)
            return SKIP_DISPLAY_PREVIEW
        return None, None
    else:
        if extra_data.endswith(b'\xdd\xcc\xbb\xaa'):
            if test:
                return
            return file_data, extra_data.removesuffix(b'\xdd\xcc\xbb\xaa')
        else:   # 应该不存在此类情况, 不存在分隔符会引发ValueError
            if test:
                interface.main_frame.dialog.async_info('尝试提取时没有出现错误, 但没有检测到LSB标识', '提取测试')
                return
            return file_data, None


def detect(outside: 'Image.Image', lsb_num: int, use_alpha: bool):
    if not use_alpha:
        outside = outside.convert('RGB')
    try:
        _, extra_data = decode(outside, lsb_num, use_alpha)
    except Exception:
        return 0
    else:
        return 2 if extra_data.endswith(b'\xdd\xcc\xbb\xaa') else 1


def save_image(interface: 'ModeInterface', source: 'Image.Image', image_item: 'ImageItem', settings: 'Settings', _, save_settings: 'SaveSettings', relative_save_path: str, quiet: bool):
    if settings.lsb_mode == 0:
        return SKIP_CUSTOM_SAVE
    file_data, info_json = decode_mode(interface, source, settings)
    if file_data is None:
        interface.main_frame.dialog.async_error('无法从所载入的图像中提取文件', '无法提取')
        return
    lsb_info = loads(info_json)
    save_path = join(save_settings.path, relative_save_path, f'{splitext(image_item.path_data.file_name)[0]}-extracted.{lsb_info["FS"]}')
    with open(save_path, 'wb') as f:
        f.write(file_data if lsb_info['CA'] == 0 else interface.compressed_file_manager.decompress_data(file_data, lsb_info['CA']))


def normal_gen_quietly(interface, source: 'Image.Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'Settings', encryption_parameters: 'EmptySettings') -> 'WrappedImage':
    if settings.lsb_mode == 0:
        image = encode_mode(interface, source, settings)
    else:
        return None
    return image
