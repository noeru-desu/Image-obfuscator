'''
Author       : noeru_desu
Date         : 2021-10-10 10:48:27
LastEditors  : noeru_desu
LastEditTime : 2021-11-21 16:40:28
Description  : 粗略包装的密码验证器
'''

from Crypto.Cipher import AES
from image_encryptor.common.utils.AES import encrypt


class PasswordDict(dict):
    '''修改了的dict'''
    def __init__(self, default_password=None):
        super().__init__()
        self[0] = 100
        if default_password is not None:
            self[self.get_validation_field_base64(default_password)] = default_password

    @staticmethod
    def get_validation_field_base64(password):
        """生成用于验证密码正确性的base64"""
        return encrypt(AES.MODE_CFB, password, 'PASS', base64=True)
