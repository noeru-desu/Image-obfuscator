"""
Author       : noeru_desu
Date         : 2022-04-17 12:11:48
LastEditors  : noeru_desu
LastEditTime : 2022-05-28 06:10:47
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.antishield.main import normal_gen
from image_encryptor.modes.base import BaseModeInterface

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class ModeInterface(BaseModeInterface):
    __slots__ = ('frame', 'mode_name', 'mode_qualname', 'enable_settings_panel', 'enable_password', 'gen_preview')

    def __init__(self, frame: 'MainFrame', mode_id: int):
        self.frame = frame
        self.mode_name = '反屏蔽模式'
        self.mode_qualname = 'builtin.antishield.v1'
        self.enable_settings_panel = False
        self.enable_password = False
        self.gen_preview = normal_gen
