'''
Author       : noeru_desu
Date         : 2021-10-10 10:48:27
LastEditors  : noeru_desu
LastEditTime : 2021-10-10 11:32:15
Description  : 粗略包装的密码验证器
'''

from Crypto.Cipher import AES
from image_encryptor.modules.version_adapter import load_encryption_attributes
from image_encryptor.utils.AES import encrypt


class PasswordSet(set):
    def __init__(self, default_password=None):
        super(PasswordSet, self).__init__()
        self.add(self.get_validation_field_base64(default_password), default_password)

    def get_password_in_set(self, correct_base64):
        for base64, password in self:
            if base64 == correct_base64:
                return password
        return None

    @staticmethod
    def get_validation_field_base64(password):
        return encrypt(AES.MODE_CFB, password, 'PASS', base64=True)


def get_image_data(file, extra_info='', password_set: PasswordSet = None):
    image_data, error = load_encryption_attributes(file)
    if error is not None:
        return None, error
    check_password = True
    password = 100
    password_base64 = 0

    if image_data['has_password']:
        if password_set is not None:
            password = password_set.get_password_in_set(image_data['password_base64'])
            if password is not None:
                check_password = False

        if check_password:
            while True:
                password = input(f'{extra_info}需要解密的图片被密码保护，请输入密码：\n')
                if password == '':
                    continue

                password_base64 = PasswordSet.get_validation_field_base64(password)
                if password_base64 is not None and password_base64 == image_data['password_base64']:
                    if password_set is not None:
                        password_set.add((password_base64, password))
                    break
                else:
                    print('密码错误！', end='')

    image_data['password'] = password
    return image_data, None
