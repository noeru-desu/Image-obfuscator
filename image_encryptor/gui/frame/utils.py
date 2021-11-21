'''
Author       : noeru_desu
Date         : 2021-11-14 08:27:48
LastEditors  : noeru_desu
LastEditTime : 2021-11-20 21:17:39
Description  : 一些小功能
'''
from typing import TYPE_CHECKING, Callable, Iterable, Optional

if TYPE_CHECKING:
    from wx import Gauge


class ProgressBar(object):
    def __init__(self, target: 'Gauge', step_count: int = 1):
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

    def add(self):
        self.update(self.value + 1)

    def finish(self):
        self.target.SetValue(int(self.next_step_progress))
        self.finished_step = True

    def over(self):
        if not self.finished_step:
            self.finish()
        self.target.SetValue(100)


class SegmentTrigger(object):
    def __init__(self, callbacks: Iterable[Callable], initcall: Optional[Callable] = None, *args, **kwargs):
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
