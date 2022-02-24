"""
Author       : noeru_desu
Date         : 2021-08-30 11:33:06
LastEditors  : noeru_desu
LastEditTime : 2022-02-24 21:15:03
Description  : 粗略包装的AES加密方法
"""
from base64 import decodebytes, encodebytes

from Crypto.Cipher import AES


def _add_16(par, fill=b'\x00'):
    """填充到16的倍数字节"""
    if isinstance(par, str):
        par = par.encode()
    while len(par) % 16 != 0:
        par += fill
    return par


def encrypt(model, key, text, iv=b'0000000000000000', base64=False, output_string=True):
    """
    :description: 使用AES加密信息
    :param model: AES加密模式
    :param key: 密钥
    :param text: 要加密的内容
    :param iv: 偏移量
    :param base64: 是否将加密后的信息进行base64编码
    :param output_string: 是否将base64编码为字符串
    :return 加密后的信息
    """
    if isinstance(text, str):
        text = text.encode()
    key = _add_16(key)
    iv = _add_16(iv, b'0')
    if model == AES.MODE_ECB:
        aes = AES.new(key, model)
    else:
        aes = AES.new(key, model, iv)
    if base64:
        return base64_encode(aes.encrypt(text), output_string).replace('\r', '').replace('\n', '')
    else:
        return aes.encrypt(text)


def decrypt(model, key, text, iv=b'0000000000000000', base64=False, output_string=True):
    """
    :description: 使用AES解密信息
    :param model: AES解密模式
    :param key: 密钥
    :param text: 要解密的内容
    :param iv: 偏移量
    :param base64: 输入的内容是否为base64
    :param output_string: 是否将解密内容编码为字符串
    :return 解密后的信息
    """
    key = _add_16(key)
    iv = _add_16(iv, b'0')
    if base64:
        text = base64_decode(text.replace('\r', '').replace('\n', ''))
        if text is None:
            return None
    if model == AES.MODE_ECB:
        aes = AES.new(key, model)
    else:
        aes = AES.new(key, model, iv)
    if output_string:
        try:
            return aes.decrypt(text).strip(b"\x00").decode()
        except UnicodeDecodeError:
            return None
    else:
        return aes.decrypt(text).strip(b"\x00")


def base64_encode(byt, output_string=True):
    """
    :description: 编码为base64
    :param byt: 要编码的信息
    :param output_string: 是否输出为字符串
    :return: 编码后的信息
    """
    base64 = encodebytes(byt)
    if output_string:
        try:
            base64 = base64.decode()
        except UnicodeDecodeError:
            return None
    return base64


def base64_decode(base64):
    """
    :description: 解码base64
    :param base64: 需要解码的base64内容
    :return: 解码后的信息
    """
    if isinstance(base64, str):
        try:
            base64 = base64.encode()
        except UnicodeEncodeError:
            return None
    base64 = decodebytes(base64)
    return base64
