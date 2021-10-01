from getopt import GetoptError, getopt
from multiprocessing import cpu_count
from os.path import isdir, isfile, normpath
from sys import exit

from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init

help_msg = '''
<path> [--nm] [-pw password] [-r row] [-c column] [-f file_format]

<path> 图片/文件夹 路径
可选参数：
-e 加密模式
-d 解密模式
--rm / --rgb-mapping 启用RGB随机映射
-x rgb/rgba / --xor rgb/rgba 异或加密rgb/rgba通道
--pw password / --password password 密码
-r row / --row row 分割行数
-c column / --col column / --column column 分割列数
-f file_format / --format file_format 指定保存的文件格式
--pc process_count / --process-count process_count 指定用于异或加解密/批量加解密的进程池大小，可使用运算符。提供{cpu_count}，表示cpu数量(每个cpu的核数之和)
'''


def parsing_parameters(logger, argv):
    if not argv or argv[0] in ('-h', '--help'):
        logger.info(help_msg)
        exit()
    CPU_COUNT = cpu_count()
    parameter = {
        'mode': None,
        'type': None,
        'path': normpath(argv[0]),
        'format': 'normal',
        'mapping': False,
        'xor_rgb': False,
        'xor_alpha': False,
        'password': 100,
        'row': 25,
        'col': 25,
        'process_count': 1 if CPU_COUNT < 3 else CPU_COUNT - 2
    }
    if isfile(argv[0]):
        parameter['type'] = 'f'
    elif isdir(argv[0]):
        parameter['type'] = 'd'
    else:
        logger.warning('没有提供文件或文件不存在')
        exit(2)
    if not EXTENSION:
        PIL_init()
    try:
        opts, args = getopt(argv[1:], 'edhf:r:c:x:', ['help', 'format=', 'pw=', 'password=', 'row=', 'col=', 'column=', 'rm', 'rgb-mapping', 'xor=', 'pc=', 'process-count='])
    except GetoptError as e:
        logger.error(f'未知的参数：{e.opt}')
        logger.info(help_msg)
        exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            logger.info(help_msg)
            exit()
        elif opt == '-e':
            parameter['mode'] = 'e'
        elif opt == '-d':
            parameter['mode'] = 'd'
        elif opt in ('--rm', '--rgb-mapping'):
            logger.info('已启用RGB随机映射')
            parameter['mapping'] = True
        elif opt in ('-x', '--xor'):
            if arg.lower() == 'rgb':
                logger.info('已启用异或加密(不包括透明通道)')
                parameter['xor_rgb'] = True
            elif arg.lower() == 'rgba':
                logger.info('已启用异或加密(包括透明通道)')
                parameter['xor_rgb'] = True
                parameter['xor_alpha'] = True
            else:
                logger.info(f'异或加密参数设置有误：{arg}')
        elif opt in ('-r', '--row'):
            try:
                parameter['row'] = int(arg)
                logger.info(f'已指定切割行数为 {arg}')
            except ValueError:
                logger.error('指定的切割行数不为纯数字')
        elif opt in ('-c', '--col', '--column'):
            try:
                parameter['col'] = int(arg)
                logger.info(f'已指定切割列数为 {arg}')
            except ValueError:
                logger.error('指定的切割列数不为纯数字')
        elif opt in ('--pw', '--password'):
            logger.info(f'已设置密码为 {arg}')
            parameter['password'] = arg
        elif opt in ('-f', '--format'):
            arg = arg.lower()
            if '.' + arg not in EXTENSION:
                logger.error(f'不支持指定的格式：{arg}')
                logger.error(f"支持的格式：{', '.join(EXTENSION)}")
            else:
                logger.info(f'指定保存格式为 {arg}')
                parameter['format'] = arg
        elif opt in ('--pc', '--process-count'):
            try:
                process_count = int(eval(arg.format(cpu_count=CPU_COUNT)))
            except SyntaxError:
                logger.error("指定的进程池大小算式格式错误")
            except NameError:
                logger.error("指定的进程池大小不为纯数字")
            except KeyError as e:
                logger.error(f"未知的变量：{str(e)}。当前支持：cpu_count")
            except Exception as e:
                logger.error("指定的进程池大小运算出现错误")
                logger.error(repr(e))
            else:
                if process_count <= 0 or process_count > 61:
                    logger.error("指定的进程池大小不符合标准")
                elif process_count > CPU_COUNT:
                    logger.warning(f"设置的进程池大小({parameter['process_count']})大于本机cpu数量({CPU_COUNT})，性能可能会有所下降")
                    parameter['process_count'] = process_count
                else:
                    logger.info(f"已设置进程池大小为 {parameter['process_count']}")
                    parameter['process_count'] = process_count
    return parameter
