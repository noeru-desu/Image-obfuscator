"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-11-21 07:18:01
"""
from collections import OrderedDict, deque
from collections.abc import Mapping
from heapq import nsmallest
from inspect import signature
from math import isqrt, sqrt
from os import walk
from os.path import normpath
from threading import Lock, Semaphore
from traceback import print_exc
from types import FunctionType
from typing import Callable, Generator, Hashable, Iterable, Any, Iterator, NoReturn, Optional, Union, TypeVar, Generic, overload

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


def walk_file(path, deep_walk=False, filter=None) -> tuple[int, list[tuple[list, list]]]:
    """
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param deep_walk: 是否遍历子目录
    :return: 返回(文件个数, [(文件所在的相对路径列表, 文件名列表)元组]列表)元组
    """
    result = []
    file_num = 0
    if filter is None:
        for r, fl in walk_file_generator(path, deep_walk):
            file_num += len(fl)
            result.append((r, fl))
    else:
        for r, fl in walk_file_generator(path, deep_walk):
            fl = [i for i in fl if i.split('.')[-1] in filter]
            file_num += len(fl)
            result.append((r, fl))
    return file_num, result


def walk_file_generator(path, deep_walk=False):
    """
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param deep_walk: 是否遍历子目录
    :return: 生成器返回(文件所在的相对路径, 文件名)元组
    """
    path = normpath(path)
    path_len = len(path) + 1
    if deep_walk:
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


def add_to(iter: Iterable[_T], lst: list[_T]):
    for i, v in enumerate(iter):
        lst[i] += v


def no_return_func(error) -> Callable[[Any], NoReturn]:
    def func(*_, **__) -> NoReturn:
        raise error
    return func


def get_factors(num: int, endpoints=True) -> Generator[int, None, None]:
    """获取`num`的因数

    Args:
        num (int): 非负整数
    Raises:
        ValueError: `num`为负数时抛出
    Returns:
        Generator
    """
    for i in range(1 if endpoints else 2, isqrt(num) + 1):
        if num % i:
            continue
        yield i
        j = num // i
        if j != i:
            yield j


def nclosest(iterable: Iterable, num: int, length=1) -> list[int]:
    """`iterable`中最接近于`num`的`length`个数字"""
    return nsmallest(length, iterable, key=lambda x: abs(x - num))


def cal_zoom_ratio(current_area: int, required_area: int) -> float:
    """计算长宽等比缩放率"""
    if current_area == required_area:
        return 1.0
    elif current_area < required_area:
        # x为缩放率, s为原始面积, sx^2 + 2sx - (required_area - s) = 0
        required_area -= current_area
        orig_area_x2 = current_area * 2
        delta = (orig_area_x2 * orig_area_x2) + (4 * current_area * required_area)
        return sqrt(delta) / orig_area_x2
    else:
        # x为缩放率, s为原始面积, sx^2 - required_area = 0
        delta = 4 * current_area * required_area
        return sqrt(delta) / (current_area * 2)


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


class Singleton(type):
    inst: 'Singleton'

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if not hasattr(self, 'inst'):
            self.inst = super().__call__(*args, **kwds)
        return self.inst


class LRUCacheRecord(object):
    __slots__ = ('_maxlen', 'dict')

    def __init__(self, maxlen=10) -> None:
        self._maxlen = maxlen
        self.dict: OrderedDict[Hashable, tuple[Callable, tuple, dict]] = OrderedDict()

    def __eq__(self, __o: object) -> bool:
        return self.dict.__eq__(__o)

    @property
    def maxlen(self) -> int:
        return self._maxlen

    @maxlen.setter
    def maxlen(self, v: int):
        self._maxlen = v
        if v != 0:
            length = len(self.dict)
            if length > v:
                for _ in range(length - v):
                    func, args, kwds = self.dict.popitem(False)[1]
                    try:
                        func(*args, **kwds)
                    except Exception:
                        print_exc()

    def record_cache(self, key: Hashable, deleter: Optional[Callable] = None, *args, **kwds):
        if key in self.dict:
            self.dict.move_to_end(key)
            if deleter is not None:
                self.dict[key] = (deleter, args, kwds)
            return
        assert deleter is not None, 'deleter cannot be NoneType when the cache_hash does not exist in the cache.'
        if self.maxlen != 0 and len(self.dict) >= self.maxlen:
            func, args, kwds = self.dict.popitem(False)[1]
            try:
                func(*args, **kwds)
            except Exception:
                print_exc()
        self.dict[key] = (deleter, args, kwds)

    def remove_cache_recode(self, key: Hashable, call_deleter=False, exist=False):
        if key not in self.dict:
            if exist:
                raise ValueError(f'no record of "{key}"')
            else:
                return
        if call_deleter:
            func, args, kwds = self.dict[key]
            try:
                func(*args, **kwds)
            except Exception:
                print_exc()
        del self.dict[key]


class LRUCache(Mapping[_KT, _VT], Generic[_KT, _VT]):
    __slots__ = ('_maxlen', 'dict')

    def __init__(self, maxlen=10) -> None:
        self._maxlen = maxlen
        self.dict: OrderedDict[_KT, _VT] = OrderedDict()

    def __eq__(self, __o: object) -> bool:
        return self.dict.__eq__(__o)

    def __getitem__(self, __key: _KT) -> _VT:
        if __key not in self.dict:
            raise KeyError(__key)
        return self.get(__key)

    def __setitem__(self, __key: _KT, __value: Any):
        self.record(__key, __value)

    def __delitem__(self, __key: _KT):
        self.remove(__key)

    def __len__(self) -> int:
        return self.dict.__len__()

    def __iter__(self) -> Iterator[_KT]:
        return self.dict.__iter__()

    @property
    def maxlen(self) -> int:
        return self._maxlen

    @maxlen.setter
    def maxlen(self, v: int):
        self._maxlen = v
        if v != 0:
            length = len(self.dict)
            if length > v:
                for _ in range(length - v):
                    self.dict.popitem(False)

    def clear(self):
        self.dict.clear()

    def reserve(self, length: int):
        if len(self.dict) <= abs(length):
            return
        if length > 0:
            for i in tuple(self.dict)[:-length]:
                del self.dict[i]
        elif length < 0:
            for i in tuple(self.dict)[-length:]:
                del self.dict[i]
        else:
            self.dict.clear()

    @overload
    def get(self, key: _KT) -> Optional[_VT]: ...

    @overload
    def get(self, key: _KT, default: _T) -> Union[_VT, _T]: ...

    def get(self, key: _KT, default: Optional[_T] = None) -> Union[_T, Optional[_VT]]:
        if key not in self.dict:
            return default
        value = self.dict[key]
        self.record(key)
        return value

    def record(self, key: _KT, value: Optional[_VT] = None):
        if key in self.dict:
            self.dict.move_to_end(key)
            if value is not None:
                self.dict[key] = value
            return
        assert value is not None, 'value cannot be NoneType when the cache_hash does not exist in the cache.'
        if self.maxlen != 0 and len(self.dict) >= self.maxlen:
            self.dict.popitem(False)
        self.dict[key] = value

    def remove(self, key: _KT, exist=False):
        if key not in self.dict:
            if exist:
                raise ValueError(f'no record of "{key}"')
            else:
                return
        del self.dict[key]
