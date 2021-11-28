'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-11-27 18:51:33
Description  : 处理退出时的相关操作
'''
from atexit import register
from traceback import print_exc


class ExitProcessor(object):
    def __init__(self):
        register(self.exit)
        self.at_exit_func = []

    def register(self, func, *args, **kwargs):
        self.at_exit_func.append((func, args, kwargs))

    def exit(self):
        for func, args, kwargs in self.at_exit_func:
            try:
                func(*args, *kwargs)
            except Exception:
                print_exc()
                pass
