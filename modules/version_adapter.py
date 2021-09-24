from json import JSONDecodeError, loads
from traceback import print_exc

from .loader import get_instances
from .utils import pause

program = get_instances()


def check_version(data):
    if 'version' not in data:
        program.logger.error('该版本不支持0.1.0-BETA版加密器加密的图片')
        pause()
        exit()
    if data['version'] > 1:
        program.logger.error('选择的图片文件由更高版本的加密器加密，请使用最新版的解密器进行解密')
        pause()
        exit()
    return data


def load_encryption_attributes():
    data = None
    with open(program.parameter['path'], 'rb') as f:
        offset = -35
        while True:
            f.seek(offset, 2)
            lines = f.readlines()
            if len(lines) >= 2:
                last_line = lines[-1]
                break
            offset *= 2
        data = last_line.decode()
    try:
        return check_version(loads(data))
    except JSONDecodeError:
        program.logger.error('加载图片加密参数时出现问题，请确保此图片使用本程序加密，且尝试解密的图片为加密后的原图')
        pause()
        exit()
    except Exception:
        program.logger.error('出现意外错误：')
        print_exc()
        pause()
        exit()
