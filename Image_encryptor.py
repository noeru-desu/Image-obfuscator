from warnings import filterwarnings

import image_encryptor.programs.bulk_file_decryptor as bulk_decryptor
import image_encryptor.programs.bulk_file_encryptor as bulk_encryptor
import image_encryptor.programs.single_file_decryptor as single_decryptor
import image_encryptor.programs.single_file_encryptor as single_encryptor
from image_encryptor.modules.loader import load_program

filterwarnings('error')

if __name__ == '__main__':
    program = None
    try:
        program = load_program()
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
    except KeyboardInterrupt:
        if program:
            program.process_pool.shutdown(wait=False, cancel_futures=True)
            program.logger.error('已强制退出')
            program.logger.error('有几率出现图片未被完全写入完毕的情况，导致图片有一部分为黑色或透明')
        else:
            print('\n已强制退出')
