'''
Author       : noeru_desu
Date         : 2021-09-24 20:05:44
LastEditors  : noeru_desu
LastEditTime : 2021-10-06 07:18:50
Description  : 对低版本加密的图片的加密信息进行转换，向下兼容
'''
from json import JSONDecodeError, loads
from os.path import getsize


def check_version(data):
    if isinstance(data, str):
        return data
    if 'version' not in data:
        return '该版本不支持0.1.0-BETA版加密器加密的图片'
    if data['version'] > 1:
        return '选择的图片文件由更高版本的加密器加密，请使用最新版的解密器进行解密'
    return data


def load_encryption_attributes(path):
    data = None
    size = getsize(path)
    with open(path, 'rb') as f:
        offset = -35
        while True:
            if size > -offset:
                f.seek(offset, 2)
            else:
                f.seek(0)
            lines = f.readlines()
            if len(lines) >= 2:
                last_line = lines[-1]
                break
            offset *= 2
    try:
        data = last_line.decode()
        return check_version(loads(data))
    except UnicodeDecodeError:
        return '选择的图片不包含加密参数，请确保尝试解密的图片为加密后的原图'
    except JSONDecodeError:
        return '加载图片加密参数时出现问题，请确保尝试解密的图片为加密后的原图'
    except Exception as e:
        return repr(e)
