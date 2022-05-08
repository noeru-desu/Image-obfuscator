"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-05-08 15:20:40
Description  : 一些小东西
"""
from inspect import signature
from os import walk
from os.path import normpath
from types import FunctionType
from typing import Iterable, Any


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


def copy_signature(target: FunctionType, origin: FunctionType) -> FunctionType:
    """
    Copy the function signature of origin into target
    """
    # https://stackoverflow.com/questions/39926567/python-create-decorator-preserving-function-arguments
    target.__signature__ = signature(origin)
    return target


def anadiplosis(iterable: Iterable, start: Any = ..., end: Any = ...):
    if start is Ellipsis:
        previous = iterable[0]
        for i in iterable[1:]:
            yield previous, i
            previous = i
    else:
        previous = start
        for i in iterable:
            yield previous, i
            previous = i
    if end is not Ellipsis:
        yield previous, end


def isclassmethod(func: FunctionType) -> bool:
    """通过比较`func`参数的
        `__qualname__`与`__name__`属性是否一致\n
        接受的参数名中是否存在名为`self`的参数
    来尝试判断`func`是否是一个类方法(满足其中一个条件)
    注意: 已实例化的类中的方法可直接使用`isinstance(func, MethodType)`或`inspect.ismethod(func)`进行准确的判断

    Args:
        func (FunctionType)
    """
    return func.__qualname__ != func.__name__ or 'self' in signature(func).parameters


class FakeBar:
    """假的进度条"""
    value = 0

    @staticmethod
    def add():
        pass

    @staticmethod
    def finish():
        pass
