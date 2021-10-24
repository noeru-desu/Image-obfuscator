'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-24 19:00:14
Description  : 一些小东西
'''
from os import system, walk
from concurrent.futures import ThreadPoolExecutor
from os.path import normpath, split

from PIL import Image, UnidentifiedImageError


class ProgressBar(object):
    def __init__(self, target, max_value: int):
        self.target = target
        self.max_value = max_value
        self.value = 0

    def update(self, value):
        self.value = value
        self.target.SetValue(int((value / self.max_value) * 100))

    def finish(self):
        self.target.SetValue(100)


class TaskManager(ThreadPoolExecutor):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.task_dict = {}

    def create_tag(self, tag_name: str, single: bool, overwrite: bool = True):
        self.task_dict[tag_name] = {
            'single': single,
            'overwrite': overwrite,
            'futures': None if single else []
        }

    def add_task(self, tag_name, future, callback=None):
        if callback is not None:
            future.add_done_callback(callback)
        if self.task_dict[tag_name]['single']:
            self.task_dict[tag_name]['futures'] = future
        else:
            self.task_dict[tag_name]['futures'].append(future)

    def check_tag(self, tag_name):
        if self.task_dict[tag_name]['single'] and self.task_dict[tag_name]['futures'] is not None:
            if self.task_dict[tag_name]['overwrite']:
                if self.task_dict[tag_name]['futures'].running():
                    return '已有一个无法打断的任务正在进行'
                else:
                    if not self.task_dict[tag_name]['futures'].cancelled():
                        self.task_dict[tag_name]['futures'].cancel()
                    return None
            else:
                return '已有一个任务正在进行'
        return None

    def del_future(self, tag_name, futures=None):
        if not (futures is None or self.task_dict[tag_name]['single']):
            self.task_dict[tag_name]['futures'].remove(futures)
        else:
            self.task_dict[tag_name]['futures'] = None


def pause():
    """输入cmd命令以暂停"""
    system('pause>nul')


def walk_file(path, topdown=False):
    '''
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param topdown: 是否遍历子目录
    :return: 生成器返回(文件所在的相对路径, 文件名)元组
    '''
    path = normpath(path)
    path_len = len(path) + 1
    for top, dirs, files in walk(path, topdown):
        yield top[path_len:], files


def calculate_formula_string(formula_string: str, **format):
    '''
    :description: 将字符串转换为公式后运算
    :param formula_string: 需要格式化的字符串
    :param format: 格式化时需要的变量
    :return: (运算结果, 错误提示)元组
    '''
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
    '''
    :description: 打开图片
    :param file: 要打开的文件
    :return: 成功时，返回(Image实例, None)元组
                失败时， 返回(文件名, 错误提示)元组
    '''
    try:
        image = Image.open(file).convert('RGBA')
    except FileNotFoundError:
        return split(file)[1], '文件不存在'
    except UnidentifiedImageError:
        return split(file)[1], '无法打开或识别图像格式，或输入了不受支持的格式'
    except Image.DecompressionBombWarning:
        return split(file)[1], '图片像素量超过允许最大像素量'
    except Exception as e:
        return split(file)[1], repr(e)
    return image, None


def scale(image: Image.Image, width: int, height: int):
    """
    :description: 指定宽或高，得到按比例缩放后的宽高
    :param image: PIL.Image.Image实例
    :param width: 可以使用的最大宽度
    :param height: 可以使用的最大高度
    :return: 按比例缩放后的宽和高(取最小)
    """
    _width, _height = image.size
    width /= _width
    height /= _height
    scale = width if width < height else height
    return int(_width * scale), int(_height * scale)
