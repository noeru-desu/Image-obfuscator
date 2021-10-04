from warnings import filterwarnings

import image_encryptor.programs.bulk_file_decryptor as bulk_decryptor
import image_encryptor.programs.bulk_file_encryptor as bulk_encryptor
import image_encryptor.programs.single_file_decryptor as single_decryptor
import image_encryptor.programs.single_file_encryptor as single_encryptor
from image_encryptor.modules.loader import load_program, reload_program

filterwarnings('error')


def main(program):
    if program.parameters['mode'] == 'e':
        if program.parameters['type'] == 'f':
            single_encryptor.main()
        else:
            bulk_encryptor.main()
    else:
        if program.parameters['type'] == 'f':
            single_decryptor.main()
        else:
            bulk_decryptor.main()
    return not program.parameters['loop']


if __name__ == '__main__':
    program = None
    try:
        program = load_program()
        while True:
            if main(program):
                break
            program.logger.info('操作完毕，进行循环')
            while True:
                user_input = input('请输入下次循环使用的参数(不输入直接回车退出程序)：\n')
                if not user_input:
                    program.logger.info('已退出')
                    exit()
                user_input = user_input.split(' ')
                try:
                    program = reload_program(parameters=user_input, auto_set=True)
                except SystemExit:
                    continue
                program.parameters['loop'] = True
                break
    except KeyboardInterrupt:
        if program:
            if program.process_pool is not None:
                program.process_pool.shutdown(wait=False, cancel_futures=True)
            program.logger.error('已强制退出')
            program.logger.error('有几率出现图片未被完全写入完毕的情况，导致图片有一部分为黑色或透明')
        else:
            print('\n已强制退出')
