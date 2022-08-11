"""
Author       : noeru_desu
Date         : 2022-04-17 12:11:48
LastEditors  : noeru_desu
LastEditTime : 2022-08-08 10:55:46
Description  : 
"""
from typing import TYPE_CHECKING

from image_obfuscator.modes.antishield.main import normal_gen, normal_gen_quietly
from image_obfuscator.modes.base import BaseModeInterface


class ModeInterface(BaseModeInterface):
    __slots__ = ()

    file_name_suffix = ('', '-antishield')
    mode_name = '反屏蔽模式'
    mode_qualname = 'builtin.antishield.v1'

    def proc_image(self, *args):
        return normal_gen(*args)

    def proc_image_quietly(self, *args):
        return normal_gen_quietly(*args)
