"""
Author       : noeru_desu
Date         : 2021-08-30 11:33:06
LastEditors  : noeru_desu
LastEditTime : 2022-03-06 16:39:49
Description  : 粗略包装的AES加密方法
"""
from base64 import decodebytes, encodebytes

from Crypto.Cipher import AES


def _auto_fill(par: bytes, fill=b'\x00'):
    """长度小于16时填充至16字节, 大于时填充至8的倍数字节"""
    if len(par) == 16:
        return par
    elif len(par) < 16:
        par += fill * (16 - len(par))
    else:
        par += fill * (len(par) % 8)
    return par


def encrypt(model, key: bytes, text: bytes, iv=b'0000000000000000', base64=False, output_string=True):
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
    if len(key) > 32:
        raise ValueError('key must be 16, 24 or 32 bytes long.')
    key = _auto_fill(key)
    if len(iv) > 16:
        raise ValueError('iv must be 16 bytes long.')
    iv = _auto_fill(iv, b'0')
    aes = AES.new(key, model) if model == AES.MODE_ECB else AES.new(key, model, iv)
    if base64:
        return base64_encode(aes.encrypt(text), output_string).replace('\r', '').replace('\n', '')
    else:
        return aes.encrypt(text)


def decrypt(model, key: bytes, text: bytes, iv=b'0000000000000000', base64=False, output_string=True):
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
    if len(key) > 32:
        raise ValueError('key must be 16, 24 or 32 bytes long.')
    key = _auto_fill(key)
    if len(iv) > 16:
        raise ValueError('iv must be 16 bytes long.')
    iv = _auto_fill(iv, b'0')
    if base64:
        text = base64_decode(text.replace('\r', '').replace('\n', ''))
        if text is None:
            return None
    aes = AES.new(key, model) if model == AES.MODE_ECB else AES.new(key, model, iv)
    if not output_string:
        return aes.decrypt(text).strip(b"\x00")
    try:
        return aes.decrypt(text).strip(b"\x00").decode()
    except UnicodeDecodeError:
        return None


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
