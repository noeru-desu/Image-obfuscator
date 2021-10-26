'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-25 21:24:37
Description  : 一些小东西
'''
from concurrent.futures import ThreadPoolExecutor

from PIL import Image


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
