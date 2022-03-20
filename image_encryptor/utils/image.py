"""
Author       : noeru_desu
Date         : 2022-02-06 19:28:02
LastEditors  : noeru_desu
LastEditTime : 2022-03-20 09:17:28
Description  : 图像相关工具
"""
from abc import ABC
from functools import cache
from itertools import permutations
from random import randrange
from random import seed as random_seed
from re import sub
from typing import TYPE_CHECKING, Iterable, Optional

from numpy import squeeze, uint8, zeros, ascontiguousarray
from numpy.random import randint
from numpy.random import seed as np_random_seed
from PIL import Image as PIL_Image
from wx import Bitmap, Image as wx_Image

from image_encryptor.constants import PIL_RESAMPLING_FILTERS, WX_RESAMPLING_FILTERS

if TYPE_CHECKING:
    from numpy import ndarray


@cache
def gen_mapping_table(nc, decryption=False) -> Optional[Iterable]:
    if len(nc) <= 1:
        return None
    nc_str = sub(f'[{nc}]', '{}', 'r, g, b, a')
    lambda_str = f'lambda {nc_str}: (r, g, b, a)' if decryption else f'lambda r, g, b, a: ({nc_str})'
    if len(nc) == 2:
        return (eval(lambda_str.format(nc[1], nc[0])),)
    return [eval(lambda_str.format(*i)) for i in permutations(nc, len(nc))]


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
    image = randint(0, factor + 1, (width, height, nc), uint8)   # [rc.4修改方法]
    # image = (np_random.rand(height, width, nc) * factor).astype(uint8) [rc.3使用方法]
    if ndarray:
        return image
    if nc == 1:
        return PIL_Image.fromarray(squeeze(image), mode='L')
    elif nc == 3:
        return PIL_Image.fromarray(image, mode='RGB')
    elif nc == 4:
        return PIL_Image.fromarray(image, mode='RGBA')
    else:
        raise ValueError(f'Input nc should be 1/3/4. Got {nc}.')


def split_channels(arr):
    return arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]


def merge_channels(arrays, shape):
    arr = zeros(shape, uint8, 'C')
    for i, v in enumerate(arrays):
        arr[..., i] = v
    return arr


def crop_array(array, width, height):
    return ascontiguousarray(array[:width, :height])


def array_to_image(array: 'ndarray', size: tuple = ...) -> 'PIL_Image.Image':
    if size is Ellipsis:
        size = array.shape[:-1:-1]
    return PIL_Image.frombuffer('RGBA', size, array.data, "raw", 'RGBA', 0, 1)


def array_to_bitmap(array: 'ndarray', size: tuple = ...) -> 'Bitmap':
    if size is Ellipsis:
        size = array.shape[:-1:-1]
    return Bitmap.FromBufferRGBA(*size, array.data)


class WrappedImage(ABC):
    __slots__ = ()

    @property
    def wxBitmap(self) -> 'Bitmap':
        raise NotImplementedError()

    @property
    def size(self) -> tuple[int, int]:
        raise NotImplementedError()

    def __init__(self, array: 'ndarray', size: tuple = ...) -> None:
        raise NotImplementedError()

    def resize(self, size: tuple[int, int], resampling_filter_id: int) -> None:
        raise NotImplementedError()

    def save(self, path: str, *args, **kwargs):
        raise NotImplementedError()


class PillowImage(WrappedImage):
    __slots__ = ('image',)

    def __init__(self, array: 'ndarray', size: tuple = ...) -> None:
        self.image = array_to_image(array, size)

    @property
    def wxBitmap(self) -> 'Bitmap':
        match self.image.mode:
            case 'RGBA':
                return Bitmap.FromBufferRGBA(*self.image.size, self.image.tobytes())
            case 'RGB':
                return Bitmap.FromBuffer(*self.image.size, self.image.tobytes())

    @property
    def size(self) -> tuple[int, int]:
        return self.image.size

    def convert(self, mode: Optional[str] = ..., *args, **kwargs):
        self.image = self.image.convert(mode, *args, **kwargs)

    def resize(self, size: tuple[int, int], resampling_filter_id: int):
        self.image = self.image.resize(size, PIL_RESAMPLING_FILTERS[resampling_filter_id])

    def save(self, path: str, *args, **kwargs):
        self.image.save(path, *args, **kwargs)


class WrappedPillowImage(PillowImage):
    __slots__ = ()

    def __init__(self, image: 'PIL_Image.Image') -> None:
        self.image = image


class wxImage(WrappedImage):
    __slots__ = ('image',)

    def __init__(self, array: 'ndarray', size: tuple = ...):
        if size is Ellipsis:
            size = array.shape[:-1:-1]
        self.image = wx_Image(size, array.data)

    @property
    def wxBitmap(self) -> 'Bitmap':
        return self.image.ConvertToBitmap()

    @property
    def size(self) -> tuple[int, int]:
        return self.image.GetSize()

    def resize(self, size: tuple[int, int], resampling_filter_id: int):
        self.image.Rescale(*size, WX_RESAMPLING_FILTERS[resampling_filter_id])
        return self


class ImageData(WrappedImage):
    __slots__ = ('wxBitmap',)

    def __init__(self, array: 'ndarray', size: tuple = ...) -> None:
        self.wxBitmap = array_to_bitmap(array, size)
