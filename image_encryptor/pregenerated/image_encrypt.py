"""
Author       : noeru_desu
Date         : 2022-04-04 10:35:30
LastEditors  : noeru_desu
LastEditTime : 2022-04-06 21:04:36
Description  : 预生成的加密相关函数
"""
from typing import TYPE_CHECKING

from PIL.Image import FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM

# from image_encryptor.modules.image import obverse_mapping, reverse_mapping

if TYPE_CHECKING:
    from typing import Any, Callable
    from PIL.Image import Image
    from numpy import ndarray


class MappingFuncV1(object):
    encrypt: 'tuple[Callable[[Any, Any, Any, Any], tuple]]' = (
        lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (g, r, b, a),
        lambda r, g, b, a: (b, g, r, a), lambda r, g, b, a: (g, b, r, a)
    )

    decrypt: 'tuple[Callable[[Any, Any, Any, Any], tuple]]' = (
        lambda r, g, b, a: (g, b, r, a), lambda r, g, b, a: (g, r, b, a),
        lambda r, g, b, a: (b, g, r, a), lambda r, g, b, a: (b, r, g, a)
    )

    index_list = [1, 2, 3, 0]


class MappingFuncV2(object):
    encrypt: 'dict[str, Callable[[Any, Any, Any, Any], tuple]]' = {
        'r': None, 'g': None, 'b': None, 'a': None,
        'rg': (lambda r, g, b, a: (g, r, b, a),), 'rb': (lambda r, g, b, a: (b, g, r, a),),
        'ra': (lambda r, g, b, a: (a, g, b, r),), 'gb': (lambda r, g, b, a: (r, b, g, a),),
        'ga': (lambda r, g, b, a: (r, a, b, g),), 'ba': (lambda r, g, b, a: (r, g, a, b),),
        'rgb': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, b, g, a), lambda r, g, b, a: (g, r, b, a),
            lambda r, g, b, a: (g, b, r, a), lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (b, g, r, a)
        ),
        'rga': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, a, b, g), lambda r, g, b, a: (g, r, b, a),
            lambda r, g, b, a: (g, a, b, r), lambda r, g, b, a: (a, r, b, g), lambda r, g, b, a: (a, g, b, r)
        ),
        'rba': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (b, g, r, a),
            lambda r, g, b, a: (b, g, a, r), lambda r, g, b, a: (a, g, r, b), lambda r, g, b, a: (a, g, b, r)
        ),
        'gba': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (r, b, g, a),
            lambda r, g, b, a: (r, b, a, g), lambda r, g, b, a: (r, a, g, b), lambda r, g, b, a: (r, a, b, g)
        ),
        'rgba': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (r, b, g, a),
            lambda r, g, b, a: (r, b, a, g), lambda r, g, b, a: (r, a, g, b), lambda r, g, b, a: (r, a, b, g),
            lambda r, g, b, a: (g, r, b, a), lambda r, g, b, a: (g, r, a, b), lambda r, g, b, a: (g, b, r, a),
            lambda r, g, b, a: (g, b, a, r), lambda r, g, b, a: (g, a, r, b), lambda r, g, b, a: (g, a, b, r),
            lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (b, r, a, g), lambda r, g, b, a: (b, g, r, a),
            lambda r, g, b, a: (b, g, a, r), lambda r, g, b, a: (b, a, r, g), lambda r, g, b, a: (b, a, g, r),
            lambda r, g, b, a: (a, r, g, b), lambda r, g, b, a: (a, r, b, g), lambda r, g, b, a: (a, g, r, b),
            lambda r, g, b, a: (a, g, b, r), lambda r, g, b, a: (a, b, r, g), lambda r, g, b, a: (a, b, g, r)
        )
    }

    decrypt: 'dict[str, Callable[[Any, Any, Any, Any], tuple]]' = {
        'r': None, 'g': None, 'b': None, 'a': None,
        'rg': (lambda g, r, b, a: (r, g, b, a),), 'rb': (lambda b, g, r, a: (r, g, b, a),),
        'ra': (lambda a, g, b, r: (r, g, b, a),), 'gb': (lambda r, b, g, a: (r, g, b, a),),
        'ga': (lambda r, a, b, g: (r, g, b, a),), 'ba': (lambda r, g, a, b: (r, g, b, a),),
        'rgb': (
            lambda r, g, b, a: (r, g, b, a), lambda r, b, g, a: (r, g, b, a), lambda g, r, b, a: (r, g, b, a),
            lambda g, b, r, a: (r, g, b, a), lambda b, r, g, a: (r, g, b, a), lambda b, g, r, a: (r, g, b, a)
        ),
        'rga': (
            lambda r, g, b, a: (r, g, b, a), lambda r, a, b, g: (r, g, b, a), lambda g, r, b, a: (r, g, b, a),
            lambda g, a, b, r: (r, g, b, a), lambda a, r, b, g: (r, g, b, a), lambda a, g, b, r: (r, g, b, a)
        ),
        'rba': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda b, g, r, a: (r, g, b, a),
            lambda b, g, a, r: (r, g, b, a), lambda a, g, r, b: (r, g, b, a), lambda a, g, b, r: (r, g, b, a)
        ),
        'gba': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda r, b, g, a: (r, g, b, a),
            lambda r, b, a, g: (r, g, b, a), lambda r, a, g, b: (r, g, b, a), lambda r, a, b, g: (r, g, b, a)
        ),
        'rgba': (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda r, b, g, a: (r, g, b, a),
            lambda r, b, a, g: (r, g, b, a), lambda r, a, g, b: (r, g, b, a), lambda r, a, b, g: (r, g, b, a),
            lambda g, r, b, a: (r, g, b, a), lambda g, r, a, b: (r, g, b, a), lambda g, b, r, a: (r, g, b, a),
            lambda g, b, a, r: (r, g, b, a), lambda g, a, r, b: (r, g, b, a), lambda g, a, b, r: (r, g, b, a),
            lambda b, r, g, a: (r, g, b, a), lambda b, r, a, g: (r, g, b, a), lambda b, g, r, a: (r, g, b, a),
            lambda b, g, a, r: (r, g, b, a), lambda b, a, r, g: (r, g, b, a), lambda b, a, g, r: (r, g, b, a),
            lambda a, r, g, b: (r, g, b, a), lambda a, r, b, g: (r, g, b, a), lambda a, g, r, b: (r, g, b, a),
            lambda a, g, b, r: (r, g, b, a), lambda a, b, r, g: (r, g, b, a), lambda a, b, g, r: (r, g, b, a)
        )
    }

    index_dict = {
        'rg': [0], 'rb': [0], 'ra': [0], 'gb': [0], 'ga': [0], 'ba': [0],
        'rgb': [0, 1, 2, 3, 4, 5], 'rga': [0, 1, 2, 3, 4, 5], 'rba': [0, 1, 2, 3, 4, 5],
        'gba': [0, 1, 2, 3, 4, 5], 'rgba': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}

    # print({k: list(range(len(v))) for k, v in encrypt.items() if v is not None})


class MappingFuncV3(object):
    encrypt: 'dict[str, Callable[[ndarray], ndarray]]' = {
        'r': None, 'g': None, 'b': None, 'a': None,
        'rg': (lambda a: a[:, :, (1, 0, 2, 3)],), 'rb': (lambda a: a[:, :, (2, 1, 0, 3)],),
        'ra': (lambda a: a[:, :, (3, 1, 2, 0)],), 'gb': (lambda a: a[:, :, (0, 2, 1, 3)],),
        'ga': (lambda a: a[:, :, (0, 3, 2, 1)],), 'ba': (lambda a: a[:, :, (0, 1, 3, 2)],),
        'rgb': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 2, 1, 3)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (2, 1, 0, 3)]
        ),
        'rga': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 3, 2, 1)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        'rba': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        'gba': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 3, 2, 1)]
        ),
        'rgba': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 3, 2, 1)],
            lambda a: a[:, :, (1, 0, 2, 3)], lambda a: a[:, :, (1, 0, 3, 2)], lambda a: a[:, :, (1, 2, 0, 3)],
            lambda a: a[:, :, (1, 2, 3, 0)], lambda a: a[:, :, (1, 3, 0, 2)], lambda a: a[:, :, (1, 3, 2, 0)],
            lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (2, 0, 3, 1)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (2, 3, 0, 1)], lambda a: a[:, :, (2, 3, 1, 0)],
            lambda a: a[:, :, (3, 0, 1, 2)], lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (3, 1, 0, 2)],
            lambda a: a[:, :, (3, 1, 2, 0)], lambda a: a[:, :, (3, 2, 0, 1)], lambda a: a[:, :, (3, 2, 1, 0)]
            )
        }

    decrypt: 'dict[str, Callable[[ndarray], ndarray]]' = {
        'r': None, 'g': None, 'b': None, 'a': None,
        'rg': (lambda a: a[:, :, (1, 0, 2, 3)],), 'rb': (lambda a: a[:, :, (2, 1, 0, 3)],),
        'ra': (lambda a: a[:, :, (3, 1, 2, 0)],), 'gb': (lambda a: a[:, :, (0, 2, 1, 3)],),
        'ga': (lambda a: a[:, :, (0, 3, 2, 1)],), 'ba': (lambda a: a[:, :, (0, 1, 3, 2)],),
        'rgb': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 2, 1, 3)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (2, 1, 0, 3)]
        ),
        'rga': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 3, 2, 1)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        'rba': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        'gba': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 2, 1)]
        ),
        'rgba': (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 2, 1)],
            lambda a: a[:, :, (1, 0, 2, 3)], lambda a: a[:, :, (1, 0, 3, 2)], lambda a: a[:, :, (2, 0, 1, 3)],
            lambda a: a[:, :, (3, 0, 1, 2)], lambda a: a[:, :, (2, 0, 3, 1)], lambda a: a[:, :, (3, 0, 2, 1)],
            lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (1, 3, 0, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (2, 3, 0, 1)], lambda a: a[:, :, (3, 2, 0, 1)],
            lambda a: a[:, :, (1, 2, 3, 0)], lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (2, 1, 3, 0)],
            lambda a: a[:, :, (3, 1, 2, 0)], lambda a: a[:, :, (2, 3, 1, 0)], lambda a: a[:, :, (3, 2, 1, 0)])}

    '''encrypt: 'dict[str, Callable[[ndarray], ndarray]]' = {
        'r': None, 'g': None, 'b': None, 'a': None,
        'rg': (lambda a: obverse_mapping(a, (1, 0, 2, 3)),), 'rb': (lambda a: obverse_mapping(a, (2, 1, 0, 3)),),
        'ra': (lambda a: obverse_mapping(a, (3, 1, 2, 0)),), 'gb': (lambda a: obverse_mapping(a, (0, 2, 1, 3)),),
        'ga': (lambda a: obverse_mapping(a, (0, 3, 2, 1)),), 'ba': (lambda a: obverse_mapping(a, (0, 1, 3, 2)),),
        'rgb': (
            lambda a: obverse_mapping(a, (0, 1, 2, 3)), lambda a: obverse_mapping(a, (0, 2, 1, 3)), lambda a: obverse_mapping(a, (1, 0, 2, 3)),
            lambda a: obverse_mapping(a, (1, 2, 0, 3)), lambda a: obverse_mapping(a, (2, 0, 1, 3)), lambda a: obverse_mapping(a, (2, 1, 0, 3))
        ),
        'rga': (
            lambda a: obverse_mapping(a, (0, 1, 2, 3)), lambda a: obverse_mapping(a, (0, 3, 2, 1)), lambda a: obverse_mapping(a, (1, 0, 2, 3)),
            lambda a: obverse_mapping(a, (1, 3, 2, 0)), lambda a: obverse_mapping(a, (3, 0, 2, 1)), lambda a: obverse_mapping(a, (3, 1, 2, 0))
        ),
        'rba': (
            lambda a: obverse_mapping(a, (0, 1, 2, 3)), lambda a: obverse_mapping(a, (0, 1, 3, 2)), lambda a: obverse_mapping(a, (2, 1, 0, 3)),
            lambda a: obverse_mapping(a, (2, 1, 3, 0)), lambda a: obverse_mapping(a, (3, 1, 0, 2)), lambda a: obverse_mapping(a, (3, 1, 2, 0))
        ),
        'gba': (
            lambda a: obverse_mapping(a, (0, 1, 2, 3)), lambda a: obverse_mapping(a, (0, 1, 3, 2)), lambda a: obverse_mapping(a, (0, 2, 1, 3)),
            lambda a: obverse_mapping(a, (0, 2, 3, 1)), lambda a: obverse_mapping(a, (0, 3, 1, 2)), lambda a: obverse_mapping(a, (0, 3, 2, 1))
        ),
        'rgba': (
            lambda a: obverse_mapping(a, (0, 1, 2, 3)), lambda a: obverse_mapping(a, (0, 1, 3, 2)), lambda a: obverse_mapping(a, (0, 2, 1, 3)),
            lambda a: obverse_mapping(a, (0, 2, 3, 1)), lambda a: obverse_mapping(a, (0, 3, 1, 2)), lambda a: obverse_mapping(a, (0, 3, 2, 1)),
            lambda a: obverse_mapping(a, (1, 0, 2, 3)), lambda a: obverse_mapping(a, (1, 0, 3, 2)), lambda a: obverse_mapping(a, (1, 2, 0, 3)),
            lambda a: obverse_mapping(a, (1, 2, 3, 0)), lambda a: obverse_mapping(a, (1, 3, 0, 2)), lambda a: obverse_mapping(a, (1, 3, 2, 0)),
            lambda a: obverse_mapping(a, (2, 0, 1, 3)), lambda a: obverse_mapping(a, (2, 0, 3, 1)), lambda a: obverse_mapping(a, (2, 1, 0, 3)),
            lambda a: obverse_mapping(a, (2, 1, 3, 0)), lambda a: obverse_mapping(a, (2, 3, 0, 1)), lambda a: obverse_mapping(a, (2, 3, 1, 0)),
            lambda a: obverse_mapping(a, (3, 0, 1, 2)), lambda a: obverse_mapping(a, (3, 0, 2, 1)), lambda a: obverse_mapping(a, (3, 1, 0, 2)),
            lambda a: obverse_mapping(a, (3, 1, 2, 0)), lambda a: obverse_mapping(a, (3, 2, 0, 1)), lambda a: obverse_mapping(a, (3, 2, 1, 0))
        )
    }'''

    '''decrypt: 'dict[str, Callable[[ndarray], ndarray]]' = {
        'r': None, 'g': None, 'b': None, 'a': None,
        'rg': (lambda a: reverse_mapping(a, (1, 0, 2, 3)),), 'rb': (lambda a: reverse_mapping(a, (2, 1, 0, 3)),),
        'ra': (lambda a: reverse_mapping(a, (3, 1, 2, 0)),), 'gb': (lambda a: reverse_mapping(a, (0, 2, 1, 3)),),
        'ga': (lambda a: reverse_mapping(a, (0, 3, 2, 1)),), 'ba': (lambda a: reverse_mapping(a, (0, 1, 3, 2)),),
        'rgb': (
            lambda a: reverse_mapping(a, (0, 1, 2, 3)), lambda a: reverse_mapping(a, (0, 2, 1, 3)), lambda a: reverse_mapping(a, (1, 0, 2, 3)),
            lambda a: reverse_mapping(a, (1, 2, 0, 3)), lambda a: reverse_mapping(a, (2, 0, 1, 3)), lambda a: reverse_mapping(a, (2, 1, 0, 3))
        ),
        'rga': (
            lambda a: reverse_mapping(a, (0, 1, 2, 3)), lambda a: reverse_mapping(a, (0, 3, 2, 1)), lambda a: reverse_mapping(a, (1, 0, 2, 3)),
            lambda a: reverse_mapping(a, (1, 3, 2, 0)), lambda a: reverse_mapping(a, (3, 0, 2, 1)), lambda a: reverse_mapping(a, (3, 1, 2, 0))
        ),
        'rba': (
            lambda a: reverse_mapping(a, (0, 1, 2, 3)), lambda a: reverse_mapping(a, (0, 1, 3, 2)), lambda a: reverse_mapping(a, (2, 1, 0, 3)),
            lambda a: reverse_mapping(a, (2, 1, 3, 0)), lambda a: reverse_mapping(a, (3, 1, 0, 2)), lambda a: reverse_mapping(a, (3, 1, 2, 0))
        ),
        'gba': (
            lambda a: reverse_mapping(a, (0, 1, 2, 3)), lambda a: reverse_mapping(a, (0, 1, 3, 2)), lambda a: reverse_mapping(a, (0, 2, 1, 3)),
            lambda a: reverse_mapping(a, (0, 2, 3, 1)), lambda a: reverse_mapping(a, (0, 3, 1, 2)), lambda a: reverse_mapping(a, (0, 3, 2, 1))
        ),
        'rgba': (
            lambda a: reverse_mapping(a, (0, 1, 2, 3)), lambda a: reverse_mapping(a, (0, 1, 3, 2)), lambda a: reverse_mapping(a, (0, 2, 1, 3)),
            lambda a: reverse_mapping(a, (0, 2, 3, 1)), lambda a: reverse_mapping(a, (0, 3, 1, 2)), lambda a: reverse_mapping(a, (0, 3, 2, 1)),
            lambda a: reverse_mapping(a, (1, 0, 2, 3)), lambda a: reverse_mapping(a, (1, 0, 3, 2)), lambda a: reverse_mapping(a, (1, 2, 0, 3)),
            lambda a: reverse_mapping(a, (1, 2, 3, 0)), lambda a: reverse_mapping(a, (1, 3, 0, 2)), lambda a: reverse_mapping(a, (1, 3, 2, 0)),
            lambda a: reverse_mapping(a, (2, 0, 1, 3)), lambda a: reverse_mapping(a, (2, 0, 3, 1)), lambda a: reverse_mapping(a, (2, 1, 0, 3)),
            lambda a: reverse_mapping(a, (2, 1, 3, 0)), lambda a: reverse_mapping(a, (2, 3, 0, 1)), lambda a: reverse_mapping(a, (2, 3, 1, 0)),
            lambda a: reverse_mapping(a, (3, 0, 1, 2)), lambda a: reverse_mapping(a, (3, 0, 2, 1)), lambda a: reverse_mapping(a, (3, 1, 0, 2)),
            lambda a: reverse_mapping(a, (3, 1, 2, 0)), lambda a: reverse_mapping(a, (3, 2, 0, 1)), lambda a: reverse_mapping(a, (3, 2, 1, 0))
        )
    }'''

    index_dict = {
        'rg': [0], 'rb': [0], 'ra': [0], 'gb': [0], 'ga': [0], 'ba': [0],
        'rgb': [0, 1, 2, 3, 4, 5], 'rga': [0, 1, 2, 3, 4, 5], 'rba': [0, 1, 2, 3, 4, 5],
        'gba': [0, 1, 2, 3, 4, 5], 'rgba': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}

    # print({k: list(range(len(v))) for k, v in encrypt.items() if v is not None})


FlipFuncV1: 'tuple[Callable[[Image], Image]]' = (
    lambda img: img,
    lambda img: img.transpose(FLIP_LEFT_RIGHT),
    lambda img: img.transpose(FLIP_TOP_BOTTOM),
    lambda img: img.transpose(FLIP_LEFT_RIGHT).transpose(FLIP_TOP_BOTTOM)
)


FlipFuncV2: 'tuple[Callable[[ndarray], ndarray]]' = (
    lambda arr: arr,
    lambda arr: arr[:, ::-1],    # 左右翻转
    lambda arr: arr[::-1],       # 上下翻转
    lambda arr: arr[::-1, ::-1]  # 上下左右翻转
)
