"""
Author       : noeru_desu
Date         : 2021-11-12 16:50:59
LastEditors  : noeru_desu
LastEditTime : 2022-02-27 14:14:00
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
VERSION_TYPE = RELEASE
VERSION_NUMBER = '1.2.0'
SUB_VERSION_NUMBER = 'release'
VERSION_BATCH = '20220227-1'
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
