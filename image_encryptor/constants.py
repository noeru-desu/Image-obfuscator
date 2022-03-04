"""
Author       : noeru_desu
Date         : 2021-11-12 16:50:59
LastEditors  : noeru_desu
LastEditTime : 2022-03-04 20:06:07
Description  : 常量
"""
from PIL.Image import init as PIL_init
from PIL.Image import EXTENSION, NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS, new

PIL_init()

RELEASE = 0
RELEASE_CANDIDATE = 1
DEV = 2
BETA = 3
ALPHA = 4
VERSION_TYPE = DEV
VERSION_NUMBER = '1.2.2'
SUB_VERSION_NUMBER = 'dev'
VERSION_BATCH = '20220304-1'
BRANCH = 'dev/1.x'

OPEN_SOURCE_URL = 'https://github.com/noeru-desu/Image-encryptor'

EXTENSION_KEYS = [i.lstrip('.') for i in EXTENSION.keys()]
EXTENSION_KEYS_STRING = ' '.join(i for i in EXTENSION_KEYS)
RESAMPLING_FILTERS = (NEAREST, BOX, BILINEAR, HAMMING, BICUBIC, LANCZOS)

DO_NOT_REFRESH = 0
MANUAL_REFRESH = 1
AUTO_REFRESH = 2
ENCRYPTION_MODE = 0
DECRYPTION_MODE = 1
ANTY_HARMONY_MODE = 2
PREVIEW_IMAGE = 0
ORIG_IMAGE = 1

BLACK_IMAGE = new('RGBA', (1, 1))

OIERR_NOT_EXIST = '文件不存在'
OIERR_UNSUPPORTED_FORMAT = '无法打开或识别图像格式, 或输入了不受支持的格式'
OIERR_EXCEED_LIMIT = '图片像素量超过允许最大像素量'

EAERR_NO_DATA = '选择的图片中没有数据'
EAERR_NO_ATTRIBUTES = '选择的图片不包含加密参数, 请确保尝试解密的图片为加密后的原图'
EAERR_DECODE_FAILED = '加载图片加密参数时出现问题, 请确保尝试解密的图片为加密后的原图'
EAERR_INCOMPATIBLE = '该版本不支持0.1.0-BETA版加密器加密的图片'
EAERR_NOT_SUPPORT = '选择的图片文件由更高版本的加密器加密, 请使用最新版的加密器进行解密'
