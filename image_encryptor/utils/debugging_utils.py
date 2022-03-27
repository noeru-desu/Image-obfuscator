"""
Author       : noeru_desu
Date         : 2022-03-27 08:07:12
LastEditors  : noeru_desu
LastEditTime : 2022-03-27 08:34:57
Description  : 调试函数
"""
from functools import wraps as functools_wraps
from threading import RLock
from time import perf_counter, perf_counter_ns
from traceback import print_exc

from image_encryptor.utils.misc_utils import copy_signature

lock = RLock()


def in_try(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        copy_signature(wrap, func)
        try:
            return func(*args, **kwargs)
        except Exception:
            with lock:
                print_exc()
    return wrap


def print_result(func):
    @functools_wraps(func)
    def wrap(*args, **kwargs):
        copy_signature(wrap, func)
        result = func(*args, **kwargs)
        print(f'{func.__name__}: {result}')
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
        print(f'{fn.__name__}运行时间：{running_time} ns')
        timeit_targets[fn.__name__]['running_time'] += running_time
        print(f'{fn.__name__}总运行时间：{timeit_targets[fn.__name__]["running_time"]} ns')
        print(f'{fn.__name__}平均运行时间：{timeit_targets[fn.__name__]["average_time"]} ns')
        return result
    return wrap


def return_execution_time(fn):
    def wrap(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        running_time = perf_counter() - start
        return result, running_time
    return wrap
