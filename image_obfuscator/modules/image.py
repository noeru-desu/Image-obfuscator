"""
Author       : noeru_desu
Date         : 2022-02-06 19:28:02
LastEditors  : noeru_desu
LastEditTime : 2022-10-24 15:02:34
"""
from abc import ABC
from posixpath import splitext
# from functools import cache
# from itertools import permutations, combinations
from random import randrange
from random import seed as random_seed
# from traceback import print_exc
# from re import sub
from weakref import ref as weak_ref
from typing import TYPE_CHECKING, Optional, Union

from numpy import ascontiguousarray, squeeze, uint8, zeros
from numpy.random import randint
from numpy.random import seed as np_random_seed
from PIL import Image as PIL_Image
from PIL import UnidentifiedImageError, ImageFile
from wx import Bitmap
from wx import Image as wx_Image

from image_obfuscator.constants import (BLACK_IMAGE, OIERR_EXCEED_LIMIT,
                                       OIERR_NOT_EXIST, OIERR_OS_ERROR,
                                       OIERR_UNSUPPORTED_FORMAT,
                                       PIL_RESAMPLING_FILTERS,
                                       WX_RESAMPLING_FILTERS)
from image_obfuscator.utils.misc_utils import LRUCache

if TYPE_CHECKING:
    from os import PathLike
    from weakref import ReferenceType
    from numpy import ndarray

ImageFile.LOAD_TRUNCATED_IMAGES = True

'''
@cache# Optional[Iterable]
def gen_mapping_table(nc, decryption=False) -> str:
    if len(nc) <= 1:
        return None
    nc_str = sub(f'[{nc}]', '{}', 'r, g, b, a')
    # lambda_str = f'lambda {nc_str}: (r, g, b, a)' if decryption else f'lambda r, g, b, a: ({nc_str})'
    if len(nc) == 2:
        return (nc_str.format(nc[1], nc[0]),)
    return [nc_str.format(*i) for i in permutations(nc, len(nc))]
    if len(nc) == 2:
        return (eval(lambda_str.format(nc[1], nc[0])),)
    return [eval(lambda_str.format(*i)) for i in permutations(nc, len(nc))]



def gen_all_mapping_table(decryption):
    mapping_table = {'r': None, 'g': None, 'b': None, 'a': None}
    return {k: tuple(f"lambda a: a[..., [{', '.join(str(j) for j in i(0, 1, 2, 3))}]]" for i in v) for k, v in MappingFuncV2.encrypt.items() if v is not None}
    for i in combinations('rgba', 2):
        nc = ''.join(i)
        mapping_table[nc] = tuple(f"lambda a: a[..., [{i.replace('r', '0').replace('g', '1').replace('b', '2').replace('a', '3')}]]" for i in gen_mapping_table(nc, decryption))
    for i in combinations('rgba', 3):
        nc = ''.join(i)
        mapping_table[nc] = tuple(f"lambda a: a[..., [{i.replace('r', '0').replace('g', '1').replace('b', '2').replace('a', '3')}]]" for i in gen_mapping_table(nc, decryption))
    for i in combinations('rgba', 4):
        nc = ''.join(i)
        mapping_table[nc] = tuple(f"lambda a: a[..., [{i.replace('r', '0').replace('g', '1').replace('b', '2').replace('a', '3')}]]" for i in gen_mapping_table(nc, decryption))
    return mapping_table

print(str(gen_all_mapping_table(False)).replace("'", ''))
'''


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


weak_ref_cache: 'LRUCache[str, ReferenceType[PIL_Image.Image]]' = LRUCache(100)


def open_image(file: 'PathLike[str]', use_cache=True) -> tuple['PIL_Image.Image', Optional[str]]:
    """使用PIL打开图像, 并使用弱引用缓存

    Args:
        file (str): 要打开的文件
        use_cache (bool): 是否在弱引用中查找缓存(重载图像时请设为False)
    Returns:
        tuple[PIL.Image, Optional[str]]: 成功时, 返回(Image实例, None); 失败时, 返回(黑色Image实例, 错误提示)
    """
    if use_cache and file in weak_ref_cache:
        orig = weak_ref_cache[file]()
        if orig is not None:
            return orig, None
    try:
        image = PIL_Image.open(file).convert('RGBA')
    except FileNotFoundError:
        return BLACK_IMAGE, OIERR_NOT_EXIST
    except UnidentifiedImageError:
        return BLACK_IMAGE, OIERR_UNSUPPORTED_FORMAT.format(splitext(file)[1])
    except PIL_Image.DecompressionBombWarning:
        return BLACK_IMAGE, OIERR_EXCEED_LIMIT
    except OSError as e:
        # print_exc()
        return BLACK_IMAGE, OIERR_OS_ERROR.format(e.args[0] if e.strerror is None else e.strerror)
    except Exception as e:
        return BLACK_IMAGE, repr(e)
    weak_ref_cache.record(file, weak_ref(image))
    return image, None


def cal_best_scale(orig_width: int, orig_height: int, visible_width: int, visible_height: int) -> float:
    """
    :description: 根据两组宽高计算最佳大小
    :param orig_width: 原始图像宽度
    :param orig_height: 原始图像高度
    :param width: 可以使用的最大宽度
    :param height: 可以使用的最大高度
    :return: 宽高的最佳缩放比例
    """
    return min(visible_width / orig_width, visible_height / orig_height)


def cal_best_size(orig_width: int, orig_height: int, visible_width: int, visible_height: int) -> tuple[int, int]:
    """
    :description: 根据两组宽高计算最佳大小
    :param orig_width: 原始图像宽度
    :param orig_height: 原始图像高度
    :param width: 可以使用的最大宽度
    :param height: 可以使用的最大高度
    :return: 按比例缩放后的最佳大小
    """
    scale = min(visible_width / orig_width, visible_height / orig_height)
    return int(orig_width * scale), int(orig_height * scale)


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
        shape = array.shape
        size = (shape[1], shape[0])
    return PIL_Image.frombuffer('RGBA', size, array.data, "raw", 'RGBA', 0, 1)


def array_to_bitmap(array: 'ndarray', size: tuple = ...) -> 'Bitmap':
    if size is Ellipsis:
        shape = array.shape
        size = (shape[1], shape[0])
    return Bitmap.FromBufferRGBA(*size, array.data)


def buffer_to_bitmap(buffer, width: int, height: int) -> 'Bitmap':
    return Bitmap.FromBufferRGBA(width, height, buffer)


class WrappedImage(ABC):
    __slots__ = ()
    scalable: bool
    cacheable: bool = True

    def __init__(self, array: 'ndarray', size: tuple = ...) -> None:
        raise NotImplementedError()

    @property
    def wxBitmap(self) -> 'Bitmap':
        raise NotImplementedError()

    @property
    def size(self) -> tuple[int, int]:
        raise NotImplementedError()

    def gen_wxBitmap(self, visible_size: tuple[int, int], resampling_filter_id: int) -> 'Bitmap':
        raise NotImplementedError()

    def resize(self, visible_size: tuple[int, int], resampling_filter_id: int) -> None:
        raise NotImplementedError()

    def save(self, path: str, *args, **kwargs):
        raise NotImplementedError()


class PillowImage(WrappedImage):
    __slots__ = ('image', 'scalable')

    def __init__(self, array: 'ndarray', size: tuple = ..., scalable=True) -> None:
        self.scalable = scalable
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

    def gen_wxBitmap(self, visible_size: tuple[int, int], resampling_filter_id: int) -> 'Bitmap':
        size = cal_best_size(*self.size, *visible_size)
        match self.image.mode:
            case 'RGBA':
                return Bitmap.FromBufferRGBA(*size, self.image.resize(size, PIL_RESAMPLING_FILTERS[resampling_filter_id]).tobytes())
            case 'RGB':
                return Bitmap.FromBuffer(*size, self.image.resize(size, PIL_RESAMPLING_FILTERS[resampling_filter_id]).tobytes())

    def convert(self, mode: Optional[str] = ..., *args, **kwargs):
        self.image = self.image.convert(mode, *args, **kwargs)

    def resize(self, visible_size: tuple[int, int], resampling_filter_id: int):
        self.image = self.image.resize(cal_best_size(*self.size, *visible_size), PIL_RESAMPLING_FILTERS[resampling_filter_id])

    def save(self, path: str, *args, **kwargs):
        self.image.save(path, *args, **kwargs)


class WrappedPillowImage(PillowImage):
    __slots__ = ('cacheable',)

    def __init__(self, image: 'PIL_Image.Image', scalable=True, cacheable=True) -> None:
        self.image = image
        self.scalable = scalable
        self.cacheable = cacheable


class wxImage(WrappedImage):
    __slots__ = ('image',)
    scalable = True

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

    def resize(self, visible_size: tuple[int, int], resampling_filter_id: int):
        self.image.Rescale(*cal_best_size(*self.size, *visible_size), WX_RESAMPLING_FILTERS[resampling_filter_id])
        return self


class ImageData(WrappedImage):
    __slots__ = ('wxBitmap',)
    scalable = False
    wxBitmap: 'Bitmap'

    def __init__(self, data: Union['ndarray', 'Bitmap'], size: tuple = ...) -> None:
        if isinstance(data, Bitmap):
            self.wxBitmap = data
        else:
            self.wxBitmap = array_to_bitmap(data, size)
