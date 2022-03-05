"""
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2022-03-05 07:38:33
Description  : 一些小东西
"""
from os import walk
from os.path import normpath, split
from time import perf_counter_ns, perf_counter
from typing import Union

from PIL import Image, UnidentifiedImageError

from image_encryptor.constants import OIERR_NOT_EXIST, OIERR_UNSUPPORTED_FORMAT, OIERR_EXCEED_LIMIT


def walk_file(path, topdown=False):
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


def calculate_formula_string(formula_string: str, **format):
    """
    :description: 将字符串转换为公式后运算
    :param formula_string: 需要格式化的字符串
    :param format: 格式化时需要的变量
    :return: (运算结果, 错误提示)元组
    """
    try:
        result = int(eval(formula_string.format(**format)))
    except SyntaxError:
        return None, '输入的公式有误，请确保输入了正确的运算符'
    except NameError:
        return None, '输入内容不为 纯数字/运算符/变量'
    except KeyError as e:
        return None, f'未知的变量：{str(e)}。当前提供：{", ".join(format.keys())}'
    except Exception as e:
        return None, f'运算输入的公式时出现错误：{repr(e)}'
    else:
        return result, None


timeit_targets = {}


def timeit(fn):
    def wrap(*args, **kwargs):
        if fn.__name__ not in timeit_targets:
            timeit_targets[fn.__name__] = 0
        start = perf_counter_ns()
        result = fn(*args, **kwargs)
        running_time = perf_counter_ns() - start
        print(f'{fn.__name__}运行时间：{running_time}')
        timeit_targets[fn.__name__] += running_time
        print(f'{fn.__name__}总运行时间：{timeit_targets[fn.__name__]}')
        return result
    return wrap


def return_execution_time(fn):
    def wrap(*args, **kwargs):
        start = perf_counter()
        result = fn(*args, **kwargs)
        running_time = perf_counter() - start
        return result, running_time
    return wrap


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


class FakeBar:
    """假的进度条"""
    value = 0

    @staticmethod
    def update(n):
        pass

    @staticmethod
    def finish():
        pass
