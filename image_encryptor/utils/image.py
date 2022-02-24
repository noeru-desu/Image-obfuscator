"""
Author       : noeru_desu
Date         : 2022-02-06 19:28:02
LastEditors  : noeru_desu
LastEditTime : 2022-02-24 21:15:14
Description  : 图像相关工具
"""
from functools import cache
from itertools import permutations
from random import randrange
from random import seed as random_seed
from re import sub

from numpy import squeeze, uint8
from numpy.random import randint
from numpy.random import seed as np_random_seed
from PIL import Image


@cache
def gen_mapping_table(nc):
    if not nc or len(nc) == 1:
        return None, None
    nc_str = sub(f'[{nc}]', '{}', 'r, g, b, a')
    lambda_str_for_encryption = f'lambda r, g, b, a: ({nc_str})'
    lambda_str_for_decryption = f'lambda {nc_str}: (r, g, b, a)'
    if len(nc) == 2:
        return (eval(lambda_str_for_encryption.format(nc[1], nc[0])),), (eval(lambda_str_for_decryption.format(nc[1], nc[0])),)
    mapping_table_for_encryption = []
    mapping_table_for_decryption = []
    for i in permutations(nc, len(nc)):
        mapping_table_for_encryption.append(eval(lambda_str_for_encryption.format(*i)))
        mapping_table_for_decryption.append(eval(lambda_str_for_decryption.format(*i)))
    return mapping_table_for_encryption, mapping_table_for_decryption


def random_noise(width: int, height: int, nc: int, seed, factor: int, ndarray=True):
    """Generator a random noise image from numpy.array.

    If nc is 1, the Grayscale image will be created.
    If nc is 3, the RGB image will be generated.
    If nc is 4, the RGBA image will be generated.

    Args:
        nc (int): (1, 3 or 4) number of channels.
        width (int): width of output image.
        height (int): height of output image.
    Returns:
        ndarray or PIL Image.
    """
    if factor > 255:
        factor = 255
    elif factor < 1:
        factor = 1
    random_seed(seed)
    seed = randrange(0, 2 ** 32)
    np_random_seed(seed)
    image = randint(0, factor + 1, (height, width, nc), uint8)   # [rc.4修改方法]
    # image = (np_random.rand(height, width, nc) * factor).astype(uint8) [rc.3使用方法]
    if ndarray:
        return image
    else:
        if nc == 1:
            return Image.fromarray(squeeze(image), mode='L')
        elif nc == 3:
            return Image.fromarray(image, mode='RGB')
        elif nc == 4:
            return Image.fromarray(image, mode='RGBA')
        else:
            raise ValueError(f'Input nc should be 1/3/4. Got {nc}.')
