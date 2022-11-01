"""
Author       : noeru_desu
Date         : 2022-05-08 15:16:41
LastEditors  : noeru_desu
LastEditTime : 2022-06-23 07:05:57
"""
from functools import wraps as functools_wraps
from traceback import format_exc
from typing import Callable

from image_obfuscator.utils.misc_utils import copy_signature
from image_obfuscator.utils.thread import TaskInterrupted

if __debug__:
    def catch_exc_and_return(func: Callable):
        @functools_wraps(func)
        def wrap(*args, **kwargs):
            # print(func.__qualname__)
            try:
                return func(*args, **kwargs), None
            except TaskInterrupted as e:
                raise e from e
            except Exception:
                return None, format_exc()
        copy_signature(wrap, func)
        return wrap
else:
    def catch_exc_and_return(func: Callable):
        return func


if __debug__:
    def catch_exc_for_frame_method(func: Callable):
        @functools_wraps(func)
        def wrap(self, *args, **kwargs):
            # print(func.__qualname__)
            try:
                return func(self, *args, **kwargs)
            except TaskInterrupted as e:
                raise e from e
            except Exception:
                self.dialog.error(format_exc())
        copy_signature(wrap, func)
        return wrap
else:
    def catch_exc_for_frame_method(func: Callable):
        return func
