from os import system

from Crypto.Cipher import AES

from modules.AES import decrypt
from modules.loader import load_program
from modules.version_adapter import load_encryption_attributes


class fake_bar():
    def update(self, n):
        pass

    def finish(self):
        pass


def pause():
    system('pause>nul')


def check_password(path, extra_info='', auto_check_password_set: set = None):
    program = load_program()
    image_data = load_encryption_attributes(path)
    if isinstance(image_data, str):
        return image_data
    password = 100
    auto_check_password_set = {} if auto_check_password_set is None else auto_check_password_set

    if image_data['has_password']:
        password = ''
        if program.parameters['password'] != 100:
            auto_check_password_set.add(program.parameters['password'])

        if auto_check_password_set:
            for i in auto_check_password_set:
                try:
                    if decrypt(AES.MODE_CFB, i, image_data['password_base64'], str(image_data['width']) + str(image_data['height']), True) == 'PASS':
                        password = i
                        break
                except UnicodeDecodeError:
                    continue

        if password == '':
            while True:
                password = input(f'{extra_info}需要解密的图片被密码保护，请输入密码：')
                if password == '':
                    continue

                try:
                    if decrypt(AES.MODE_CFB, password, image_data['password_base64'], str(image_data['width']) + str(image_data['height']), True) == 'PASS':
                        break
                    else:
                        program.logger.warning('密码错误！')
                except UnicodeDecodeError:
                    program.logger.warning('密码错误！')

    image_data['password'] = password
    return image_data
