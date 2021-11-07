'''
Author       : noeru_desu
Date         : 2021-11-05 19:42:33
LastEditors  : noeru_desu
LastEditTime : 2021-11-06 19:02:33
Description  : 线程相关类
'''
from ctypes import c_long, py_object, pythonapi
from threading import Thread as threading_Thread
from typing import Callable


class ThreadKilled(SystemExit):
    pass


class ThreadTerminationFailed(Exception):
    pass


class Thread(threading_Thread):
    def __init__(self, callback: Callable, callback_args=(), callback_kwargs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if callback_kwargs is None:
            callback_kwargs = {}
        self._callback = callback
        self._callback_args = callback_args
        self._callback_kwargs = callback_kwargs

    def run(self):
        result = None
        try:
            result = self._target(*self._args, **self._kwargs)
        except Exception as e:
            self._callback(e, result, *self._callback_args, **self._callback_kwargs)
        except ThreadKilled as e:
            self._callback(e, result, *self._callback_args, **self._callback_kwargs)
        finally:
            del self._target, self._args, self._kwargs
            self._callback(None, result, *self._callback_args, **self._callback_kwargs)


class ThreadManager(object):
    def __init__(self, thread_name: str = 'Worker'):
        self.thread_name = thread_name
        self._thread = None

    def start_new(self, target: Callable, callback: Callable, args=(), kwargs=None, callback_args=(), callback_kwargs=None):
        if self._thread is not None and self._thread.is_alive() and not self.kill():
            raise ThreadTerminationFailed
        self._thread = Thread(callback, callback_args, callback_kwargs, target=target, name=self.thread_name, args=args, kwargs=kwargs, daemon=True)
        self._thread.start()

    def kill(self):
        if self._thread.is_alive():
            res = pythonapi.PyThreadState_SetAsyncExc(c_long(self._thread.ident), py_object(ThreadKilled))
            if res != 1 and res != 0:
                pythonapi.PyThreadState_SetAsyncExc(self._thread.ident, None)
                return False
        return True
