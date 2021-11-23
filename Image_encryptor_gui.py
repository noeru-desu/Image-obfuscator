'''
Author       : noeru_desu
Date         : 2021-08-28 18:34:08
LastEditors  : noeru_desu
LastEditTime : 2021-11-23 21:20:28
Description  : GUI程序
'''
from multiprocessing import freeze_support
from sys import argv, exit
from warnings import filterwarnings

from image_encryptor.gui.frame.main_frame import MainFrame
from image_encryptor.gui.modules.loader import load_program

filterwarnings('error')


if __name__ == '__main__':
    freeze_support()
    program = load_program()
    if len(argv) > 1 and argv[1] == '+test':
        exit()
    MainFrame.run()
