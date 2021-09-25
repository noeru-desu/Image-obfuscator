from atexit import register
from concurrent.futures import ProcessPoolExecutor
from sys import argv, exit

from .logger import Logger
from .start_mode import check_start_mode


class program_instances:
    def __init__(self):
        # 注册logger
        self.logger = Logger()
        # 检查启动参数
        self.parameter = check_start_mode(self.logger, argv[1:])
        if not self.parameter:
            self.logger.error('未知的启动属性或未给出启动属性')
            exit()
        if self.parameter['xor_rgb']:
            self.process_pool = ProcessPoolExecutor(self.parameter['process_count'])
        else:
            self.process_pool = None


def get_instances():
    return program


def create_process_pool():
    if program.process_pool is None:
        program.process_pool = ProcessPoolExecutor(program.parameter['process_count'])


program = program_instances()


@register
def at_exit():
    if program.process_pool is not None:
        program.logger.info('程序退出，正在清理进程池')
        program.process_pool.shutdown(wait=False, cancel_futures=True)
        program.logger.info('完成')
