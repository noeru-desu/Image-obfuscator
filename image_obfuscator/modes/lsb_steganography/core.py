"""
Author       : noeru_desu
Date         : 2022-11-20 12:33:03
LastEditors  : noeru_desu
LastEditTime : 2022-11-22 09:43:53
"""
from sys import byteorder
from os.path import getsize
from typing import TYPE_CHECKING, Optional

from numpy import array, frombuffer, uint8
from stego_lsb.bit_manipulation import roundup, lsb_interleave_bytes, lsb_deinterleave_bytes

from image_obfuscator.modules.image import PIL_image_from_array

if TYPE_CHECKING:
    from os import PathLike
    from PIL.Image import Image
    from numpy import ndarray

DELIMITER = b'\xaa\xbb\xcc\xdd'
DELIMITER_LEN = len(DELIMITER)


class SizeError(ValueError): pass


def decode(steg_image: 'Image', num_lsb: int, use_alpha: bool = False) -> tuple[bytes, bytes]:
    color_data = array(steg_image, dtype=uint8).flatten()

    file_size_tag_size = bytes_in_max_file_size(steg_image, num_lsb, 4 if use_alpha else 3)
    tag_bit_height = roundup(8 * file_size_tag_size / num_lsb)

    bytes_to_recover = int.from_bytes(
        lsb_deinterleave_list(
            color_data[:tag_bit_height], 8 * file_size_tag_size, num_lsb
        ),
        byteorder=byteorder,
    )

    maximum_bytes_in_image = (max_bits_to_hide(steg_image, num_lsb, 4 if use_alpha else 3) // 8 - file_size_tag_size)
    if bytes_to_recover > maximum_bytes_in_image:
        raise SizeError(
            "This image appears to be corrupted.\n"
            f"It claims to hold {bytes_to_recover} B, "
            f"but can only hold {maximum_bytes_in_image} B with {num_lsb} LSBs"
        )

    split_data = lsb_deinterleave_list(color_data, 8 * (bytes_to_recover + file_size_tag_size), num_lsb)[file_size_tag_size:].split(DELIMITER)
    if len(split_data) > 2:
        file_data = b''
        for i in split_data[1:]:
            file_data += i
        extra_data = split_data[0]
    else:
        extra_data, file_data = split_data
    return file_data, extra_data


def encode(outside: 'Image', inside: 'PathLike', num_lsb: int, extra_data: Optional[bytes] = None, use_alpha: bool = False) -> 'Image':
    # image_data = outside.getdata()
    # num_channels = len(image_data[0])
    # flattened_color_data = list(chain.from_iterable(image_data))
    image_data = array(outside, dtype=uint8)
    flattened_color_data = image_data.flatten()

    # We add the size of the input file to the beginning of the payload.
    with open(inside, 'rb') as f:
        inside_data = f.read()
    inside_size = len(inside_data) + DELIMITER_LEN + (1 if extra_data is None else len(extra_data))
    file_size_tag = inside_size.to_bytes(bytes_in_max_file_size(outside, num_lsb), byteorder=byteorder)
    data = file_size_tag + (b'\0' if extra_data is None else extra_data) + DELIMITER + inside_data

    available_size = max_bits_to_hide(outside, num_lsb, 4 if use_alpha else 3)
    required_size = len(data)
    if 8 * required_size > available_size:
        raise SizeError(
            f"Only able to hide {available_size // 8} bytes in this image "
            f"with {num_lsb} LSBs, but {required_size} bytes were requested"
        )

    flattened_color_data = lsb_interleave_list(flattened_color_data, data, num_lsb)

    return PIL_image_from_array(flattened_color_data.reshape(image_data.shape, order='C'), use_memoryview=True)


def lsb_interleave_list(carrier: 'ndarray', payload, num_lsb) -> 'ndarray':
    """修改自`stego_lsb.LSBSteg.lsb_interleave_list`,
    `carrier`和返回值都由展平的`list`改为展平的`ndarray`"""
    bit_height = roundup(8 * len(payload) / num_lsb)
    carrier_bytes = carrier[:bit_height].tobytes()
    interleaved = lsb_interleave_bytes(carrier_bytes, payload, num_lsb, truncate=True)
    carrier[:bit_height] = frombuffer(interleaved, dtype=uint8)
    return carrier


def lsb_deinterleave_list(carrier: 'ndarray', num_bits, num_lsb):
    """修改自`stego_lsb.LSBSteg.lsb_interleave_list`,
    `carrier`由展平的`list`改为展平的`ndarray`"""
    plen = roundup(num_bits / num_lsb)
    carrier_bytes = carrier[:plen].tobytes()
    return lsb_deinterleave_bytes(carrier_bytes, num_bits, num_lsb)


def max_bits_to_hide(image: 'Image', num_lsb: int, channel: int = 3):
    """修改自`stego_lsb.LSBSteg.max_bits_to_hide`,
    添加`channel`以计算非3通道图像的最大数据存储量"""
    return int(channel * image.size[0] * image.size[1] * num_lsb)


def bytes_in_max_file_size(image: 'Image', num_lsb: int, channel: int = 3):
    """修改自`stego_lsb.LSBSteg.bytes_in_max_file_size`,
    添加`channel`以计算非3通道图像的最大数据存储量"""
    return roundup(max_bits_to_hide(image, num_lsb, channel).bit_length() / 8)


def cal_required_size(outside: 'Image', inside: 'PathLike', num_lsb: int, extra_data_length: int = 1, use_alpha: bool = False):
    """使用`inside`文件属性提供的大小计算隐写所需比特数"""
    inside_size = getsize(inside)
    file_size_tag = inside_size.to_bytes(bytes_in_max_file_size(outside, num_lsb, 4 if use_alpha else 3), byteorder=byteorder)
    return (len(file_size_tag) + DELIMITER_LEN + (1 if extra_data_length is None else extra_data_length) + inside_size) * 8
