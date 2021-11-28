'''
Author       : noeru_desu
Date         : 2021-08-28 18:34:08
LastEditors  : noeru_desu
LastEditTime : 2021-11-27 21:31:10
Description  : GUI程序
'''
from multiprocessing import freeze_support
from sys import argv, exit
from warnings import filterwarnings

from image_encryptor.gui.frame.main_frame import MainFrame

filterwarnings('error')


if __name__ == '__main__':
    freeze_support()
    if len(argv) > 1 and argv[1] == '+test':
        exit()
    MainFrame.run()
