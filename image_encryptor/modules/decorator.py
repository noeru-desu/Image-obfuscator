"""
Author       : noeru_desu
Date         : 2022-05-08 15:16:41
LastEditors  : noeru_desu
LastEditTime : 2022-05-12 06:27:12
Description  : 装饰器
"""
from functools import wraps as functools_wraps
from traceback import format_exc

from image_encryptor.utils.misc_utils import copy_signature
from image_encryptor.utils.thread import TaskInterrupted

if __debug__:
    def catch_exc_and_return(func):
        @functools_wraps(func)
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs), None
            except TaskInterrupted as e:
                raise e from e
            except Exception:
                return None, format_exc()
        copy_signature(wrap, func)
        return wrap
else:
    def catch_exc_and_return(func):
        warp = functools_wraps(func)(lambda *args, **kwargs: (func(*args, **kwargs), None))
        copy_signature(warp, func)
        return warp


if __debug__:
    def catch_exc_for_frame_method(func):
        @functools_wraps(func)
        def wrap(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except TaskInterrupted as e:
                raise e from e
            except Exception:
                self.dialog.error(format_exc())
        copy_signature(wrap, func)
        return wrap
else:
    def catch_exc_for_frame_method(func):
        return func
