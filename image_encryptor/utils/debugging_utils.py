"""
Author       : noeru_desu
Date         : 2022-03-27 08:07:12
LastEditors  : noeru_desu
LastEditTime : 2022-04-03 09:40:01
Description  : 调试函数
"""
from functools import wraps as functools_wraps
from threading import RLock
from time import perf_counter, perf_counter_ns
from traceback import print_exc

from image_encryptor.utils.misc_utils import copy_signature

lock = RLock()


def gen_parameter_str(args: tuple = None, kwargs: dict = None) -> str:
    delimiter = '' if args is None or kwargs is None else ', '
    return f'{"" if args is None else ", ".join(str(i) for i in args)}{delimiter}{"" if kwargs is None else ", ".join(f"{k}={v}" for k, v in kwargs.items())}'


def in_try(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        copy_signature(wrap, func)
        try:
            return func(*args, **kwargs)
        except Exception:
            with lock:
                print_exc()
                print(f'Function arguments when caught: {func.__qualname__}({gen_parameter_str(args, kwargs)})')
    return wrap


def print_result(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        copy_signature(wrap, func)
        result = func(*args, **kwargs)
        print(f'{func.__qualname__}: {result}')
        return result
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


class Timeit(object):
    """使用时请实例化"""
    __slots__ = ('func', 'func_name', 'total_running_time', 'average_time', 'running_times', 'bound', 'default_parameters')

    def __init__(self, *default_parameters) -> None:
        self.default_parameters = default_parameters
        self.total_running_time = 0
        self.running_times = 0
        self.average_time = ...
        self.bound = False

    def __call__(self, func):
        assert not self.bound, 'Do not reuse Timeit instances.'
        self.bound = True
        func_name = f'[{id(func)}]{func.__qualname__}'
        def wapper(*args, **kwargs):
            start = perf_counter_ns()
            result = func(*self.default_parameters, *args, **kwargs)
            running_time = perf_counter_ns() - start
            self.total_running_time += running_time
            self.running_times += 1
            if self.average_time is Ellipsis:
                self.average_time = running_time
            else:
                self.average_time = self.total_running_time / self.running_times
            print(f'{func_name}本次运行时间：{running_time} ns')
            print(f'{func_name}总运行时间：{self.total_running_time} ns')
            print(f'{func_name}平均运行时间：{self.average_time} ns')
            return result
        return wapper


def return_execution_time(fn):
    def wrap(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        running_time = perf_counter() - start
        return result, running_time
    return wrap
