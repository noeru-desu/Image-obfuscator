"""
Author       : noeru_desu
Date         : 2022-09-11 17:31:05
LastEditors  : noeru_desu
LastEditTime : 2022-09-11 17:35:14
"""
from typing import TYPE_CHECKING, Union

from image_obfuscator.constants import EA_VERSION
from image_obfuscator.modes.encrypt.core import BaseImageEncryptV1, BaseImageEncryptV2, BaseImageEncryptV3
from image_obfuscator.utils.misc_utils import FakeBar

if TYPE_CHECKING:
    from PIL.Image import Image
    from numpy import ndarray
    from image_obfuscator.modes.base import Channels


class ImageDecrypt(object):
    __slots__ = ('base',)

    def __init__(self, image: 'Image', row: int, col: int, random_seed, version=EA_VERSION) -> None:
        if version >= 7:
            self.base = BaseImageEncryptV3(image, row, col, random_seed, True)
        elif version >= 5:
            self.base = BaseImageEncryptV2(image, row, col, random_seed, True)
        else:
            self.base = BaseImageEncryptV1(image, row, col, random_seed, True)

    def init_block_data(self, shuffle: bool, flip: bool, mapped_channels: 'Channels', bar=FakeBar):
        return self.base.init_block_data(True, shuffle, flip, mapped_channels, bar)

    def generate_image(self, bar=FakeBar) -> Union[tuple['ndarray', tuple[int, int]], 'Image']:
        return self.base.generate_image(bar)

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255) -> Union[tuple['ndarray', tuple[int, int]], 'Image']:
        return self.base.xor_pixels(channels, noise, noise_factor)
