'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-09 21:04:55
Description  : 参数解析器
'''
from getopt import GetoptError, getopt
from multiprocessing import cpu_count
from os import makedirs, system
from os.path import isdir, isfile, normpath, split
from sys import exit

from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init

from image_encryptor.utils.utils import calculate_formula_string

help_msg = '''
<path> <save-path> [--nm] [-pw password] [-r row] [-c column] [-f file_format]

<path> 图片/文件夹 路径
<save-path> 保存路径
可选参数：
-l / --loop 启用自动循环，程序每次执行完任务后不直接退出，等待输入下一个操作的参数。为空时退出
-e / --encrypt 加密模式
-d / --decrypt 解密模式
-t / --topdown 批量加解密时不仅遍历表层文件夹，同时遍历所有文件夹内的文件夹
--rm / --rgb-mapping 启用RGB随机映射
-x rgb/rgba / --xor rgb/rgba 异或加密rgb/rgba通道
--pw password / --password password 密码
-r row / --row row 分割行数
-c column / --col column / --column column 分割列数
-f file_format / --format file_format 指定保存的文件格式
--pc process_count / --process-count process_count 指定用于异或加解密/批量加解密的进程池大小，可使用运算符。提供{cpu_count}，表示cpu数量(每个cpu的核数之和)
'''

CPU_COUNT = cpu_count()

shortopts = 'hledtf:r:c:x:'
longopts = ['help', 'loop', 'encrypt', 'decrypt',
            'topdown', 'format=', 'pw=', 'password=',
            'row=', 'col=', 'column=', 'nne',
            'no-normal-encryption', 'rm', 'rgb-mapping', 'xor=',
            'pc=', 'process-count=', 'debug']


class ParameterParser(object):
    def __init__(self, logger, argv):
        self.argv = argv
        self.logger = logger
        self.initialize()
        self.parsing_methods = {
            '-h': self.help, '--help': self.help,
            '-l': self.loop, '--loop': self.loop,
            '-e': self.encrypt, '--encrypt': self.encrypt,
            '-d': self.decrypt, '--decrypt': self.decrypt,
            '-t': self.topdown, '--topdown': self.topdown,
            '--nne': self.normal_encryption, '--no-normal-encryption': self.normal_encryption,
            '--rm': self.rgb_mapping, '--rgb-mapping': self.rgb_mapping,
            '-x': self.xor, '--xor': self.xor,
            '-r': self.row, '--row': self.row,
            '-c': self.col, '--col': self.col, '--column': self.col,
            '--pw': self.password, '--password': self.password,
            '-f': self.format, '--format': self.format,
            '--pc': self.process_count, '--process-count': self.process_count,
            '--debug': self.debug
        }

    def initialize(self):
        self._initialize_parameters()
        self._initialize_vars()

    def _initialize_vars(self):
        self.input_path = normpath(self.argv[0])
        self.file_path = split(self.input_path)[0]

        # 补全输出路径
        if len(self.argv) == 1 or self.argv[1].startswith('-'):
            self.output_path = self.file_path
            self.skip_argv = 1
        else:
            self.output_path = normpath(self.argv[1].format(input_path=self.file_path))
            self.skip_argv = 2

        # 选择加密类型
        if isfile(self.input_path):
            self.parameters['type'] = 'f'
        elif isdir(self.input_path):
            if self.skip_argv == 1:
                self.parameters['output_path'] = self.output_path = self.input_path
            self.parameters['type'] = 'd'
        else:
            self.logger.error('没有提供文件或文件不存在')
            exit(2)

        # 检测保存位置是否存在
        if isfile(self.output_path):
            self.logger.error(f'提供的保存位置[{self.output_path}]不是文件夹')
            exit(2)
        elif not isdir(self.output_path):
            self.logger.warning(f'提供的保存位置[{self.output_path}]不存在，按任意键自动创建')
            system('pause>nul')
            makedirs(self.output_path)

        self.parameters['input_path'] = self.input_path
        self.parameters['output_path'] = self.output_path

    def _initialize_parameters(self):
        self.parameters = {
            'loop': False,
            'mode': None,
            'type': None,
            'topdown': False,
            'input_path': None,
            'output_path': None,
            'format': None,
            'normal_encryption': True,
            'mapping': False,
            'xor_rgb': False,
            'xor_alpha': False,
            'password': 100,
            'row': 25,
            'col': 25,
            'process_count': 1 if CPU_COUNT < 3 else CPU_COUNT - 2,
            'debug': False
        }

    def help(self, arg):
        self.logger.info(help_msg)
        exit()

    def loop(self, arg):
        self.parameters['loop'] = True

    def encrypt(self, arg):
        self.parameters['mode'] = 'e'

    def decrypt(self, arg):
        self.parameters['mode'] = 'd'

    def topdown(self, arg):
        self.logger.info('已启用多层遍历')
        self.parameters['topdown'] = True

    def normal_encryption(self, arg):
        self.logger.info('已禁用常规加密')
        self.parameters['normal_encryption'] = False

    def rgb_mapping(self, arg):
        self.logger.info('已启用RGB随机映射')
        self.parameters['mapping'] = True

    def xor(self, arg):
        if arg.lower() == 'rgb':
            self.logger.info('已启用异或加密(不包括透明通道)')
            self.parameters['xor_rgb'] = True
        elif arg.lower() == 'rgba':
            self.logger.info('已启用异或加密(包括透明通道)')
            self.parameters['xor_rgb'] = True
            self.parameters['xor_alpha'] = True
        else:
            self.logger.info(f'异或加密参数设置有误：{arg}')

    def row(self, arg):
        try:
            self.parameters['row'] = int(arg)
            self.logger.info(f'已指定切割行数为 {arg}')
        except ValueError:
            row, error = calculate_formula_string(arg, width=1, height=1)
            if error is not None:
                self.logger.error('测试运算输入的切割行数参数时出现错误：')
                self.logger.error(error)
            else:
                self.parameters['row'] = arg

    def col(self, arg):
        try:
            self.parameters['col'] = int(arg)
            self.logger.info(f'已指定切割列数为 {arg}')
        except ValueError:
            col, error = calculate_formula_string(arg, width=1, height=1)
            if error is not None:
                self.logger.error('测试运算输入的切割列数参数时出现错误：')
                self.logger.error(error)
            else:
                self.parameters['col'] = arg

    def password(self, arg):
        self.logger.info(f'已设置密码为 {arg}')
        self.parameters['password'] = arg

    def format(self, arg):
        arg = arg.lower()
        if '.' + arg not in EXTENSION:
            self.logger.error(f'不支持指定的格式：{arg}')
            self.logger.error(f"支持的格式：{', '.join(EXTENSION)}")
        else:
            self.logger.info(f'指定保存格式为 {arg}')
            self.parameters['format'] = arg

    def process_count(self, arg):
        process_count, error = calculate_formula_string(arg, cpu_count=CPU_COUNT)
        if error is not None:
            self.logger.error('运算输入的线程池大小参数时出现错误：')
            self.logger.error(error)
        else:
            if process_count <= 0 or process_count > 61:
                self.logger.error("指定的进程池大小不符合标准")
            elif process_count > CPU_COUNT:
                self.logger.warning(f"设置的进程池大小({self.parameters['process_count']})大于本机cpu数量({CPU_COUNT})，性能可能会有所下降")
                self.parameters['process_count'] = process_count
            else:
                self.logger.info(f"已设置进程池大小为 {self.parameters['process_count']}")
                self.parameters['process_count'] = process_count

    def debug(self, arg):
        self.logger.info('已启用调试模式')
        self.parameters['debug'] = True


def parse_parameters(logger, argv):
    # 检测是否直接输出帮助信息
    if not argv or argv[0] in ('-h', '--help'):
        logger.info(help_msg)
        exit()

    # 检测PIL是否初始化
    if not EXTENSION:
        PIL_init()

    parameters = ParameterParser(logger, argv)

    # 解析参数
    try:
        opts, args = getopt(argv[parameters.skip_argv:], shortopts, longopts)
    except GetoptError as e:
        logger.error(f'未知的参数：{e.opt}')
        logger.info(help_msg)
        exit(2)
    for opt, arg in opts:
        parameters.parsing_methods[opt](arg)
    return parameters.parameters
