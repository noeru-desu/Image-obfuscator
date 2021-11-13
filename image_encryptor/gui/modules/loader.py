'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-11-13 12:05:08
Description  : 程序的启动器，加载各参数与准备工作
'''
from atexit import register
from multiprocessing import cpu_count

from PIL.Image import init as PIL_init, EXTENSION

from image_encryptor import BRANCH, VERSION_NUMBER, SUB_VERSION_NUMBER, OPEN_SOURCE_URL, VERSION_BATCH
from image_encryptor.gui.modules.data import Data
from image_encryptor.common.utils.logger import Logger
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.gui.utils.utils import ProcessTaskManager, ThreadTaskManager

program = None


class Program(object):
    def __init__(self):
        # 注册logger
        self.logger = Logger('image-encryptor')
        self.logger.warning(f'You are using Image encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH}) (batch: {VERSION_BATCH})')
        self.logger.warning(f'Open source at {OPEN_SOURCE_URL}')
        # 全局变量模块
        self.data = Data()
        self.password_dict = PasswordDict()
        self.thread_pool = ThreadTaskManager(cpu_count())
        max_workers = 1
        if cpu_count() > 3:
            max_workers = cpu_count() - 2
        if max_workers > 61:
            max_workers = 61
        self.process_pool = ProcessTaskManager(max_workers)
        self.EXTENSION = None
        self.EXTENSION_KEYS = None


def at_exit():
    if program.thread_pool is not None:
        program.logger.info('程序退出，正在清理线程池')
        program.thread_pool.shutdown(wait=False, cancel_futures=True)
        program.logger.info('完成')


def load_program():
    global program
    if program is None:
        if not EXTENSION:
            PIL_init()
        program = Program()
        program.EXTENSION = EXTENSION
        program.EXTENSION_KEYS = [i.strip('.') for i in EXTENSION.keys()]
        register(at_exit)
    return program
