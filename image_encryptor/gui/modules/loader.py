'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-11-21 17:54:11
Description  : 程序的启动器，加载各参数与准备工作
'''
from atexit import register
from sys import version
from traceback import print_exc

from PIL.Image import init as PIL_init, EXTENSION

from image_encryptor import BRANCH, VERSION_NUMBER, SUB_VERSION_NUMBER, VERSION_BATCH
from image_encryptor.common.utils.logger import Logger
from image_encryptor.common.modules.password_verifier import PasswordDict

program = None


class Program(object):
    def __init__(self):
        # 注册logger
        self.logger = Logger('image-encryptor')
        self.logger.info(f'Python {version}')
        self.logger.info(f'You are using Image encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH}) (batch: {VERSION_BATCH})')
        self.password_dict = PasswordDict()
        self.EXTENSION = None
        self.EXTENSION_KEYS = None
        self.at_exit_func = []

    def at_exit(self, func, *args, **kwargs):
        self.at_exit_func.append((func, args, kwargs))

    def exit(self):
        self.logger.info('退出清理中')
        for func, args, kwargs in self.at_exit_func:
            try:
                func(*args, *kwargs)
            except Exception:
                print_exc()
                pass
        self.logger.info('完成')


def load_program():
    global program
    if program is None:
        if not EXTENSION:
            PIL_init()
        program = Program()
        program.EXTENSION = EXTENSION
        program.EXTENSION_KEYS = [i.strip('.') for i in EXTENSION.keys()]
        register(program.exit)
    return program
