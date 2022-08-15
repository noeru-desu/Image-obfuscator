"""
Author       : noeru_desu
Date         : 2022-08-13 16:27:28
LastEditors  : noeru_desu
LastEditTime : 2022-08-15 09:29:22
Description  : 生成幻影坦克的核心函数
Reference    : https://github.com/Aloxaf/MirageTankGo
"""
from typing import TYPE_CHECKING

from numpy import (ascontiguousarray, dstack, float16, float32, float64, uint8, where,
                   zeros, seterr)
from PIL.Image import Image, new
from PIL.ImageEnhance import Brightness

from image_obfuscator.modules.image import cal_best_size

if TYPE_CHECKING:
    from numpy import ndarray

accuracy = (float16, float32, float64)


def uniform_image_size(o_image: 'Image', i_image: 'Image', image_mode: str, resize_mode: int):
    o_image = o_image.convert(image_mode)
    i_image = i_image.convert(image_mode)
    ow, oh = o_image.size
    iw, ih = i_image.size
    max_w = max(ow, iw)
    max_h = max(oh, ih)
    unified_o_image = new(image_mode, (max_w, max_h), 255)
    unified_i_image = new(image_mode, (max_w, max_h), 0)
    match resize_mode:
        case 0:
            o_image = o_image.resize((max_w, max_h))
            i_image = i_image.resize((max_w, max_h))
            unified_o_image.paste(o_image)
            unified_i_image.paste(i_image)
        case 1:
            o_image = o_image.resize(cal_best_size(ow, oh, max_w, max_h))
            i_image = i_image.resize(cal_best_size(iw, ih, max_w, max_h))
            ow, oh = o_image.size
            iw, ih = i_image.size
            unified_o_image.paste(o_image, ((max_w - ow) // 2, (max_h - oh) // 2))
            unified_i_image.paste(i_image, ((max_w - iw) // 2, (max_h - ih) // 2))
    return unified_o_image, unified_i_image


def gray_mode(i_image: 'Image', o_image: 'Image', o_brightness: float, i_brightness: float, damier: bool, resize_mode: int, accuracy_lvl: int) -> 'ndarray':
    seterr(divide='ignore', invalid='ignore')
    o_image, i_image = uniform_image_size(o_image, i_image, 'L', resize_mode)

    dtype = accuracy[accuracy_lvl]
    o_array = ascontiguousarray(o_image, dtype)
    i_array = ascontiguousarray(i_image, dtype)

    if damier:
        o_array[::2, ::2] = 255.0
        i_array[1::2, 1::2] = 0.0

    o_array *= o_brightness
    i_array *= i_brightness

    a = 1.0 - o_array / 255.0 + i_array / 255.0
    r = where(a != 0, i_array / a, 255.0)

    pixels = dstack((r, r, r, a * 255.0))

    pixels[pixels > 255] = 255

    return ascontiguousarray(pixels, uint8)



def colorful_mode(i_image: 'Image', o_image: 'Image', o_brightness: float, i_brightness: float, o_color: float , i_color: float, damier: bool, resize_mode: int, accuracy_lvl: int) -> 'ndarray':
    seterr(divide='ignore', invalid='ignore')
    o_image, i_image = uniform_image_size(
        Brightness(o_image).enhance(o_brightness),
        Brightness(i_image).enhance(i_brightness),
        'RGB', resize_mode
    )

    dtype = accuracy[accuracy_lvl]
    o_array = ascontiguousarray(o_image, dtype)
    i_array = ascontiguousarray(i_image, dtype)

    if damier:
        o_array[::2, ::2] = [255., 255., 255.]
        i_array[1::2, 1::2] = [0., 0., 0.]

    o_array /= 255.
    i_array /= 255.

    o_gray = o_array[:, :, 0] * 0.334 + o_array[:, :, 1] * 0.333 + o_array[:, :, 2] * 0.333
    o_array *= o_color
    o_array[:, :, 0] += o_gray * (1. - o_color)
    o_array[:, :, 1] += o_gray * (1. - o_color)
    o_array[:, :, 2] += o_gray * (1. - o_color)

    i_gray = i_array[:, :, 0] * 0.334 + i_array[:, :, 1] * 0.333 + i_array[:, :, 2] * 0.333
    i_array *= i_color
    i_array[:, :, 0] += i_gray * (1. - i_color)
    i_array[:, :, 1] += i_gray * (1. - i_color)
    i_array[:, :, 2] += i_gray * (1. - i_color)

    d = 1. - o_array + i_array

    d[:, :, 0] = d[:, :, 1] = d[:, :, 2] = d[:, :, 0] * 0.222 + d[:, :, 1] * 0.707 + d[:, :, 2] * 0.071

    p = where(d != 0, i_array / d * 255., 255.)
    a = d[:, :, 0] * 255.

    colors = zeros((p.shape[0], p.shape[1], 4))
    colors[:, :, :3] = p
    colors[:, :, -1] = a

    colors[colors > 255] = 255

    return ascontiguousarray(colors, uint8)
