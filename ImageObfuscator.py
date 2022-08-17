#! python3.10
"""
Author       : noeru_desu
Date         : 2021-08-28 18:34:08
LastEditors  : noeru_desu
LastEditTime : 2022-08-11 13:28:33
Description  : GUI程序
"""
from multiprocessing import freeze_support
from warnings import filterwarnings

from image_obfuscator.frame.events import MainFrame

filterwarnings('error')


if __name__ == '__main__':
    freeze_support()
    MainFrame.run()