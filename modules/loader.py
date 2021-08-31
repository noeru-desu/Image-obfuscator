from sys import argv, exit

from .logger import Logger
from .start_mode import check_start_mode


class program_instances:
    def __init__(self):
        # 注册logger
        self.logger = Logger()
        # 检查启动参数
        self.parameter = check_start_mode(argv[1:])
        if not self.parameter:
            self.logger.error('未知的启动属性或未给出启动属性')
            exit()


def get_instances():
    return program


program = program_instances()
