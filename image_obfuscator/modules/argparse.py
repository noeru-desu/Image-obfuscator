"""
Author       : noeru_desu
Date         : 2022-02-09 18:44:07
LastEditors  : noeru_desu
LastEditTime : 2022-07-23 19:34:53
Description  : 参数解析
"""
from argparse import ArgumentParser
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image_obfuscator.frame.controller import Controller

# from image_obfuscator.constants import VERSION_INFO


class Parameters(object):
    MAIN_PARAMETER_NAMES = (
        'disable_cache', 'low_memory', 'maximum_redundant_cache_length', 'record_interface_settings',
        'record_password_dict', 'final_layout_widgets'
    )
    MAIN_PARAMETERS_CORRESPONDING_NAMES = (
        'disable_cache', 'low_memory_mode', 'redundant_cache_length', 'record_interface_settings',
        'record_password_dict', 'final_layout_widgets'
    )
    __slots__ = ALL_PARAMETER_NAMES = (
        'disable_cache', 'test', 'low_memory', '_dark_mode', 'maximum_redundant_cache_length',
        'record_interface_settings', 'record_password_dict', 'final_layout_widgets'
    )

    _dark_mode: bool
    record_interface_settings: bool
    record_password_dict: bool
    maximum_redundant_cache_length: int
    low_memory: bool
    disable_cache: bool
    final_layout_widgets: bool
    test: bool

    def __init__(self) -> None:
        self.test = False
        self.disable_cache = False
        self.low_memory = False
        self.maximum_redundant_cache_length = 5
        self._dark_mode = False
        self.record_interface_settings = True
        self.record_password_dict = True
        self.final_layout_widgets = False

    def __repr__(self) -> str:
        return ', '.join(f'{n} = {getattr(self, n)}' for n in self.ALL_PARAMETER_NAMES)

    @property
    def dark_mode(self) -> bool:
        return self._dark_mode

    @dark_mode.setter
    def dark_mode(self, v):
        self._dark_mode = v == 'confirm'

    @property
    def parameters_dict(self) -> dict:
        return {k: getattr(self, k) for k in self.MAIN_PARAMETER_NAMES}

    @parameters_dict.setter
    def parameters_dict(self, v: dict):
        for k, _v in v.items():
            if k in self.MAIN_PARAMETER_NAMES:
                setattr(self, k, _v)

    def apply_to_interface(self, controller: 'Controller'):
        for i, j in zip(self.MAIN_PARAMETER_NAMES, self.MAIN_PARAMETERS_CORRESPONDING_NAMES):
            setattr(controller, j, getattr(self, i))


class Arguments(object):
    __slots__ = ('argparser',)

    def __init__(self):
        self.argparser = ArgumentParser(add_help=False)
        self.argparser.add_argument('-h', '--help', action='help', help='输出参数帮助信息并退出')
        # self.argparser.add_argument('-v', '--version', action='version', help='输出程序版本信息并退出', version=VERSION_INFO)   # TODO 不会换行
        self.argparser.add_argument('--disable-cache', dest='disable_cache', action='store_true', help='禁用处理结果缓存(仍会存储, 但不会使用)。默认关闭')
        self.argparser.add_argument('--low-memory', dest='low_memory', action='store_true', help='低内存占用模式(磁盘读取频率与CPU占用率将会有所升高)。默认关闭')
        self.argparser.add_argument('--final-layout-widgets', dest='final_layout_widgets', action='store_true', help='在拖动更改窗口大小时不实时更改部件排版, 在拖动更改大小时卡顿过于严重的情况下可开启。默认关闭')
        self.argparser.add_argument('--MRCL', '--maximum-redundant-cache-length', dest='maximum_redundant_cache_length', default=5, type=int, help='处理后预览图冗余缓存量, 切换图像项目时自动清理冗余缓存。默认为5')
        self.argparser.add_argument('--record-interface-settings', dest='record_interface_settings', action='store_true', help='是否在退出时记录界面设置, 并在下次启动时回溯界面。默认开启')
        self.argparser.add_argument('--record-password-dict', dest='record_password_dict', action='store_true', help='是否在退出时保存密码字典, 并在下次启动时重新载入。默认关闭')
        self.argparser.add_argument('-t', '--test', dest='test', action='store_true', help='用于CI中测试程序能否正常初始化')
        # self.argparser.add_argument('--dark-mode', dest='dark_mode', action='store', help='随便写的深色模式, 不提供启用方法(瞎写的)')

    def parse_args(self, namespace: Parameters) -> Parameters:
        return self.argparser.parse_args(namespace=namespace)
