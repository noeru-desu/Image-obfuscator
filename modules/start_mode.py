from getopt import getopt, GetoptError
from os.path import isfile


help_msg = """
<filename> [--nm] [-pw password] [-r row] [-c column]

<filename> 图片路径
--nm / --not_mapping 关闭RGB通道映射
--pw password / --password password 密码
-r row / --row row 分割行数
-c column / --col column / --column column 分割列数
-f file_format / --format file_format 指定保存的文件格式
"""


def check_start_mode(argv):
    if not isfile(argv[0]):
        print('没有提供文件或文件不存在')
        exit(2)
    parameter = {
        'path': argv[0],
        'format': 'png',
        'mapping': True,
        'password': 100,
        'row': 25,
        'col': 25
    }
    try:
        opts, args = getopt(argv[1:], "hf:r:c:", ["help", "format=", "pw=", "password=", "row=", "col=", "column=", "nm", "not_mapping"])
    except GetoptError:
        print(help_msg)
        exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_msg)
            exit()
        elif opt in ("-f", "--format"):
            parameter['format'] = arg
        elif opt in ("--nm", "--not_mapping"):
            parameter['mapping'] = False
        elif opt in ("--pw", "--password"):
            parameter['password'] = arg
        elif opt in ("-r", "--row"):
            parameter['row'] = int(arg)
        elif opt in ("-c", "--col", "--column"):
            parameter['col'] = int(arg)
    return parameter
