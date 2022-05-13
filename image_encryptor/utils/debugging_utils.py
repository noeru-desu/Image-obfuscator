"""
Author       : noeru_desu
Date         : 2022-03-27 08:07:12
LastEditors  : noeru_desu
LastEditTime : 2022-05-12 06:21:05
Description  : 调试函数
"""
from functools import wraps as functools_wraps
from threading import RLock
from time import perf_counter, perf_counter_ns
from traceback import print_exc
from typing import Iterable, Type
from types import FunctionType

from image_encryptor.utils.misc_utils import copy_signature, isclassmethod

lock = RLock()


def gen_parameter_str(args: tuple = None, kwargs: dict = None) -> str:
    return f"""{', '.join(str(i) for i in args) if args else ''}{'' if not args or not kwargs else ', '}{', '.join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ''}"""


def in_try(error_type: Iterable[Type[BaseException]] = (Exception,)):
    def wrapper(func):
        @functools_wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                if not isinstance(e, error_type):
                    raise e from e
                with lock:
                    print_exc()
                    print(f'Function arguments: {func.__qualname__}({gen_parameter_str(args, kwargs)})')
        copy_signature(wrap, func)
        return wrap
    if not isinstance(error_type, Iterable):
        func = error_type
        error_type = (Exception,)
        return wrapper(func)
    return wrapper


def print_result(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'{func.__qualname__}: {result}')
        return result
    copy_signature(wrap, func)
    return wrap


def gen_slots_str(a_set):
    a_set = sorted(a_set)
    a_args_str = ('\000' * 4) + '__slots__ = ('
    b_args_str = ''
    start = True
    for i in a_set:
        if len(b_args_str) + len(i) > 118:
            a_args_str += '\n' + ('\000' * 8) + b_args_str + ','
            b_args_str = f"'{i}'"
        elif start:
            start = False
            b_args_str += f"'{i}'"
        else:
            b_args_str += f", '{i}'"
    a_args_str += '\n' + ('\000' * 8) + b_args_str
    a_args_str += '\n' + ('\000' * 4) + ')'
    print(a_args_str)


class Timeit(object):
    __slots__ = ('func', 'func_name', 'total_running_time', 'average_time', 'running_times', 'bound', 'default_args', 'repeat_times', 'prompt')

    def __init__(self, *default_args, repeat_times: int = 1, prompt: bool = True) -> None:
        assert repeat_times > 0, '"repeat_times" must be greater than 0.'
        self.default_args = default_args
        self.repeat_times = repeat_times
        self.prompt = prompt
        self.total_running_time = 0
        self.running_times = 0
        self.average_time = ...
        self.bound = False

    def __call__(self, func: FunctionType):
        assert not self.bound, 'Do not reuse Timeit instances.'
        self.bound = True
        func_name = repr(func)
        if self.prompt and self.repeat_times > 1 and isclassmethod(func):
            if not input(f'待循环计时的对象{func_name}为类方法, 是否确定? (y/n)') == 'y':
                self.repeat_times = 1
        @functools_wraps(func)
        def wrap(*args, **kwargs):
            for i in range(1, self.repeat_times + 1):
                start = perf_counter_ns()
                result = func(*self.default_args, *args, **kwargs)
                running_time = perf_counter_ns() - start
                self.total_running_time += running_time
                self.running_times += 1
                if self.average_time is Ellipsis:
                    self.average_time = running_time
                else:
                    self.average_time = self.total_running_time / self.running_times
                if self.repeat_times != 1:
                    print(f'{func_name}本次循环计时第{i}次运行时间：{running_time} ns')
            if self.repeat_times == 1:
                print(f'{func_name}本次运行时间：{running_time} ns')
            print(f'{func_name}总运行时间：{self.total_running_time} ns')
            print(f'{func_name}平均运行时间：{self.average_time} ns')
            return result
        copy_signature(wrap, func)
        return wrap


def return_execution_time(fn):
    def wrap(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        running_time = perf_counter() - start
        return result, running_time
    return wrap
