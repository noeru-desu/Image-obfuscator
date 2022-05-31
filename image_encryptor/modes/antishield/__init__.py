"""
Author       : noeru_desu
Date         : 2022-04-17 12:11:48
LastEditors  : noeru_desu
LastEditTime : 2022-05-31 20:54:51
Description  : 
"""
from typing import TYPE_CHECKING

from image_encryptor.modes.antishield.main import normal_gen
from image_encryptor.modes.base import BaseModeInterface
from image_encryptor.modules.decorator import catch_exc_and_return

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class ModeInterface(BaseModeInterface):
    __slots__ = ('frame', 'mode_name', 'mode_qualname', 'enable_settings_panel', 'enable_password')
    file_name_suffix = ('', '-antishield')

    def __init__(self, frame: 'MainFrame', mode_id: int):
        self.frame = frame
        self.mode_name = '反屏蔽模式'
        self.mode_qualname = 'builtin.antishield.v1'
        self.enable_settings_panel = False
        self.enable_password = False

    @catch_exc_and_return
    def proc_image(self, *args):
        return normal_gen(*args)
