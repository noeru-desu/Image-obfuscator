'''
Author       : noeru_desu
Date         : 2021-08-28 18:34:08
LastEditors  : noeru_desu
LastEditTime : 2021-10-29 23:26:09
Description  : GUI程序
'''
from sys import argv, exit
from warnings import filterwarnings

from image_encryptor.gui.frame.main_frame import MainFrame
from image_encryptor.gui.modules.loader import load_program

filterwarnings('error')


if __name__ == '__main__':
    program = load_program()
    if len(argv) > 1 and argv[1] == '+test':
        exit()
    try:
        MainFrame.run()
    except KeyboardInterrupt:
        if program.thread_pool is not None:
            program.thread_pool.shutdown(wait=False, cancel_futures=True)
        program.logger.error('已强制退出')
