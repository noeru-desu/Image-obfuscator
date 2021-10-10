'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-10 11:43:19
Description  : 一些小东西
'''
from os import system, walk
from os.path import normpath, split

from PIL import Image, UnidentifiedImageError


class fake_bar(object):
    value = 0

    def update(self, n):
        pass

    def finish(self):
        pass


def pause():
    system('pause>nul')


def walk_file(path, topdown=False):
    path = normpath(path)
    path_len = len(path) + 1
    for top, dirs, files in walk(path, topdown):
        yield top[path_len:], files


def calculate_formula_string(formula_string: str, **format):
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


def open_image(file):
    try:
        image = Image.open(file).convert('RGBA')
    except FileNotFoundError:
        return split(file)[1], '文件不存在'
    except UnidentifiedImageError:
        return split(file)[1], '无法打开或识别图像格式，或输入了不受支持的格式'
    except Image.DecompressionBombWarning:
        return split(file)[1], '图片像素量过多，为防止被解压炸弹DOS攻击，自动跳过'
    except Exception as e:
        return split(file)[1], repr(e)
    return image, None
