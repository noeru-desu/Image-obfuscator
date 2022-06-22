"""
Author       : noeru_desu
Date         : 2021-09-24 20:05:44
LastEditors  : noeru_desu
LastEditTime : 2022-06-22 11:51:27
Description  : 对低版本加密的图像的加密信息进行转换, 向下兼容
"""
from base64 import b64decode, b85encode
from json import JSONDecodeError, loads
from os.path import getsize
from typing import Callable, Type

from image_encryptor.constants import (EA_VERSION, EAERR_DECODE_FAILED,
                                       EAERR_INCOMPATIBLE, EAERR_NO_ATTRIBUTES,
                                       EAERR_NO_DATA, EAERR_NOT_SUPPORT)



# 1 初始版本
# 2 可开关normal_encryption设置
# 3 细分normal_encryption设置
# 4 可选异或通道，可选异或噪声
# 5 可选随机映射
# 6 动态密码验证字段 (无参数转换)
# 7 加密核心v3 (无参数转换)
# 8 模块化
# 9 ...


def v_1_to_2(data):
    data['normal_encryption'] = True
    return v_2_to_3(data)


def v_2_to_3(data):
    if data['normal_encryption']:
        data['upset'] = True
        data['flip'] = True
    else:
        data['upset'] = False
        data['flip'] = False
        data['rgb_mapping'] = False
    return v_3_to_4(data)


def v_3_to_4(data):
    data['shuffle'] = data['upset']
    data['xor_channels'] = ''
    if data['xor_rgb']:
        data['xor_channels'] += 'rgb'
    if data['xor_alpha']:
        data['xor_channels'] += 'a'
    data['noise_xor'] = False
    data['noise_factor'] = 1
    return v_4_to_5(data)


def v_4_to_5(data):
    data['cutting_row'] = data['row']
    data['cutting_col'] = data['col']
    data['orig_width'] = data['width']
    data['orig_height'] = data['height']
    data['shuffle_chunks'] = data['shuffle']
    data['flip_chunks'] = data['flip']
    data['XOR_channels'] = data['xor_channels']
    data['noise_XOR'] = data['noise_xor']
    data['mapping_channels'] = 'rgb' if data['rgb_mapping'] else ''
    return v_5_to_8(data)


def v_5_to_8(data):
    data['XOR_channels'] = tuple(i in data['XOR_channels'] for i in 'rgba')
    data['mapping_channels'] = tuple(i in data['mapping_channels'] for i in 'rgba')
    if data['has_password']:
        data['password_base85'] = b85encode(b64decode(data['password_base64'].encode())).decode()
    else:
        data['password_base85'] = 0
    return v_8_to_9(data)


def v_8_to_9(data):
    return {
        'corresponding_decryption_mode': 'builtin.decrypt.v1',
        'data': data,
        'version': 9
    }


version_conversion: tuple[Callable[[dict], dict]] = (
    None, v_1_to_2, v_2_to_3, v_3_to_4, v_4_to_5, v_5_to_8, v_5_to_8, v_5_to_8, v_8_to_9
)


def check_version(data: dict):
    version = data.get('version')
    if version is None:
        return None, EAERR_INCOMPATIBLE
    elif version > EA_VERSION:
        return None, EAERR_NOT_SUPPORT
    elif version != EA_VERSION:
        data = version_conversion[version](data)
    return data, None


def load_encryption_attributes(file):
    try:
        last_line = read_last_line(file, b'}')
        if last_line is None:
            return None, EAERR_NO_DATA
        elif not last_line:
            return None, EAERR_NO_ATTRIBUTES
        return check_version(loads(last_line.decode()))
    except UnicodeDecodeError:
        return None, EAERR_NO_ATTRIBUTES
    except JSONDecodeError:
        return None, EAERR_DECODE_FAILED


def read_last_line(file, endswith: bytes = None):
    file_size = getsize(file)
    if file_size == 0:
        return None
    with open(file, 'rb') as f:
        f.seek(-1, 2)
        end = f.read(1)
        if not end:
            return None
        elif endswith is not None and end != endswith:
            return False
        offset = -400
        while True:
            if file_size > -offset:
                f.seek(offset, 2)
                lines = f.readlines()
            else:
                f.seek(0)
                lines = f.readlines()
                if len(lines) < 2:
                    last_line = lines[-1]
                    break
            if len(lines) >= 2:
                last_line = lines[-1]
                break
            else:
                offset -= 25
                if __debug__:
                    print(f'expanded to {offset}')
    return last_line


def gen_encryption_attributes(corresponding_decryption_mode: str, data: str):
    return {
        'corresponding_decryption_mode': corresponding_decryption_mode,
        'data': data,
        'version': EA_VERSION
    }
