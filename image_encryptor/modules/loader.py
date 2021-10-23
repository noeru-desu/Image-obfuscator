'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-23 18:20:30
Description  : 程序的启动器，加载各参数与准备工作
'''
from atexit import register
from concurrent.futures import ProcessPoolExecutor

from PIL import Image

from image_encryptor.modules.data import Data
from image_encryptor.utils.logger import Logger
from image_encryptor.utils.password_verifier import PasswordDict

program = None


class Program(object):
    def __init__(self):
        # 注册logger
        self.logger = Logger('image-encryptor')
        self.logger.warning('You are using Image encryptor 1.0.0-alpha.1 (branch: features/gui)')
        self.logger.warning('Open source at https://github.com/noeru-desu/Image-encryptor')
        # 全局变量模块
        self.data = Data()
        self.password_dict = PasswordDict()


def at_exit():
    if program.process_pool is not None:
        program.logger.info('程序退出，正在清理进程池')
        program.process_pool.shutdown(wait=False, cancel_futures=True)
        program.logger.info('完成')


def load_program():
    global program
    if program is None:
        if not Image.EXTENSION:
            Image.init()
            Image.EXTENSION_KEYS = list(Image.EXTENSION.keys())
        program = Program()
        register(at_exit)
    return program


def create_process_pool(max_workers):
    if max_workers != program.process_pool_max_workers:
        if program.process_pool is not None:
            program.process_pool.shutdown(wait=False, cancel_futures=True)
        program.process_pool = ProcessPoolExecutor(max_workers)
