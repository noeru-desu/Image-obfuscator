'''
Author       : noeru_desu
Date         : 2021-08-28 18:35:58
LastEditors  : noeru_desu
LastEditTime : 2021-10-06 07:17:53
Description  : 参数解析器
'''
from getopt import GetoptError, getopt
from multiprocessing import cpu_count
from os.path import isdir, isfile, normpath, split
from sys import exit

from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init

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


def parsing_parameters(logger, argv):
    if not argv or argv[0] in ('-h', '--help'):
        logger.info(help_msg)
        exit()
    CPU_COUNT = cpu_count()
    file_path = normpath(argv[0])
    path = split(file_path)[0]
    if len(argv) == 1 or argv[1].startswith('-'):
        save_path = path
        skip_argv = 1
    else:
        save_path = normpath(argv[1].format(file_path=path))
        skip_argv = 2
    parameter = {
        'loop': False,
        'mode': None,
        'type': None,
        'topdown': False,
        'path': file_path,
        'save_path': save_path,
        'format': None,
        'mapping': False,
        'xor_rgb': False,
        'xor_alpha': False,
        'password': 100,
        'row': 25,
        'col': 25,
        'process_count': 1 if CPU_COUNT < 3 else CPU_COUNT - 2,
        'debug': False
    }
    if isfile(file_path):
        parameter['type'] = 'f'
    elif isdir(file_path):
        if skip_argv == 1:
            parameter['save_path'] = save_path = file_path
        parameter['type'] = 'd'
    else:
        logger.error('没有提供文件或文件不存在')
        exit(2)
    if not isdir(save_path):
        logger.error('提供的保存位置不是文件夹或文件夹不存在')
        exit(2)
    if not EXTENSION:
        PIL_init()
    try:
        opts, args = getopt(argv[skip_argv:], 'hledtf:r:c:x:', ['help', 'loop', 'encrypt', 'decrypt', 'topdown', 'format=', 'pw=', 'password=', 'row=', 'col=', 'column=', 'rm', 'rgb-mapping', 'xor=', 'pc=', 'process-count=', 'debug'])
    except GetoptError as e:
        logger.error(f'未知的参数：{e.opt}')
        logger.info(help_msg)
        exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            logger.info(help_msg)
            exit()
        elif opt in ('-l', '--loop'):
            parameter['loop'] = True
        elif opt in ('-e', '--encrypt'):
            parameter['mode'] = 'e'
        elif opt in ('-d', '--decrypt'):
            parameter['mode'] = 'd'
        elif opt in ('-t', '--topdown'):
            parameter['topdown'] = True
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
        elif opt == '--debug':
            logger.info('已启用调试模式')
            parameter['debug'] = True
    return parameter
