"""
Author       : noeru_desu
Date         : 2022-11-26 09:14:39
LastEditors  : noeru_desu
LastEditTime : 2022-11-26 16:21:32
"""
from atexit import register
from os import makedirs, remove, listdir
from os.path import join, getmtime, exists, getsize, split, isfile, splitext
from typing import TYPE_CHECKING, Literal, Optional, Union
from math import ceil
from zlib import compress as zlib_compress, decompress as zlib_decompress
from bz2 import compress as bz2_compress, decompress as bz2_decompress
from lzma import compress as lzma_compress, decompress as lzma_decompress

from orjson import dumps

from image_obfuscator.constants import LOCAL_APPDATA_TEMP
from image_obfuscator.modes.lsb_steganography.constants import LSB_INFO_VERSION

if TYPE_CHECKING:
    from os import PathLike
    from PIL.Image import Image


class CompressedFile(object):
    __slots__ = (
        'compressed_file', 'compressor', 'level', 'compressed_file_size',
        'orig_size', 'compression_ratio', 'compression_percentage'
    )

    def __init__(self, compressed_file: 'PathLike', orig_size: int, compressor, level) -> None:
        self.compressed_file = compressed_file
        self.compressor = compressor
        self.level = level
        self.compressed_file_size = getsize(compressed_file)
        self.orig_size = orig_size
        self.compression_ratio: float = self.compressed_file_size / orig_size
        self.compression_percentage = f'{round(self.compression_ratio * 100, 2)}%'

    def load_compressed_data(self):
        with open(self.compressed_file, 'rb') as f:
            return f.read()


class CompressedFileManager(object):
    __slots__ = ('cache',)
    temp_dir = join(LOCAL_APPDATA_TEMP, 'compressed_files')

    def __init__(self) -> None:
        if not exists(self.temp_dir):
            makedirs(self.temp_dir)
        else:
            for i in listdir(self.temp_dir):
                remove(i)
        self.cache: dict[str, CompressedFile] = {}
        register(self.clear_cache)

    def get_size(self, file: 'PathLike', use_compressed_file_cache=True) -> int:
        if use_compressed_file_cache:
            cache = self.cache.get(self.gen_cache_file_name(file))
            if cache is not None:
                return cache.compressed_file_size
        return getsize(file)

    def open_file(self, file: 'PathLike', use_compressed_file_cache=True) -> Union[bytes, CompressedFile]:
        if use_compressed_file_cache:
            cache = self.cache.get(self.gen_cache_file_name(file))
            if cache is not None:
                return cache
        with open(file, 'rb') as f:
            return f.read()

    def get_compressed_file(self, file: 'PathLike') -> Optional[CompressedFile]:
        if not isfile(file):
            return None
        return self.cache.get(self.gen_cache_file_name(file))

    def del_compressed_data(self, file: 'PathLike'):
        if not isfile(file):
            return
        name = self.gen_cache_file_name(file)
        if name not in self.cache:
            return
        cache = self.cache.pop(name)
        remove(cache.compressed_file)

    def recompress_data(self, file: 'PathLike', compressor: Literal['zlib', 'bz2', 'lzma'], compresslevel=6) -> Optional[CompressedFile]:
        if not isfile(file):
            return
        name = self.gen_cache_file_name(file)
        if name not in self.cache:
            return
        cache = self.cache.pop(name)
        remove(cache.compressed_file)
        return self.compress_file(file, compressor, compresslevel)

    def cache_compressed_data(self, file: 'PathLike', data: bytes, compressor, compresslevel) -> CompressedFile:
        name = self.gen_cache_file_name(file)
        cache_file = join(self.temp_dir, name)
        with open(cache_file, 'wb') as f:
            f.write(data)
        cache = self.cache[name] = CompressedFile(cache_file, getsize(file), compressor, compresslevel)
        return cache

    def clear_cache(self):
        for i in self.cache.values():
            remove(i.compressed_file)
        self.cache.clear()

    @staticmethod
    def gen_cache_file_name(file: 'PathLike'):
        return f'{split(file)[1]}{getmtime(file)}'

    def compress_file(self, file: 'PathLike', compressor: Literal['zlib', 'bz2', 'lzma'], compresslevel=6) -> Optional[CompressedFile]:
        if not isfile(file):
            return None
        with open(file, 'rb') as f:
            match compressor:
                case 'zlib':
                    data = zlib_compress(f.read(), level=compresslevel)
                case 'bz2':
                    data = bz2_compress(f.read(), compresslevel)
                case 'lzma':
                    data = lzma_compress(f.read(), preset=compresslevel)
        return self.cache_compressed_data(file, data, compressor, compresslevel)

    def decompress_data(self, data: bytes, compressor: Literal['zlib', 'bz2', 'lzma']) -> bytes:
        match compressor:
            case 'zlib':
                return zlib_decompress(data)
            case 'bz2':
                return bz2_decompress(data)
            case 'lzma':
                return lzma_decompress(data)


def gen_lsb_info_json(compressor: str, file: str) -> bytes:
    return dumps({
        'CA': compressor,
        'FS': splitext(file)[1].lstrip('.'),
        'V': LSB_INFO_VERSION
    })


def cal_estimated_size(image: 'Image', lsb_ratio) -> tuple[int, int]:
    w, h = image.size
    return ceil(w * lsb_ratio), ceil(h * lsb_ratio)
