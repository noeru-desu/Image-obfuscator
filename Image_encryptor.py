import modules.bulk_file_decryptor as bulk_decryptor
import modules.bulk_file_encryptor as bulk_encryptor
import modules.single_file_decryptor as single_decryptor
import modules.single_file_encryptor as single_encryptor
from modules.loader import load_program

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
            program.logger.error('已强制退出')
        else:
            print('\n已强制退出')
