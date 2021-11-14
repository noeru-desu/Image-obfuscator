'''
Author       : noeru_desu
Date         : 2021-11-14 08:27:48
LastEditors  : noeru_desu
LastEditTime : 2021-11-14 08:45:34
Description  : 一些小功能
'''
from typing import Callable, Iterable, Optional


class SegmentTrigger(object):
    def __init__(self, callbacks: Iterable, initcall: Optional[Callable] = None, *args, **kwargs):
        self._callbacks = callbacks
        self._initcall = initcall
        self._args = args
        self._kwargs = kwargs
        self._max_num = len(callbacks)
        self._num = -1

    @property
    def call(self) -> Callable:
        if self._num >= self._max_num:
            self.init()
        self._num += 1
        return self._callbacks[self._num]

    def init(self):
        self._num = -1
        if self._initcall is not None:
            self._initcall(*self._args, **self._kwargs)
