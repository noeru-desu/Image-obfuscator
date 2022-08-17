"""
Author       : noeru_desu
Date         : 2021-11-12 16:50:59
LastEditors  : noeru_desu
LastEditTime : 2022-08-17 19:40:58
Description  : 常量
"""
from platform import machine, platform
from sys import version as py_ver

from numpy import __version__ as numpy_ver
from PIL import __version__ as pillow_ver
from PIL.Image import (BICUBIC, BILINEAR, BOX, EXTENSION, HAMMING, LANCZOS,
                       NEAREST)
from PIL.Image import init as Pillow_init
from PIL.Image import new
from wx import (ID_CANCEL, ID_HELP, ID_NO, ID_OK, ID_YES,
                IMAGE_QUALITY_BICUBIC, IMAGE_QUALITY_BILINEAR,
                IMAGE_QUALITY_BOX_AVERAGE, IMAGE_QUALITY_HIGH,
                IMAGE_QUALITY_NEAREST, IMAGE_QUALITY_NORMAL,
                VERTICAL, HORIZONTAL, Colour)
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
VERSION_TYPE = RELEASE
VERSION = '2.1.1'
PRE_RELEASE_VERSION = 'release'
BATCH = '20220817a'
BUILD_METADATA = 'build.1' # 'build.1' / BATCH
COMPILED = True
BRANCH = 'dev/2.x'

OPEN_SOURCE_URL = 'https://github.com/noeru-desu/Image-obfuscator'

EXTENSION_KEYS = [i.lstrip('.') for i in EXTENSION.keys()]
EXTENSION_KEYS_STRING = ' '.join(EXTENSION_KEYS)
LOSSY_FORMATS = (
    'jpg', 'jpeg', 'wmf', 'webp'
)
PIL_RESAMPLING_FILTERS = (NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS)
WX_RESAMPLING_FILTERS = (IMAGE_QUALITY_NEAREST, IMAGE_QUALITY_BOX_AVERAGE, IMAGE_QUALITY_BILINEAR, IMAGE_QUALITY_NORMAL, IMAGE_QUALITY_BICUBIC, IMAGE_QUALITY_HIGH)

DO_NOT_REFRESH = 0
MANUALLY_REFRESH = 1
AUTO_REFRESH = 2
PREVIEW_IMAGE = 0
ORIG_IMAGE = 1

BLACK_IMAGE = new('RGBA', (1, 1))

# OpenImage
OIERR_NOT_EXIST = '文件不存在'
OIERR_UNSUPPORTED_FORMAT = '{}是无法打开/识别或不受支持的图像格式, 已跳过加载此文件'
OIERR_EXCEED_LIMIT = '图像像素量超过允许最大像素量'
OIERR_OS_ERROR = '''OSError: {}
常见错误原因:
Permission denied - 权限不足
Truncated File Read - 无法忽略的图像截断(图像损坏或格式错误/格式版本不受支持)'''

# EncryptionAttributes
EA_VERSION = 9
EAERR_NO_DATA = '选择的图像中没有数据'
EAERR_NO_ATTRIBUTES = '选择的图像不包含加密参数, 请确保尝试解密的图像为加密后的原图'
EAERR_DECODE_FAILED = '加载图像加密参数时出现问题, 请确保尝试解密的图像为加密后的原图'
EAERR_INCOMPATIBLE = '该版本不支持解密0.1.0-BETA版混淆器加密的图像'
EAERR_NOT_SUPPORT = '选择的图像文件由更高版本的混淆器加密, 请使用最新版的混淆器进行解密'

FRAME_SETTINGS_MAIN_VERSION = 1
FRAME_SETTINGS_SUB_VERSION = 3

LIGHT_RED = Colour(255, 30, 30)

_BUILD_METADATA = BUILD_METADATA if COMPILED else BATCH

VERSION_INFO = (
    f'{machine()}-{platform()}',
    f'Python {py_ver}',
    f' - wxPython {wx_ver()}',
    f' - Pillow {pillow_ver}',
    f' - Numpy {numpy_ver}',
    f' - Nutika {nuitka_ver()}',
    f'You are using Image Obfuscator GUI {VERSION}-{PRE_RELEASE_VERSION}+{_BUILD_METADATA} (branch: {BRANCH})',
    f'Open source at {OPEN_SOURCE_URL}'
)

FULL_VERSION_STRING = f'{VERSION}-{PRE_RELEASE_VERSION}+{_BUILD_METADATA} (branch: {BRANCH}) {"[Not optimized]" if __debug__ else ""}'
SHORT_VERSION_STRING = f'{VERSION} {"[Not optimized]" if __debug__ else ""}'


class DialogReturnCodes(object):
    ok = ID_OK
    yes = ID_YES
    no = ID_NO
    cancel = ID_CANCEL
    help = ID_HELP


class Orientations(object):
    vertical = VERTICAL
    horizontal = HORIZONTAL
