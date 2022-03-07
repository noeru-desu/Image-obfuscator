"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-03-07 09:54:39
Description  : 一些小东西
"""
from os import walk
from os.path import normpath, split
from time import perf_counter_ns, perf_counter
from typing import Union, Callable
from threading import RLock
from functools import wraps as functools_wraps
from inspect import signature
from traceback import print_exc

from PIL import Image, UnidentifiedImageError

from image_encryptor.constants import OIERR_NOT_EXIST, OIERR_UNSUPPORTED_FORMAT, OIERR_EXCEED_LIMIT


def scale(image: 'Image', width: int, height: int):
    """
    :description: 指定宽或高，得到按比例缩放后的宽高
    :param image: PIL.Image.Image实例
    :param width: 可以使用的最大宽度
    :param height: 可以使用的最大高度
    :return: 按比例缩放后的宽和高(取最小)
    """
    _width, _height = image.size
    scale = min(width / _width, height / _height)
    return int(_width * scale), int(_height * scale)


def walk_file(path, topdown=False, filter=None) -> tuple[int, list[tuple[list, list]]]:
    """
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param topdown: 是否遍历子目录
    :return: 返回(文件个数, [(文件所在的相对路径列表, 文件名列表)元组]列表)元组
    """
    result = []
    file_num = 0
    if filter is None:
        for r, fl in walk_file_generator(path, topdown):
            file_num += len(fl)
            result.append((r, fl))
    else:
        for r, fl in walk_file_generator(path, topdown):
            fl = [i for i in fl if i.split('.')[-1] in filter]
            file_num += len(fl)
            result.append((r, fl))
    return file_num, result


def open_image(file) -> Union[tuple[str, str], tuple['Image.Image', None]]:
    """
    :description: 打开图片
    :param file: 要打开的文件
    :return: 成功时，返回(Image实例, None)元组
                失败时， 返回(文件名, 错误提示)元组
    """
    try:
        image = Image.open(file).convert('RGBA')
    except FileNotFoundError:
        return split(file)[1], OIERR_NOT_EXIST
    except UnidentifiedImageError:
        return split(file)[1], OIERR_UNSUPPORTED_FORMAT
    except Image.DecompressionBombWarning:
        return split(file)[1], OIERR_EXCEED_LIMIT
    except Exception as e:
        return split(file)[1], repr(e)
    return image, None


def walk_file_generator(path, topdown=False):
    """
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param topdown: 是否遍历子目录
    :return: 生成器返回(文件所在的相对路径, 文件名)元组
    """
    path = normpath(path)
    path_len = len(path) + 1
    if topdown:
        for top, dirs, files in walk(path):
            yield top[path_len:], files
    else:
        top, dirs, files = next(walk(path))
        yield '', files


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


def gen_slots_str(a_set):
    a_args_str = ('\000' * 4) + '__slots__ = ('
    b_args_str = ''
    start = True
    for i in a_set:
        if len(b_args_str) + len(i) > 118:
            a_args_str += '\n' + ('\000' * 8) + b_args_str + ','
            b_args_str = f"'{i}'"
            start = True
        elif start:
            start = False
            b_args_str += f"'{i}'"
        else:
            b_args_str += f", '{i}'"
    a_args_str += '\n' + ('\000' * 8) + b_args_str
    a_args_str += '\n' + ('\000' * 4) + ')'
    print(a_args_str)


timeit_targets = {}


def timeit(fn):
    def wrap(*args, **kwargs):
        if fn.__name__ not in timeit_targets:
            timeit_targets[fn.__name__] = {'running_time': 0}
            first = True
        else:
            first = False
        start = perf_counter_ns()
        result = fn(*args, **kwargs)
        running_time = perf_counter_ns() - start
        if first:
            timeit_targets[fn.__name__]['average_time'] = running_time
        else:
            timeit_targets[fn.__name__]['average_time'] = (running_time + timeit_targets[fn.__name__]['average_time']) / 2
        print(f'{fn.__name__}运行时间：{running_time}')
        timeit_targets[fn.__name__]['running_time'] += running_time
        print(f'{fn.__name__}总运行时间：{timeit_targets[fn.__name__]["running_time"]}')
        print(f'{fn.__name__}平均运行时间：{timeit_targets[fn.__name__]["average_time"]}')
        return result
    return wrap


def return_execution_time(fn):
    def wrap(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        running_time = perf_counter() - start
        return result, running_time
    return wrap


class FakeBar:
    """假的进度条"""
    value = 0

    @staticmethod
    def add(n):
        pass

    @staticmethod
    def finish():
        pass
