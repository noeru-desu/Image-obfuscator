"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-03-27 08:27:31
Description  : 一些小东西
"""
from functools import wraps as functools_wraps
from inspect import signature
from os import walk
from os.path import normpath
from traceback import format_exc
from typing import Callable


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


def catch_exception_and_return(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        copy_signature(wrap, func)
        try:
            return func(*args, **kwargs), None
        except Exception:
            return None, format_exc()
    return wrap


class FakeBar:
    """假的进度条"""
    value = 0

    @staticmethod
    def add():
        pass

    @staticmethod
    def finish():
        pass
