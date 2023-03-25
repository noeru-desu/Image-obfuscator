#! python3.11
"""
Author       : noeru_desu
Date         : 2021-08-28 18:34:08
LastEditors  : noeru_desu
LastEditTime : 2023-03-25 19:34:25
"""
# from multiprocessing import freeze_support
from warnings import filterwarnings

from image_obfuscator.frame.events import MainFrame

filterwarnings('error')


if __name__ == '__main__':
    # freeze_support()
    MainFrame.run()
