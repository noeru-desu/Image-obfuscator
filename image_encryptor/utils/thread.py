'''
Author       : noeru_desu
Date         : 2021-11-05 19:42:33
LastEditors  : noeru_desu
LastEditTime : 2022-02-05 20:50:50
Description  : 线程相关类
'''
from ctypes import c_long, py_object, pythonapi
from threading import Thread as threading_Thread
from traceback import print_exc
from typing import Callable


class ThreadKilled(SystemExit):
    pass


class ThreadTerminationFailed(Exception):
    pass


class ThreadIsRunningError(Exception):
    pass


class Thread(threading_Thread):
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
            if res != 1 and res != 0:
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
