"""
Author       : noeru_desu
Date         : 2021-11-05 19:42:33
LastEditors  : noeru_desu
LastEditTime : 2022-04-06 21:40:46
Description  : 线程相关类
"""
from concurrent.futures import (CancelledError, ProcessPoolExecutor,
                                ThreadPoolExecutor)
from contextlib import suppress
from ctypes import c_long, py_object, pythonapi
from threading import Thread as threading_Thread
from traceback import print_exc
from typing import TYPE_CHECKING, Any, Callable, NamedTuple, Optional, Union

if TYPE_CHECKING:
    from concurrent.futures import Future


class ThreadKilled(SystemExit):
    pass


class ThreadTerminationFailed(Exception):
    pass


class ThreadIsRunningError(Exception):
    pass


class Thread(threading_Thread):
    __slots__ = ('_callback', '_callback_args', '_callback_kwargs', 'ended')

    def __init__(self, callback: Callable, callback_args=(), callback_kwargs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if callback_kwargs is None:
            callback_kwargs = {}
        self._callback = callback
        self._callback_args = callback_args
        self._callback_kwargs = callback_kwargs
        self.ended = False

    def run(self):
        result = None
        try:
            result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self.ended = True
            if self._callback is not None:
                try:
                    self._callback(e, result, *self._callback_args, **self._callback_kwargs)
                except Exception:
                    print_exc()
        except ThreadKilled as e:
            self.ended = True
            if self._callback is not None:
                try:
                    self._callback(e, result, *self._callback_args, **self._callback_kwargs)
                except Exception:
                    print_exc()
        else:
            self.ended = True
            if self._callback is not None:
                try:
                    self._callback(None, result, *self._callback_args, **self._callback_kwargs)
                except Exception:
                    print_exc()
        finally:
            del self._target, self._args, self._kwargs


class ThreadManager(object):
    __slots__ = ('thread_name', '_force', '_thread', '_raise_error', 'exit_signal')

    def __init__(self, thread_name: str = 'Worker', force: bool = False, raise_error=SystemExit):
        self.thread_name = thread_name
        self._force = force
        self._thread = None
        self._raise_error = raise_error
        self.exit_signal = False

    def start_new(self, target: Callable, callback: Callable = None, args=(), kwargs=None, callback_args=(), callback_kwargs=None):
        if not self._force and not self.is_ended:
            raise ThreadIsRunningError
        if self._force and self.is_alive and not self.kill():
            raise ThreadTerminationFailed
        self.exit_signal = False
        self._thread = Thread(callback, callback_args, callback_kwargs, target=target, name=self.thread_name, args=args, kwargs=kwargs, daemon=True)
        self._thread.start()

    def kill(self):
        if self._thread.is_alive():
            res = pythonapi.PyThreadState_SetAsyncExc(c_long(self._thread.ident), py_object(self._raise_error))
            if res not in (1, 0):
                pythonapi.PyThreadState_SetAsyncExc(self._thread.ident, None)
                return False
        return True

    def set_exit_signal(self, signal: bool = True):
        self.exit_signal = signal

    @property
    def is_alive(self):
        return False if self._thread is None else self._thread.is_alive()

    @property
    def is_ended(self):
        return True if self._thread is None else self._thread.ended


class TaskTag(NamedTuple):
    single: bool
    overwrite: bool
    futures: Optional[Union['Future', list['Future']]]


class ThreadTaskManager(ThreadPoolExecutor):
    __slots__ = ('task_dict')

    def __init__(self, max_workers: int = ..., *args, **kwargs):
        if 'thread_name_prefix' not in kwargs:
            kwargs['thread_name_prefix'] = 'worker_thread'
        super().__init__(max_workers, *args, **kwargs)
        self.task_dict: dict[Any, TaskTag] = {}

    def create_tag(self, tag_name, single: bool, overwrite: bool = True):
        self.task_dict[tag_name] = TaskTag(single, overwrite, None if single else [])

    def add_task(self, tag_name, future: 'Future', callback=None, *callback_args, **callback_kwargs):
        future.add_done_callback(lambda future: self.callback(tag_name, future, callback, *callback_args, **callback_kwargs))
        if self.task_dict[tag_name].single:
            self.task_dict[tag_name].futures = future
        else:
            self.task_dict[tag_name].futures.append(future)

    def callback(self, tag_name, future, callback=None, *callback_args, **callback_kwargs):
        if callback is not None:
            try:
                callback(future, tag_name, *callback_args, **callback_kwargs)
            except Exception:
                print_exc()
        self.del_future(tag_name, future)

    def cancel_task(self, tag_name=None, future: 'Future' = None) -> bool:
        if future is not None:
            if future.running():
                return False
            if not future.done():
                return future.cancel()
        elif tag_name is None:
            return True

        if self.task_dict[tag_name].futures is not None:
            if self.task_dict[tag_name].single:
                if self.task_dict[tag_name].futures.running():
                    return False
                if not self.task_dict[tag_name].futures.done():
                    return self.task_dict[tag_name].futures.cancel()
            else:
                all_cancelled = True
                for i in self.task_dict[tag_name].futures:
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
        if not self.task_dict[tag_name].futures:
            return None
        if not self.task_dict[tag_name].overwrite:
            return '已有一个任务正在进行'
        if self.cancel_task(tag_name):
            return None
        return '已有一个无法打断的任务正在进行' if self.task_dict[tag_name].single else '任务列表没有被完全取消'

    def del_future(self, tag_name, futures=None):
        if not (futures is None or self.task_dict[tag_name].single):
            self.task_dict[tag_name].futures.remove(futures)
        else:
            self.task_dict[tag_name].futures = None


class ProcessTaskManager(ProcessPoolExecutor):
    __slots__ = ('task_dict', 'watchdog')

    def __init__(self, max_workers: int = ..., *args, **kwargs):
        super().__init__(max_workers, *args, **kwargs)
        self.watchdog = ThreadTaskManager(max_workers, thread_name_prefix='process_pool_watchdog')
        self.task_dict: dict[Any, TaskTag] = {}

    def create_tag(self, tag_name: str, single: bool, overwrite: bool = True):
        self.watchdog.create_tag(tag_name, single, overwrite)
        self.task_dict[tag_name] = TaskTag(single, overwrite, None if single else [])

    def add_task(self, tag_name, future, callback=None, *callback_args, **callback_kwargs):
        if self.task_dict[tag_name].single:
            self.task_dict[tag_name].futures = future
        else:
            self.task_dict[tag_name].futures.append(future)
        self.watchdog.add_task(tag_name, self.watchdog.submit(self.wait, future), self.callback, future, callback, *callback_args, **callback_kwargs)

    def wait(self, future: 'Future'):
        with suppress(CancelledError):
            error = future.exception()
            if error is not None:
                print(error)

    def callback(self, watchdog_future, tag_name, future: 'Future', callback=None, *callback_args, **callback_kwargs):
        if callback is not None:
            try:
                callback(future, tag_name, future.result(), *callback_args, **callback_kwargs)
            except Exception:
                print_exc()
        self.del_future(tag_name, future)

    def cancel_task(self, tag_name=None, future: 'Future' = None):
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

        if self.task_dict[tag_name].futures is not None:
            if self.task_dict[tag_name].single:
                if self.task_dict[tag_name].futures.running():
                    return False
                if not self.task_dict[tag_name].futures.done():
                    if not self.task_dict[tag_name].futures.cancel():
                        return False
                    self.watchdog.cancel_task(tag_name)
                    return True
            else:
                all_cancelled = True
                for i in self.task_dict[tag_name].futures:
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
        if not self.task_dict[tag_name].futures:
            return None
        if not self.task_dict[tag_name].overwrite:
            return '已有一个任务正在进行'
        if self.cancel_task(tag_name):
            return None
        return '已有一个无法打断的任务正在进行' if self.task_dict[tag_name].single else '任务列表没有被完全取消'

    def del_future(self, tag_name, futures=None):
        if not (futures is None or self.task_dict[tag_name].single):
            self.task_dict[tag_name].futures.remove(futures)
        else:
            self.task_dict[tag_name].futures = None
