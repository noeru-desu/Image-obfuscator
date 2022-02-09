'''
Author       : noeru_desu
Date         : 2022-02-09 18:44:07
LastEditors  : noeru_desu
LastEditTime : 2022-02-09 19:19:10
Description  : 参数解析
'''
from argparse import ArgumentParser

from image_encryptor.constants import VERSION_NUMBER, SUB_VERSION_NUMBER, BRANCH


class Parameters(object):
    PARAMETER_NAMES = ('test', 'low_memory', 'dark_mode', '_dark_mode')
    test: bool
    low_memory: bool
    _dark_mode: str

    def __repr__(self) -> str:
        return ', '.join(f'{n} = {getattr(self, n)}' for n in self.PARAMETER_NAMES)

    @property
    def dark_mode(self) -> bool:
        return self._dark_mode == 'confirm'

    @dark_mode.setter
    def dark_mode(self, v):
        self._dark_mode = v


class Arguments(object):
    def __init__(self):
        self.argparser = ArgumentParser(add_help=False)
        self.argparser.add_argument('-h', '--help', action='help', help='输出参数帮助信息并退出')
        self.argparser.add_argument('-v', '--version', action='version', help='输出程序版本信息并退出', version=f'Image Encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH})')
        self.argparser.add_argument('--low-memory', action='store_true', help='低内存占用模式(磁盘读取频率与CPU占用将会有所升高)')
        self.argparser.add_argument('-t', '--test', action='store_true', help='用于CI中测试程序能否正常初始化')
        self.argparser.add_argument('--dark-mode', action='store', help='随便写的深色模式, 不提供启用方法(瞎写的)')

    def parse_args(self) -> Parameters:
        return self.argparser.parse_args(namespace=Parameters())
