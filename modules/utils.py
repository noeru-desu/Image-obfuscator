from os import system

from Crypto.Cipher import AES
from win32file import FILE_ATTRIBUTE_NORMAL, GENERIC_READ, INVALID_HANDLE_VALUE, OPEN_EXISTING, CloseHandle, CreateFile

from modules.AES import encrypt
from modules.loader import load_program
from modules.version_adapter import load_encryption_attributes


class fake_bar():
    def update(self, n):
        pass

    def finish(self):
        pass


def pause():
    system('pause>nul')


def is_using(path):
    try:
        vHandle = CreateFile(path, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        if int(vHandle) == INVALID_HANDLE_VALUE:
            return True
        CloseHandle(vHandle)
    except Exception as e:
        print(e)
        return True


def check_password(path, extra_info='', auto_check_password_set: set = None):
    program = load_program()
    image_data = load_encryption_attributes(path)
    if isinstance(image_data, str):
        return image_data, 0
    password = 100
    password_base64 = 0
    auto_check_password_set = set() if auto_check_password_set is None else auto_check_password_set

    if image_data['has_password']:
        password = ''
        '''
        if program.parameters['password'] != 100:
            auto_check_password_set.add(base64, program.parameters['password'])
        '''
        if auto_check_password_set:
            for b, p in auto_check_password_set:
                try:
                    if b == image_data['password_base64']:
                        password = p
                        break
                except UnicodeDecodeError:
                    continue

        if password == '':
            while True:
                password = input(f'{extra_info}需要解密的图片被密码保护，请输入密码：')
                if password == '':
                    continue

                try:
                    password_base64 = encrypt(AES.MODE_CFB, password, 'PASS', base64=True)
                    if password_base64 == image_data['password_base64']:
                        break
                    else:
                        program.logger.warning('密码错误！')
                except UnicodeDecodeError:
                    program.logger.warning('密码错误！')

    image_data['password'] = password
    return image_data, password_base64
