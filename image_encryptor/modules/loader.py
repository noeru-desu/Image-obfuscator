from atexit import register
from concurrent.futures import ProcessPoolExecutor
from sys import argv

from image_encryptor.utils.logger import Logger
from .parameter_parser import parsing_parameters

program = None


class Initializer:
    def __init__(self):
        # 注册logger
        self.logger = Logger()
        # 检查启动参数
        self.parameters = parsing_parameters(self.logger, argv[1:])
        if self.parameters['xor_rgb'] or self.parameters['type'] == 'd':
            self.process_pool = ProcessPoolExecutor(self.parameters['process_count'])
        else:
            self.process_pool = None


def reload_program(logger=False, parameters=None, auto_set=False):
    if program is None:
        return load_program()
    if logger:
        program.logger = Logger()
    if parameters:
        program.parameters = parsing_parameters(program.logger, parameters)
        check_mode()
    if auto_set:
        if program.parameters['xor_rgb'] or program.parameters['type'] == 'd':
            program.process_pool = ProcessPoolExecutor(program.parameters['process_count'])
        else:
            program.process_pool = None
    return program


def at_exit():
    if program.process_pool is not None:
        program.logger.info('程序退出，正在清理进程池')
        program.process_pool.shutdown(wait=False, cancel_futures=True)
        program.logger.info('完成')


def check_mode():
    if program.parameters['mode'] is None:
        while True:
            mode = input('请选择处理模式[输入e表示加密或d表示解密]：\n').lower()
            if mode in ('e', 'd'):
                program.parameters['mode'] = mode
                break


def load_program():
    global program
    if program is None:
        program = Initializer()
        register(at_exit)
        check_mode()
    return program


def create_process_pool():
    if program.process_pool is None:
        program.process_pool = ProcessPoolExecutor(program.parameters['process_count'])
