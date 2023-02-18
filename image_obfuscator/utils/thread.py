"""
Author       : noeru_desu
Date         : 2021-11-05 19:42:33
LastEditors  : noeru_desu
LastEditTime : 2023-01-29 10:29:58
"""
from concurrent.futures import (CancelledError, ProcessPoolExecutor,
                                ThreadPoolExecutor)
from contextlib import suppress
from ctypes import c_long, py_object, pythonapi
from threading import Lock, Semaphore, Event
from threading import Thread as threading_Thread
from traceback import format_exc, print_exc
from typing import TYPE_CHECKING, Any, Callable, NamedTuple, Optional, Union

from image_obfuscator.utils.misc_utils import Deque

if TYPE_CHECKING:
    from concurrent.futures import Future

STOP = 2


class TaskInterrupted(Exception):
    pass


class ThreadTerminationFailed(Exception):
    pass


class ThreadIsRunningError(Exception):
    pass


class ThreadHasBeenShutdownError(Exception):
    pass


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


class SingleThreadExecutor(object):
    """单线程化线程池"""
    __slots__ = ('thread', 'name', 'deque', 'exc_cb', 'restartable')

    class Thread(threading_Thread):
        __slots__ = ('executor', 'semaphore', 'lock', 'exit_signal', 'in_execution', 'changed_signal', 'started')

        def __init__(self, executor: 'SingleThreadExecutor', name: str = 'single-thread-executor') -> None:
            super().__init__(name=name if name is ... else name, daemon=True)
            self.executor = executor
            self.semaphore = Semaphore(0)
            self.exit_signal = False
            self.in_execution = False
            self.idle = True
            self.changed_signal = False
            self.lock = Lock()
            self.pause = Event()
            self.pause.set()
            self.started = False

        def set_async_exc(self, exc_type: type[Any] = SystemExit):
            if self.is_alive():
                res = pythonapi.PyThreadState_SetAsyncExc(c_long(self.ident), py_object(exc_type))
                if res > 1:
                    pythonapi.PyThreadState_SetAsyncExc(self.ident, 0)
                    return False
            return True

        def run(self):
            while True:
                try:
                    if self.perform_task() == STOP:
                        break
                except TaskInterrupted:
                    pass
                except Exception:
                    print_exc()

        def perform_task(self):
            with self.lock:
                self.idle = True
                self.in_execution = False
            self.semaphore.acquire()
            self.pause.wait()
            with self.lock:
                if self.executor.deque.empty():
                    return
                self.idle = False
                if self.exit_signal:
                    return STOP
                self.changed_signal = False
                func, args, kwargs, cb_func, cb_args, cb_kwargs = self.executor.deque.get()
            try:
                with self.lock:
                    self.in_execution = True
                result = func(*args, **kwargs)
                with self.lock:
                    self.in_execution = False
                if cb_func is not None:
                    cb_func(result, *cb_args, **cb_kwargs)
            except TaskInterrupted:
                pass
            except Exception as e:
                if self.executor.exc_cb is None:
                    print_exc()
                else:
                    e.traceback = format_exc()
                    self.executor.exc_cb(e)

    def __init__(self, name: str = 'single-thread-executor', maxlen: int = None) -> None:
        """
        Args:
            name (str, optional): 线程名. 默认为`single-thread-executor`
            maxlen (int, optional): 最大队列长度. 默认为`None`, 即无限.

        注意: 当队列长度到达上限时添加任务, 将会挤出多余的任务(添加普通任务时删除下一个将被执行的任务, 添加最高优先级任务时删除最后将被执行的任务)
        """
        self.name = name
        self.exc_cb: Optional[Callable] = None
        self.deque: Deque[tuple[Callable, tuple, dict, Optional[Callable], tuple, dict]] = Deque(maxlen=maxlen, blocking=False)
        self.restartable = True
        self.thread: 'SingleThreadExecutor.Thread' = self.Thread(self, name)

    def restart_thread(self, clean_restart=True):
        """重启线程

        Args:
            clean_restart (bool, optional): 是否在重启时清空任务列表. 默认为`True`.
        """
        self.start_thread()
        if self.thread.is_alive():
            raise ThreadIsRunningError('The thread is already running.')
        if not self.restartable:
            raise ThreadHasBeenShutdownError('The current SingleThreadExecutor instance does not allow restarting threads.')
        if clean_restart:
            self.deque.clear()
        self.thread = self.Thread(self, self.name)
        if not clean_restart:
            self.thread.start()

    def start_thread(self):
        with self.thread.lock:
            if not self.thread.started:
                self.thread.start()
                self.thread.started = True

    def set_exception_callback(self, func: Callable, *args, **kwargs):
        """设置当任务内出现异常时将使用的回调. 将会在第一个参数中传入异常实例, 其`traceback`属性将被赋值为`traceback.format_exc()`"""
        self.exc_cb = lambda traceback: func(traceback, *args, **kwargs)

    def del_exception_callback(self):
        """删除异常回调, 将在出现异常时使用`traceback.print_exc()`"""
        self.exc_cb = None

    @property
    def task_list(self) -> list:
        """当前任务列表"""
        return list(self.deque)

    def get_task_list(self) -> list:
        """获取当前任务列表"""
        return list(self.deque)

    def clear_task(self):   # ? 待验证-可能出现信号量未重置的问题
        self.deque.clear()
        self.thread.semaphore = Semaphore(0)

    def shutdown(self, wait: bool = True, restartable=False):
        """关闭线程, 尚未被执行的任务将被搁置

        Args:
            wait (bool, optional): 是否等待当前任务(如果有)执行完成后再关闭. 默认为`True`. 为`False`时如果线程线程正在执行任务,
            则将强制中断, 且任务中申请的资源可能不会被释放. 如果线程处于空闲状态, 则该参数无效.
            restartable (bool, optional): 是否在线程关闭后仍可手动重启. 默认为`False`. 为`False`时未执行的任务相当于被舍弃.
        """
        self.set_exit_signal(True)
        if not wait and not self.thread.idle:
            self.interrupt_task()
        self.restartable = restartable

    def interrupt_task(self):
        """中断当前任务的执行操作, 并执行下一项任务(如果有)"""
        assert not self.thread.idle, 'No task in progress.'
        self.thread.set_async_exc(TaskInterrupted)

    def set_exit_signal(self, signal: bool = True):
        """设置结束信号

        Args:
            signal (bool, optional): 是否在当前任务(如果有)执行完成后结束线程, 尚未被执行的任务将被搁置. 默认为`True`.
            为`True`时等价于`shutdown(wait=True)`, 为`False`时可在当前任务(如果有)尚未执行完成前取消关闭计划.
        """
        with self.thread.lock:
            self.thread.exit_signal = signal
            if not self.thread.changed_signal:
                self.thread.changed_signal = True
                self.thread.semaphore.release()

    def add_task(self, target: Callable, args: tuple = (), kwargs: dict = None, cb: Callable = None, cb_args: tuple =(), cb_kwargs: dict = None, highest_priority: bool = False):
        """添加任务

        普通任务: 将在已有任务(如果有)顺次执行完毕后执行
        最高优先级任务: 将在当前任务(如果有)执行完毕后执行, 原有任务依次后移\n
        调用回调函数时将插入`target`的返回值在第一个参数的位置

        Args:
            target (Callable): 目标可调用对象
            args (tuple, optional): 目标可调用对象的positional参数. 默认为`()`.
            kwargs (dict, optional): 目标可调用对象的keyword参数. 默认为`{}`.
            cb (Callable, optional): 目标可调用对象调用完成后的回调. 默认为`None`. 为`None`时不进行回调, 回调的第一个参数为`target`的返回值
            cb_args (tuple, optional): 回调的positional参数. 默认为`()`.
            cb_kwargs (dict, optional): 回调的keyword参数. 默认为`{}`.
            highest_priority (bool, optional): 是否添加为最高优先级任务. 默认为`False`
        """
        self.start_thread()
        assert self.thread.is_alive(), 'Thread has been shutdown.'
        if kwargs is None:
            kwargs = {}
        if cb_kwargs is None:
            cb_kwargs = {}
        with self.thread.lock:
            is_full = self.deque.full()
            self.deque.put((target, args, kwargs, cb, cb_args, cb_kwargs), highest_priority)
            if not is_full:
                self.thread.semaphore.release()

    def pause(self):
        """暂停线程的任务获取操作"""
        self.thread.pause.clear()

    def unpause(self):
        """取消暂停线程的任务获取操作"""
        self.thread.pause.set()

    @property
    def full(self):
        """队列是否已满"""
        return self.deque.full()

    def is_full(self):
        """队列是否已满"""
        return self.deque.full()

    @property
    def alive(self):
        return (not self.thread.started) or self.thread.is_alive()

    def is_alive(self):
        return (not self.thread.started) or self.thread.is_alive()

    @property
    def idle(self):
        """是否为闲置状态(即完全空闲)"""
        return self.thread.idle

    @property
    def in_execution(self):
        """是否正在执行任务(不包含回调)"""
        return self.thread.in_execution


class ThreadManager(object):
    """重复创建线程执行任务的线程管理器"""
    __slots__ = ('thread_name', '_force', '_thread', '_raise_error', 'exit_signal')

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
            else:
                self.ended = True
                if self._callback is not None:
                    try:
                        self._callback(None, result, *self._callback_args, **self._callback_kwargs)
                    except Exception:
                        print_exc()
            finally:
                del self._target, self._args, self._kwargs

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
        self._thread = self.Thread(callback, callback_args, callback_kwargs, target=target, name=self.thread_name, args=args, kwargs=kwargs, daemon=True)
        self._thread.start()

    def kill(self):
        if self._thread is not None and self._thread.is_alive():
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
