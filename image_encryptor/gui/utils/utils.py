'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-11-12 17:24:59
Description  : 一些小东西
'''
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, CancelledError
from traceback import print_exc
from typing import TYPE_CHECKING

from image_encryptor.common.utils.utils import walk_file as wf

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Gauge


class ProgressBar(object):
    def __init__(self, target: 'Gauge', step_count: int):
        self.target = target
        self.step_count = step_count
        self.step = -1
        self.value = 0
        self.finished_step = True
        self.max_value = 0
        self.step_progress = 0
        self.next_step_progress = 0
        self.target.SetValue(0)

    def next_step(self, max_value: int):
        if not self.finished_step:
            self.finish()
        self.finished_step = False
        self.step += 1
        self.max_value = max_value
        self.max = self.max_value * self.step_count
        self.value = 0
        self.step_progress = 0 if self.next_step_progress == 0 else self.next_step_progress
        self.next_step_progress = (self.step + 1) / self.step_count * 100 if self.step < self.step_count else 100

    def update(self, value):
        if value > self.max_value:
            return
        self.value = value
        self.target.SetValue(int(self.step_progress + value / self.max * 100))

    def finish(self):
        self.target.SetValue(int(self.next_step_progress))
        self.finished_step = True

    def over(self):
        if not self.finished_step:
            self.finish()
        self.target.SetValue(100)


class ThreadTaskManager(ThreadPoolExecutor):
    def __init__(self, max_workers: int = ..., *args, **kwargs):
        if 'thread_name_prefix' not in kwargs:
            kwargs['thread_name_prefix'] = 'worker_thread'
        super().__init__(max_workers, *args, **kwargs)
        self.task_dict = {}

    def create_tag(self, tag_name: str, single: bool, overwrite: bool = True):
        self.task_dict[tag_name] = {
            'single': single,
            'overwrite': overwrite,
            'futures': None if single else []
        }

    def add_task(self, tag_name, future, callback=None, *callback_args, **callback_kwargs):
        if callback is not None:
            future.add_done_callback(lambda future: self.callback(tag_name, future, callback, *callback_args, **callback_kwargs))
        if self.task_dict[tag_name]['single']:
            self.task_dict[tag_name]['futures'] = future
        else:
            self.task_dict[tag_name]['futures'].append(future)

    def callback(self, tag_name, future, callback=None, *callback_args, **callback_kwargs):
        try:
            future.result()
        except CancelledError:
            pass
        if callback is not None:
            try:
                callback(future, tag_name, *callback_args, **callback_kwargs)
            except Exception:
                print_exc()
        self.del_future(tag_name, future)

    def cancel_task(self, tag_name=None, future=None):
        if future is not None:
            if future.running():
                return False
            if not future.done():
                return future.cancel()
        elif tag_name is None:
            return True

        if self.task_dict[tag_name]['futures'] is not None:
            if self.task_dict[tag_name]['single']:
                if self.task_dict[tag_name]['futures'].running():
                    return False
                if not self.task_dict[tag_name]['futures'].done():
                    return self.task_dict[tag_name]['futures'].cancel()
            else:
                all_cancelled = True
                for i in self.task_dict[tag_name]['futures']:
                    if i.done():
                        continue
                    if i.running():
                        all_cancelled = False
                        continue
                    if not i.cancel():
                        all_cancelled = False
                return all_cancelled

        return True

    def check_tag(self, tag_name):
        if self.task_dict[tag_name]['overwrite']:
            if self.cancel_task(tag_name):
                return None
            else:
                if self.task_dict[tag_name]['single']:
                    return '已有一个无法打断的任务正在进行'
                else:
                    return '任务列表没有被完全取消'
        else:
            return '已有一个任务正在进行'

    def del_future(self, tag_name, futures=None):
        if not (futures is None or self.task_dict[tag_name]['single']):
            self.task_dict[tag_name]['futures'].remove(futures)
        else:
            self.task_dict[tag_name]['futures'] = None


class ProcessTaskManager(ProcessPoolExecutor):
    def __init__(self, max_workers: int = ..., *args, **kwargs):
        super().__init__(max_workers, *args, **kwargs)
        self.watchdog = ThreadTaskManager(max_workers, thread_name_prefix='process_pool_watchdog')
        self.task_dict = {}

    def create_tag(self, tag_name: str, single: bool, overwrite: bool = True):
        self.watchdog.create_tag(tag_name, single, overwrite)
        self.task_dict[tag_name] = {
            'single': single,
            'overwrite': overwrite,
            'futures': None if single else []
        }

    def add_task(self, tag_name, future, callback=None, *callback_args, **callback_kwargs):
        if self.task_dict[tag_name]['single']:
            self.task_dict[tag_name]['futures'] = future
        else:
            self.task_dict[tag_name]['futures'].append(future)
        self.watchdog.add_task(tag_name, self.watchdog.submit(self.callback, tag_name, future, callback, *callback_args, **callback_kwargs))

    def callback(self, watchdog_future, tag_name, future, callback=None, *callback_args, **callback_kwargs):
        print(1)
        try:
            future.result()
        except CancelledError:
            pass
        print(2)
        if callback is not None:
            try:
                callback(future, tag_name, *callback_args, **callback_kwargs)
            except Exception:
                print_exc()
        self.watchdog.del_future(tag_name, watchdog_future)

    def cancel_task(self, tag_name=None, future=None):
        if future is not None:
            if future.running():
                return False
            if not future.done():
                if future.cancel():
                    self.watchdog.cancel_task(tag_name, future)
                    return True
                else:
                    return False
        elif tag_name is None:
            return True

        if self.task_dict[tag_name]['futures'] is not None:
            if self.task_dict[tag_name]['single']:
                if self.task_dict[tag_name]['futures'].running():
                    return False
                if not self.task_dict[tag_name]['futures'].done():
                    if self.task_dict[tag_name]['futures'].cancel():
                        self.watchdog.cancel_task(tag_name)
                        return True
                    else:
                        return False
            else:
                all_cancelled = True
                for i in self.task_dict[tag_name]['futures']:
                    if i.done():
                        continue
                    if i.running():
                        all_cancelled = False
                        continue
                    if not i.cancel():
                        all_cancelled = False
                    else:
                        self.watchdog.cancel_task(tag_name, i)
                return all_cancelled

        return True

    def check_tag(self, tag_name):
        if self.task_dict[tag_name]['overwrite']:
            if self.cancel_task(tag_name):
                return None
            else:
                if self.task_dict[tag_name]['single']:
                    return '已有一个无法打断的任务正在进行'
                else:
                    return '任务列表没有被完全取消'
        else:
            return '已有一个任务正在进行'

    def del_future(self, tag_name, futures=None):
        if not (futures is None or self.task_dict[tag_name]['single']):
            self.task_dict[tag_name]['futures'].remove(futures)
        else:
            self.task_dict[tag_name]['futures'] = None


def scale(image: 'Image', width: int, height: int):
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


def walk_file(path, topdown=False) -> tuple[int, list[tuple[list, list]]]:
    '''
    :description: 获取目录下的所有文件
    :param path: 需要遍历的文件夹
    :param topdown: 是否遍历子目录
    :return: 返回(文件个数, [(文件所在的相对路径列表, 文件名列表)元组]列表)元组
    '''
    result = []
    file_num = 0
    for r, fl in wf(path, topdown):
        file_num += len(fl)
        result.append((r, fl))
    return file_num, result
