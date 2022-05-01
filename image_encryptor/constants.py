"""
Author       : noeru_desu
Date         : 2021-11-12 16:50:59
LastEditors  : noeru_desu
LastEditTime : 2022-05-01 13:09:09
Description  : 常量
"""
from sys import version as py_ver

from numpy import __version__ as numpy_ver
from PIL import __version__ as pillow_ver
from PIL.Image import (BICUBIC, BILINEAR, BOX, EXTENSION, HAMMING, LANCZOS,
                       NEAREST)
from PIL.Image import init as Pillow_init
from PIL.Image import new
from wx import (ID_CANCEL, ID_HELP, ID_NO, ID_YES, IMAGE_QUALITY_BICUBIC,
                IMAGE_QUALITY_BILINEAR, IMAGE_QUALITY_BOX_AVERAGE,
                IMAGE_QUALITY_HIGH, IMAGE_QUALITY_NEAREST,
                IMAGE_QUALITY_NORMAL, Colour)
from wx import version as wx_ver

try:
    from nuitka.Version import getNuitkaVersion as nuitka_ver
except ImportError:
    nuitka_ver = lambda: '[未安装]'

Pillow_init()

RELEASE = 0
RELEASE_CANDIDATE = 1
DEV = 2
BETA = 3
ALPHA = 4
VERSION_TYPE = RELEASE_CANDIDATE
VERSION_NUMBER = '1.4.1'
SUB_VERSION_NUMBER = 'dev.2'
VERSION_BATCH = '20220501-2'
BRANCH = 'dev/1.x'

OPEN_SOURCE_URL = 'https://github.com/noeru-desu/Image-encryptor'

EXTENSION_KEYS = [i.lstrip('.') for i in EXTENSION.keys()]
EXTENSION_KEYS_STRING = ' '.join(EXTENSION_KEYS)
PIL_RESAMPLING_FILTERS = (NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS)
WX_RESAMPLING_FILTERS = (IMAGE_QUALITY_NEAREST, IMAGE_QUALITY_BOX_AVERAGE, IMAGE_QUALITY_BILINEAR, IMAGE_QUALITY_NORMAL, IMAGE_QUALITY_BICUBIC, IMAGE_QUALITY_HIGH)

DO_NOT_REFRESH = 0
MANUALLY_REFRESH = 1
AUTO_REFRESH = 2
ENCRYPTION_MODE = 0
DECRYPTION_MODE = 1
ANTY_HARMONY_MODE = 2
PREVIEW_IMAGE = 0
ORIG_IMAGE = 1

BLACK_IMAGE = new('RGBA', (1, 1))

OIERR_NOT_EXIST = '文件不存在'
OIERR_UNSUPPORTED_FORMAT = '无法打开或识别图像格式, 或输入了不受支持的格式'
OIERR_EXCEED_LIMIT = '图像像素量超过允许最大像素量'

EA_VERSION = 7
EAERR_NO_DATA = '选择的图像中没有数据'
EAERR_NO_ATTRIBUTES = '选择的图像不包含加密参数, 请确保尝试解密的图像为加密后的原图'
EAERR_DECODE_FAILED = '加载图像加密参数时出现问题, 请确保尝试解密的图像为加密后的原图'
EAERR_INCOMPATIBLE = '该版本不支持0.1.0-BETA版加密器加密的图像'
EAERR_NOT_SUPPORT = '选择的图像文件由更高版本的加密器加密, 请使用最新版的加密器进行解密'

LIGHT_RED = Colour(255, 30, 30)

VERSION_INFO = (
    f'Python {py_ver}',
    f' - wxPython {wx_ver()}',
    f' - Pillow {pillow_ver}',
    f' - Numpy {numpy_ver}',
    f' - Nutika {nuitka_ver()}',
    f'You are using Image encryptor GUI {VERSION_NUMBER}-{SUB_VERSION_NUMBER} (branch: {BRANCH}) (batch: {VERSION_BATCH})',
    f'Open source at {OPEN_SOURCE_URL}'
)


class DialogReturnCodes(object):
    yes = ID_YES
    no = ID_NO
    cancel = ID_CANCEL
    help = ID_HELP
