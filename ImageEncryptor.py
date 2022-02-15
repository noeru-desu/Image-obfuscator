#! python3.10
"""
Author       : noeru_desu
Date         : 2021-08-28 18:34:08
LastEditors  : noeru_desu
LastEditTime : 2022-02-15 09:46:27
Description  : GUI程序
"""
from sys import exit
from multiprocessing import freeze_support
from warnings import filterwarnings

from image_encryptor.frame.events import MainFrame
from image_encryptor.modules.argparse import Arguments

filterwarnings('error')


if __name__ == '__main__':
    freeze_support()
    startup_parameters = Arguments().parse_args()
    if startup_parameters.test:
        exit()
    MainFrame.run(startup_parameters)
