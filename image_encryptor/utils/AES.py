"""
Author       : noeru_desu
Date         : 2021-08-30 11:33:06
LastEditors  : noeru_desu
LastEditTime : 2022-05-22 09:52:06
Description  : 粗略包装的AES加密方法
"""
from base64 import b85encode, b85decode

from Crypto.Cipher import AES


def _auto_fill(par: bytes, fill=b'\x00'):
    """长度小于16时填充至16字节, 大于时填充至8的倍数字节"""
    length = len(par)
    if length < 16:
        par += fill * (16 - length)
    elif length % 8 != 0:
         par += fill * ((length // 8 + 1) * 8 - length)
    return par


def encrypt(model, key: bytes, text: bytes, iv=b'0000000000000000', base85=False, output_string=True):
    """
    :description: 使用AES加密信息
    :param model: AES加密模式
    :param key: 密钥
    :param text: 要加密的内容
    :param iv: 偏移量
    :param base8564: 是否将加密后的信息进行base85编码
    :param output_string: 是否将base85编码为字符串
    :return 加密后的信息
    """
    if len(key) > 32:
        raise ValueError('key must be 16, 24 or 32 bytes long.')
    key = _auto_fill(key)
    if len(iv) > 16:
        raise ValueError('iv must be 16 bytes long.')
    iv = _auto_fill(iv, b'0')
    aes = AES.new(key, model) if model == AES.MODE_ECB else AES.new(key, model, iv)
    if base85:
        return base85_encode(aes.encrypt(text), output_string).replace('\r', '').replace('\n', '')
    else:
        return aes.encrypt(text)


def decrypt(model, key: bytes, text: bytes, iv=b'0000000000000000', base85=False, output_string=True):
    """
    :description: 使用AES解密信息
    :param model: AES解密模式
    :param key: 密钥
    :param text: 要解密的内容
    :param iv: 偏移量
    :param base85: 输入的内容是否为base85
    :param output_string: 是否将解密内容编码为字符串
    :return 解密后的信息
    """
    if len(key) > 32:
        raise ValueError('key must be 16, 24 or 32 bytes long.')
    key = _auto_fill(key)
    if len(iv) > 16:
        raise ValueError('iv must be 16 bytes long.')
    iv = _auto_fill(iv, b'0')
    if base85:
        text = base85_decode(text.replace('\r', '').replace('\n', ''))
        if text is None:
            return None
    aes = AES.new(key, model) if model == AES.MODE_ECB else AES.new(key, model, iv)
    if not output_string:
        return aes.decrypt(text).strip(b"\x00")
    try:
        return aes.decrypt(text).strip(b"\x00").decode()
    except UnicodeDecodeError:
        return None


def base85_encode(byt, output_string=True):
    """
    :description: 编码为base85
    :param byt: 要编码的信息
    :param output_string: 是否输出为字符串
    :return: 编码后的信息
    """
    base85 = b85encode(byt)
    if output_string:
        try:
            base85 = base85.decode()
        except UnicodeDecodeError:
            return None
    return base85


def base85_decode(base85):
    """
    :description: 解码base85
    :param base85: 需要解码的base85内容
    :return: 解码后的信息
    """
    if isinstance(base85, str):
        try:
            base85 = base85.encode()
        except UnicodeEncodeError:
            return None
    base85 = b85decode(base85)
    return base85
