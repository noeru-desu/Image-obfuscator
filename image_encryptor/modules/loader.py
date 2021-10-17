'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-17 08:15:13
Description  : 程序的启动器，加载各参数与准备工作
'''
from atexit import register
from concurrent.futures import ProcessPoolExecutor
from os import system
from sys import argv

from image_encryptor.utils.logger import Logger
from image_encryptor.modules.parameter_parser import parse_parameters

program = None


class Program(object):
    def __init__(self):
        # 注册logger
        self.logger = Logger('image-encryptor')
        self.logger.warning('You are using Image encryptor 0.1.4')
        self.logger.warning('Open source at https://github.com/noeru-desu/Image-encryptor')
        # 检查启动参数
        self.parameter_parser = parse_parameters(self.logger, argv[1:])
        self.parameters = self.parameter_parser.parameters
        if self.parameters['debug']:
            self.logger.remove()
            self.logger = Logger('image-encryptor', 10, True)
        if self.parameters['xor_rgb'] or self.parameters['type'] == 'd':
            self.process_pool = ProcessPoolExecutor(self.parameters['process_count'])
        else:
            self.process_pool = None


def reload_program(logger=False, parameters=None, auto_set=False):
    if program is None:
        return load_program()
    if parameters:
        program.parameters = parse_parameters(program.logger, parameters)
        check_mode()
    if logger:
        program.logger.remove()
        program.logger = Logger('image-encryptor', 10 if program.parameters['debug'] else 20, program.parameters['debug'])
    if auto_set:
        if program.parameters['xor_rgb'] or program.parameters['type'] == 'd':
            create_process_pool()
    return program


def at_exit():
    if program.process_pool is not None:
        program.logger.info('程序退出，正在清理进程池')
        program.process_pool.shutdown(wait=False, cancel_futures=True)
        program.logger.info('完成')


def check_mode():
    if not program.parameters['normal_encryption'] and not program.parameters['xor_rgb']:
        program.logger.error('没有使用任何加密方法')
        system('pause>nul')
        exit()
    if program.parameters['mode'] is None:
        while True:
            mode = input('请选择处理模式[输入e表示加密或d表示解密]：\n').lower()
            if mode in ('e', 'd', 'q'):
                program.parameters['mode'] = mode
                break


def load_program():
    global program
    if program is None:
        program = Program()
        register(at_exit)
        check_mode()
    return program


def create_process_pool():
    if program.process_pool is None:
        program.process_pool = ProcessPoolExecutor(program.parameters['process_count'])
