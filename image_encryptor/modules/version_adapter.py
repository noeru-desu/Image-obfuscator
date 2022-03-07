"""
Author       : noeru_desu
Date         : 2021-09-24 20:05:44
LastEditors  : noeru_desu
LastEditTime : 2022-03-07 09:46:37
Description  : 对低版本加密的图片的加密信息进行转换, 向下兼容
"""
from json import JSONDecodeError, loads
from os.path import getsize

from image_encryptor.constants import EA_VERSION, EAERR_NO_DATA, EAERR_NO_ATTRIBUTES, EAERR_DECODE_FAILED, EAERR_INCOMPATIBLE, EAERR_NOT_SUPPORT


# 1 初始版本
# 2 可开关normal_encryption设置
# 3 细分normal_encryption设置
# 4 可选异或通道，可选异或噪声
# 5 可选随机映射
# 6 动态密码验证字段 (无参数转换)
# 7 加密核心v3 (无参数转换)
# 8 ...


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
    return data


def v_5_to_8(data):
    ...


def check_version(data):
    if 'version' not in data:
        return None, EAERR_INCOMPATIBLE
    elif data['version'] > EA_VERSION:
        return None, EAERR_NOT_SUPPORT
    if data['version'] == 1:
        data = v_1_to_2(data)
    elif data['version'] == 2:
        data = v_2_to_3(data)
    elif data['version'] == 3:
        data = v_3_to_4(data)
    elif data['version'] == 4:
        data = v_4_to_5(data)
    return data, None


def load_encryption_attributes(file):
    data = None
    last_line = read_last_line(file)
    if last_line is None:
        return None, EAERR_NO_DATA
    try:
        data = last_line.decode()
        return check_version(loads(data))
    except UnicodeDecodeError:
        return None, EAERR_NO_ATTRIBUTES
    except JSONDecodeError:
        return None, EAERR_DECODE_FAILED


def read_last_line(file):
    file_size = getsize(file)
    if file_size == 0:
        return None
    with open(file, 'rb') as f:
        offset = -300
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
    return last_line
