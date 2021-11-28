'''
Author       : noeru_desu
Date         : 2021-09-24 20:05:44
LastEditors  : noeru_desu
LastEditTime : 2021-11-28 14:37:08
Description  : 对低版本加密的图片的加密信息进行转换，向下兼容
'''
from json import JSONDecodeError, loads
from os.path import getsize


def v_1_to_2(data):
    data['normal_encryption'] = True
    data['version'] = 2
    return v_2_to_3(data)


def v_2_to_3(data):
    if data['normal_encryption']:
        data['upset'] = True
        data['flip'] = True
    else:
        data['upset'] = False
        data['flip'] = False
        data['rgb_mapping'] = False
    data['version'] = 3
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
    data['version'] = 4
    return data


def check_version(data):
    if 'version' not in data:
        return None, '该版本不支持0.1.0-BETA版加密器加密的图片'
    elif data['version'] > 4:
        return None, '选择的图片文件由更高版本的加密器加密，请使用最新版的加密器进行解密'
    if data['version'] == 1:
        data = v_1_to_2(data)
    elif data['version'] == 2:
        data = v_2_to_3(data)
    elif data['version'] == 3:
        data = v_3_to_4(data)
    return data, None


def get_encryption_parameters(original_width, original_height, parameters, has_password, password_base64):
    return {
        'version': 4,
        'width': original_width,
        'height': original_height,
        'col': parameters['col'],
        'row': parameters['row'],
        'shuffle': parameters['shuffle'],
        'flip': parameters['flip'],
        'rgb_mapping': parameters['rgb_mapping'],
        'xor_channels': parameters['xor_channels'],
        'noise_xor': parameters['noise_xor'],
        'noise_factor': parameters['noise_factor'],
        'has_password': has_password,
        'password_base64': password_base64
    }


def load_encryption_attributes(file):
    data = None
    last_line = read_last_line(file)
    if last_line is None:
        return '选择的图片中没有数据'
    try:
        data = last_line.decode()
        return check_version(loads(data))
    except UnicodeDecodeError:
        return None, '选择的图片不包含加密参数，请确保尝试解密的图片为加密后的原图'
    except JSONDecodeError:
        return None, '加载图片加密参数时出现问题，请确保尝试解密的图片为加密后的原图'
    except Exception as e:
        return None, repr(e)


def read_last_line(file):
    file_size = getsize(file)
    if file_size == 0:
        return None
    with open(file, 'rb') as f:
        offset = -35
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
                offset *= 2
    return last_line
