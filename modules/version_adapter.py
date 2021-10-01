from json import JSONDecodeError, loads


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
    with open(path, 'rb') as f:
        offset = -35
        while True:
            f.seek(offset, 2)
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
