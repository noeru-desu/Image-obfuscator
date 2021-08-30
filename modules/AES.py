from base64 import decodebytes, encodebytes

from Crypto.Cipher import AES


def _add_16(par, fill=b'\x00'):
    if isinstance(par, str):
        par = par.encode()
    while len(par) % 16 != 0:
        par += fill
    return par


def encrypt(model, key, text, iv=b'0000000000000000', base64=False, base64_output_string=True):
    if isinstance(text, str):
        text = text.encode()
    key = _add_16(key)
    iv = _add_16(iv, b'0')
    if model == AES.MODE_ECB:
        aes = AES.new(key, model)
    else:
        aes = AES.new(key, model, iv)
    if base64:
        return base64_encode(aes.encrypt(text), base64_output_string).replace('\r', '').replace('\n', '')
    else:
        return aes.encrypt(text)


def decrypt(model, key, text, iv=b'0000000000000000', base64=False, output_string=True):
    key = _add_16(key)
    iv = _add_16(iv, b'0')
    if base64:
        text = base64_decode(text.replace('\r', '').replace('\n', ''))
    if model == AES.MODE_ECB:
        aes = AES.new(key, model)
    else:
        aes = AES.new(key, model, iv)
    if output_string:
        return aes.decrypt(text).strip(b"\x00").decode()
    else:
        return aes.decrypt(text).strip(b"\x00")


def base64_encode(byt, output_string=True):
    base64 = encodebytes(byt)
    if output_string:
        base64 = base64.decode()
    return base64


def base64_decode(base64):
    if isinstance(base64, str):
        base64 = base64.encode()
    base64 = decodebytes(base64)
    return base64
