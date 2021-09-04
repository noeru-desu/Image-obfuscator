from getopt import GetoptError, getopt
from os.path import isfile
from sys import exit

help_msg = """
<filename> [--nm] [-pw password] [-r row] [-c column] [-f file_format]

<filename> 图片路径
可选参数：
--nm / --not_mapping 关闭RGB随机映射
--xa / --xor_alpha 在异或加密图像时将透明度也进行异或
--pw password / --password password 密码
-r row / --row row 分割行数
-c column / --col column / --column column 分割列数
-f file_format / --format file_format 指定保存的文件格式
"""


def check_start_mode(logger, argv):
    if not argv or argv[0] in ("-h", "--help"):
        logger.info(help_msg)
        exit()
    elif not isfile(argv[0]):
        logger.warning('没有提供文件或文件不存在')
        exit(2)
    parameter = {
        'path': argv[0],
        'format': 'png',
        'mapping': True,
        'xor_alpha': False,
        'password': 100,
        'row': 25,
        'col': 25
    }
    try:
        opts, args = getopt(argv[1:], "hf:r:c:", ["help", "format=", "pw=", "password=", "row=", "col=", "column=", "nm", "not_mapping", "xa", "xor_alpha"])
    except GetoptError:
        logger.warning(help_msg)
        exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            logger.info(help_msg)
            exit()
        elif opt in ("-f", "--format"):
            logger.info(f'指定保存格式为 {arg}')
            parameter['format'] = arg
        elif opt in ("--nm", "--not_mapping"):
            logger.info('已关闭RGB随机映射')
            parameter['mapping'] = False
        elif opt in ("--xa", "--xor_alpha"):
            logger.info('已启用透明通道异或加密')
            parameter['xor_alpha'] = True
        elif opt in ("--pw", "--password"):
            logger.info(f'已设置密码为 {arg}')
            parameter['password'] = arg
        elif opt in ("-r", "--row"):
            logger.info(f'已指定切割行数为 {arg}')
            parameter['row'] = int(arg)
        elif opt in ("-c", "--col", "--column"):
            logger.info(f'已指定切割行列数为 {arg}')
            parameter['col'] = int(arg)
    return parameter
