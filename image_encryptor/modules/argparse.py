"""
Author       : noeru_desu
Date         : 2022-02-09 18:44:07
LastEditors  : noeru_desu
LastEditTime : 2022-02-19 21:04:55
Description  : 参数解析
"""
from argparse import ArgumentParser

from image_encryptor.constants import VERSION_NUMBER, SUB_VERSION_NUMBER, BRANCH


class Parameters(object):
    PARAMETER_NAMES = ('test', 'low_memory', 'dark_mode', '_dark_mode', 'maximum_redundant_cache_length')
    test: bool
    low_memory: bool
    maximum_redundant_cache_length: int
    _dark_mode: bool

    def __repr__(self) -> str:
        return ', '.join(f'{n} = {getattr(self, n)}' for n in self.PARAMETER_NAMES)

    @property
    def dark_mode(self) -> bool:
        return self._dark_mode

    @dark_mode.setter
    def dark_mode(self, v):
        self._dark_mode = v == 'confirm'


class Arguments(object):
    def __init__(self):
        self.argparser = ArgumentParser(add_help=False)
        self.argparser.add_argument('-h', '--help', action='help', help='输出参数帮助信息并退出')
        self.argparser.add_argument('-v', '--version', action='version', help='输出程序版本信息并退出', version=f'Image Encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH})')
        self.argparser.add_argument('--low-memory', dest='low_memory', action='store_true', help='低内存占用模式(磁盘读取频率与CPU占用将会有所升高)。默认关闭')
        self.argparser.add_argument('--MRCL', '--maximum-redundant-cache-length', dest='maximum_redundant_cache_length', default=5, type=int, help='处理后预览图冗余缓存量, 切换图像项目时自动清理冗余缓存。默认为5')
        self.argparser.add_argument('-t', '--test', dest='test', action='store_true', help='用于CI中测试程序能否正常初始化')
        self.argparser.add_argument('--dark-mode', dest='dark_mode', action='store', help='随便写的深色模式, 不提供启用方法(瞎写的)')

    def parse_args(self) -> Parameters:
        return self.argparser.parse_args(namespace=Parameters())
