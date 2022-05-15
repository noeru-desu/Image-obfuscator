"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-05-15 10:30:11
Description  : 一些小东西
"""
from collections import deque
from inspect import signature
from os import walk
from os.path import normpath
from threading import Lock, Semaphore
from types import FunctionType
from typing import Iterable, Any, Iterator, Union


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


class SingleTaskDeque(object):
    __slots__ = ('_task', '_lock', '_internal_lock', '_blocking')

    def __init__(self, item: Any = None, blocking=True) -> None:
        self._internal_lock = Lock()
        self._lock = Lock() if blocking else None
        self._blocking = blocking
        self._task = item
        if blocking:
            self._lock.acquire()

    def __iter__(self) -> Iterator:
        return ().__iter__() if self._task is None else (self._task,).__iter__()

    def spare(self):
        return self._task is None

    def empty(self):
        return self._task is None

    def full(self):
        return self._task is not None

    def put(self, item, left=False):
        with self._internal_lock:
            self._task = item
            if self._blocking and self._lock.locked():
                self._lock.release()

    def get(self, blocking: bool = True, timeout: float = -1):
        with self._internal_lock:
            if self._blocking:
                self._lock.acquire(blocking, timeout)
            task = self._task
            self._task = None
            return task

    def clear(self):
        with self._internal_lock:
            self.task = None
            if self._blocking and not self._lock.locked():
                self._lock.acquire()


class Deque(object):
    __slots__ = ('_deque', '_lock', '_semaphore', '_blocking')

    def __new__(cls: type['Deque'], item: Any = None, maxlen: int = None, blocking=True) -> Union['Deque', SingleTaskDeque]:
        return SingleTaskDeque(item, blocking) if maxlen == 1 else super().__new__(cls)

    def __init__(self, iterable: Iterable = (), maxlen: int = None, blocking=True):
        self._deque = deque(iterable, maxlen)
        self._lock = Lock()
        self._semaphore = Semaphore(len(iterable)) if blocking else None
        self._blocking = blocking

    def __iter__(self) -> Iterator:
        return self._deque.__iter__()

    def spare(self):
        return self._deque.maxlen is None or (len(self._deque) < self._deque.maxlen)

    def empty(self):
        return len(self._deque) == 0

    def full(self):
        return self._deque.maxlen is not None and len(self._deque) == self._deque.maxlen

    def put(self, item, left=False):
        with self._lock:
            is_full = self.full()
            self._deque.appendleft(item) if left else self._deque.append(item)
            if self._blocking and not is_full:
                self._semaphore.release()

    def get(self, blocking: bool = True, timeout: float = None, from_right=False):
        with self._lock:
            if self._blocking:
                self._semaphore.acquire(blocking, timeout)
            return self._deque.pop() if from_right else self._deque.popleft()

    def clear(self):
        with self._lock:
            self._deque.clear()
            if self._blocking:
                self._semaphore = Semaphore(0)
