"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-02-15 09:17:35
Description  : 一些小东西
"""
from threading import RLock
from functools import wraps as functools_wraps
from inspect import signature
from traceback import print_exc
from typing import TYPE_CHECKING, Callable

from image_encryptor.utils.utils import walk_file as wf

if TYPE_CHECKING:
    from PIL.Image import Image


def scale(image: 'Image', width: int, height: int):
    """
    :description: 指定宽或高，得到按比例缩放后的宽高
    :param image: PIL.Image.Image实例
    :param width: 可以使用的最大宽度
    :param height: 可以使用的最大高度
    :return: 按比例缩放后的宽和高(取最小)
    """
    _width, _height = image.size
    width /= _width
    height /= _height
    scale = width if width < height else height
    return int(_width * scale), int(_height * scale)


def walk_file(path, topdown=False, filter=None) -> tuple[int, list[tuple[list, list]]]:
    '''
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param topdown: 是否遍历子目录
    :return: 返回(文件个数, [(文件所在的相对路径列表, 文件名列表)元组]列表)元组
    '''
    result = []
    file_num = 0
    if filter is None:
        for r, fl in wf(path, topdown):
            file_num += len(fl)
            result.append((r, fl))
    else:
        for r, fl in wf(path, topdown):
            fl = [i for i in fl if i.split('.')[-1] in filter]
            file_num += len(fl)
            result.append((r, fl))
    return file_num, result


def copy_signature(target: Callable, origin: Callable) -> Callable:
    """
    Copy the function signature of origin into target
    """
    # https://stackoverflow.com/questions/39926567/python-create-decorator-preserving-function-arguments
    target.__signature__ = signature(origin)
    return target


lock = RLock()


def in_try(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            with lock:
                print_exc()
        copy_signature(wrap, func)
        wrap.original = func
    return wrap
