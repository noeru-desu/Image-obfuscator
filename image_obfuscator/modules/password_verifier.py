"""
Author       : noeru_desu
Date         : 2021-10-10 10:48:27
LastEditors  : noeru_desu
LastEditTime : 2022-05-27 21:11:21
"""
from Crypto.Cipher import AES

from image_obfuscator.utils.AES import encrypt


class PasswordDict(dict):   # TODO 限制长度
    """修改了的dict"""
    def __init__(self, default_password=None):
        super().__init__()
        self[0] = 100
        if default_password is not None:
            self[self.get_validation_field_base85(default_password)] = default_password
            self[self.get_validation_field_base85(default_password, False)] = default_password

    def get_password(self, base85):
        return self.get(base85)

    @staticmethod
    def get_validation_field_base85(password: str, dynamic_auth=True) -> str:
        """生成用于验证密码正确性的base85"""
        password = password.encode()
        return encrypt(AES.MODE_CFB, password, password if dynamic_auth else b'PASS', base85=True)
