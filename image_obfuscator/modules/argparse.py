"""
Author       : noeru_desu
Date         : 2022-02-09 18:44:07
LastEditors  : noeru_desu
LastEditTime : 2023-01-15 09:55:52
"""
# from argparse import ArgumentParser
from os.path import isdir
from sys import argv
from typing import TYPE_CHECKING

from image_obfuscator.constants import LOCAL_APPDATA_TEMP

if TYPE_CHECKING:
    from os import PathLike
    from image_obfuscator.frame.controller import Controller


class Options(object):
    MAIN_PARAMETER_NAMES = (
        'disable_cache', 'maximum_redundant_cache_length', 'record_interface_settings',
        'record_password_dict', 'final_layout_widgets', 'maximum_orig_image_cache',
        'maximum_proc_result_cache', 'no_extra_data_cache', 'temp_dir'
    )
    MAIN_PARAMETERS_CORRESPONDING_NAMES = (
        'disable_cache', 'redundant_cache_length', 'record_interface_settings',
        'record_password_dict', 'final_layout_widgets', 'maximum_orig_image_cache',
        'maximum_proc_result_cache', 'no_extra_data_cache', 'temp_dir'
    )
    __slots__ = ALL_PARAMETER_NAMES = (
        'disable_cache', 'test', '_dark_mode', 'maximum_redundant_cache_length',
        'record_interface_settings', 'record_password_dict', 'final_layout_widgets',
        'maximum_orig_image_cache', 'maximum_proc_result_cache', 'no_extra_data_cache',
        '_temp_dir'
    )

    _dark_mode: bool
    temp_dir: 'PathLike[str]'
    no_extra_data_cache: bool
    record_interface_settings: bool
    record_password_dict: bool
    maximum_redundant_cache_length: int
    disable_cache: bool
    final_layout_widgets: bool
    maximum_orig_image_cache: int
    maximum_proc_result_cache: int
    test: bool

    def __init__(self) -> None:
        self.disable_cache = False
        self.maximum_redundant_cache_length = 5
        self._dark_mode = False
        self.no_extra_data_cache = False
        self.temp_dir = LOCAL_APPDATA_TEMP
        self.record_interface_settings = True
        self.record_password_dict = True
        self.final_layout_widgets = False
        self.maximum_orig_image_cache = 20
        self.maximum_proc_result_cache = 20
        self.test = len(argv) > 1 and argv[1] == '-t'

    def __repr__(self) -> str:
        return ', '.join(f'{n} = {getattr(self, n)}' for n in self.ALL_PARAMETER_NAMES)

    @property
    def dark_mode(self) -> bool:
        return self._dark_mode

    @dark_mode.setter
    def dark_mode(self, v):
        self._dark_mode = v == 'confirm'

    @property
    def temp_dir(self):
        return self._temp_dir

    @temp_dir.setter
    def temp_dir(self, v: str):
        if isdir(v):
            self._temp_dir = v

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

'''
class Arguments(object):
    __slots__ = ('argparser',)

    def __init__(self):
        self.argparser = ArgumentParser(add_help=False)
        self.argparser.add_argument('-h', '--help', action='help', help='输出参数帮助信息并退出')
        # self.argparser.add_argument('-v', '--version', action='version', help='输出程序版本信息并退出', version=VERSION_INFO)   # TODO 不会换行
        self.argparser.add_argument('--disable-cache', dest='disable_cache', action='store_true', help='禁用处理结果缓存(仍会存储, 但不会使用)。默认关闭')
        self.argparser.add_argument('--final-layout-widgets', dest='final_layout_widgets', action='store_true', help='在拖动更改窗口大小时不实时更改部件排版, 在拖动更改大小时卡顿过于严重的情况下可开启。默认关闭')
        self.argparser.add_argument('--MRCL', '--maximum-redundant-cache', dest='maximum_redundant_cache_length', default=5, type=int, help='处理后预览图冗余缓存量, 切换图像项目时自动清理冗余缓存。默认为5')
        self.argparser.add_argument('--record-interface-settings', dest='record_interface_settings', action='store_true', help='是否在退出时记录界面设置, 并在下次启动时回溯界面。默认开启')
        self.argparser.add_argument('--record-password-dict', dest='record_password_dict', action='store_true', help='是否在退出时保存密码字典, 并在下次启动时重新载入。默认关闭')
        self.argparser.add_argument('--MOIC', '--maximum-orig-image-cache', dest='maximum_orig_image_cache', default=20, type=int, help='未开启低内存占用模式时, 可缓存原始图像数据的数量上限。0为无限制。默认为20')
        self.argparser.add_argument('--MPRC', '--maximum-proc-result-cache', dest='maximum_proc_result_cache', default=20, type=int, help='未开启低内存占用模式时, 可缓存处理结果数据的数量上限。0为无限制。默认为20')
        self.argparser.add_argument('-t', '--test', dest='test', action='store_true', help='用于CI中测试程序能否正常初始化')
        # self.argparser.add_argument('--dark-mode', dest='dark_mode', action='store', help='随便写的深色模式, 不提供启用方法(瞎写的)')

    def parse_args(self, namespace: Parameters) -> Parameters:
        return self.argparser.parse_args(namespace=namespace)
'''
