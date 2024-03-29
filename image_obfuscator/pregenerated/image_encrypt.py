# Generated on Sat May 21 06:20:59 2022
from typing import TYPE_CHECKING

from PIL.Image import FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM

# from image_obfuscator.modules.image import obverse_mapping, reverse_mapping

if TYPE_CHECKING:
    from typing import Any, Callable, Optional
    from PIL.Image import Image
    from numpy import ndarray


class MappingFuncV1(object):
    encrypt: 'tuple[Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Any]], ...]' = (
        lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (g, r, b, a),
        lambda r, g, b, a: (b, g, r, a), lambda r, g, b, a: (g, b, r, a)
    )

    decrypt: 'tuple[Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Any]], ...]' = (
        lambda r, g, b, a: (g, b, r, a), lambda r, g, b, a: (g, r, b, a),
        lambda r, g, b, a: (b, g, r, a), lambda r, g, b, a: (b, r, g, a)
    )

    index_list = [1, 2, 3, 0]


class MappingFuncV2(object):
    encrypt: 'dict[int, Optional[tuple[Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Any]], ...]]]' = {
        2338065862577075610: None, 6917473940299867721: None, 2225566097923666370: None, 5929087490696133568: None,
        7245409237690708392: (lambda r, g, b, a: (g, r, b, a),), -6258529559168087954: (lambda r, g, b, a: (b, g, r, a),),
        8845706618679074035: (lambda r, g, b, a: (a, g, b, r),), 4480416093559622028: (lambda r, g, b, a: (r, b, g, a),),
        -5021629377307685470: (lambda r, g, b, a: (r, a, b, g),), 8733206854025664795: (lambda r, g, b, a: (r, g, a, b),),
        9206708773934830827: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, b, g, a), lambda r, g, b, a: (g, r, b, a),
            lambda r, g, b, a: (g, b, r, a), lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (b, g, r, a)
        ),
        2352335208718012026: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, a, b, g), lambda r, g, b, a: (g, r, b, a),
            lambda r, g, b, a: (g, a, b, r), lambda r, g, b, a: (a, r, b, g), lambda r, g, b, a: (a, g, b, r)
        ),
        -4149246186050457657: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (b, g, r, a),
            lambda r, g, b, a: (b, g, a, r), lambda r, g, b, a: (a, g, r, b), lambda r, g, b, a: (a, g, b, r)
        ),
        -7458687224047931163: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (r, b, g, a),
            lambda r, g, b, a: (r, b, a, g), lambda r, g, b, a: (r, a, g, b), lambda r, g, b, a: (r, a, b, g)
        ),
        -84722638022233667: (
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

    decrypt: 'dict[int, Optional[tuple[Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Any]], ...]]]' = {
        2338065862577075610: None, 6917473940299867721: None, 2225566097923666370: None, 5929087490696133568: None,
        7245409237690708392: (lambda g, r, b, a: (r, g, b, a),), -6258529559168087954: (lambda b, g, r, a: (r, g, b, a),),
        8845706618679074035: (lambda a, g, b, r: (r, g, b, a),), 4480416093559622028: (lambda r, b, g, a: (r, g, b, a),),
        -5021629377307685470: (lambda r, a, b, g: (r, g, b, a),), 8733206854025664795: (lambda r, g, a, b: (r, g, b, a),),
        9206708773934830827: (
            lambda r, g, b, a: (r, g, b, a), lambda r, b, g, a: (r, g, b, a), lambda g, r, b, a: (r, g, b, a),
            lambda g, b, r, a: (r, g, b, a), lambda b, r, g, a: (r, g, b, a), lambda b, g, r, a: (r, g, b, a)
        ),
        2352335208718012026: (
            lambda r, g, b, a: (r, g, b, a), lambda r, a, b, g: (r, g, b, a), lambda g, r, b, a: (r, g, b, a),
            lambda g, a, b, r: (r, g, b, a), lambda a, r, b, g: (r, g, b, a), lambda a, g, b, r: (r, g, b, a)
        ),
        -4149246186050457657: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda b, g, r, a: (r, g, b, a),
            lambda b, g, a, r: (r, g, b, a), lambda a, g, r, b: (r, g, b, a), lambda a, g, b, r: (r, g, b, a)
        ),
        -7458687224047931163: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda r, b, g, a: (r, g, b, a),
            lambda r, b, a, g: (r, g, b, a), lambda r, a, g, b: (r, g, b, a), lambda r, a, b, g: (r, g, b, a)
        ),
        -84722638022233667: (
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
        7245409237690708392: [0], -6258529559168087954: [0], 8845706618679074035: [0], 4480416093559622028: [0], -5021629377307685470: [0], 8733206854025664795: [0],
        9206708773934830827: [0, 1, 2, 3, 4, 5], 2352335208718012026: [0, 1, 2, 3, 4, 5], -4149246186050457657: [0, 1, 2, 3, 4, 5],
        -7458687224047931163: [0, 1, 2, 3, 4, 5], -84722638022233667: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    }

    # print({k: list(range(len(v))) for k, v in encrypt.items() if v is not None})


class MappingFuncV3(object):
    encrypt: 'dict[int, Optional[tuple[Callable[[ndarray], ndarray], ...]]]' = {
        2338065862577075610: None, 6917473940299867721: None, 2225566097923666370: None, 5929087490696133568: None,
        7245409237690708392: (lambda a: a[:, :, (1, 0, 2, 3)],), -6258529559168087954: (lambda a: a[:, :, (2, 1, 0, 3)],),
        8845706618679074035: (lambda a: a[:, :, (3, 1, 2, 0)],), 4480416093559622028: (lambda a: a[:, :, (0, 2, 1, 3)],),
        -5021629377307685470: (lambda a: a[:, :, (0, 3, 2, 1)],), 8733206854025664795: (lambda a: a[:, :, (0, 1, 3, 2)],),
        9206708773934830827: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 2, 1, 3)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (2, 1, 0, 3)]
        ),
        2352335208718012026: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 3, 2, 1)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        -4149246186050457657: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        -7458687224047931163: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 3, 2, 1)]
        ),
        -84722638022233667: (
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

    decrypt: 'dict[int, Optional[tuple[Callable[[ndarray], ndarray], ...]]]' = {
        2338065862577075610: None, 6917473940299867721: None, 2225566097923666370: None, 5929087490696133568: None,
        7245409237690708392: (lambda a: a[:, :, (1, 0, 2, 3)],), -6258529559168087954: (lambda a: a[:, :, (2, 1, 0, 3)],),
        8845706618679074035: (lambda a: a[:, :, (3, 1, 2, 0)],), 4480416093559622028: (lambda a: a[:, :, (0, 2, 1, 3)],),
        -5021629377307685470: (lambda a: a[:, :, (0, 3, 2, 1)],), 8733206854025664795: (lambda a: a[:, :, (0, 1, 3, 2)],),
        9206708773934830827: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 2, 1, 3)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (2, 1, 0, 3)]
        ),
        2352335208718012026: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 3, 2, 1)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        -4149246186050457657: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        -7458687224047931163: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 2, 1)]
        ),
        -84722638022233667: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 2, 1)],
            lambda a: a[:, :, (1, 0, 2, 3)], lambda a: a[:, :, (1, 0, 3, 2)], lambda a: a[:, :, (2, 0, 1, 3)],
            lambda a: a[:, :, (3, 0, 1, 2)], lambda a: a[:, :, (2, 0, 3, 1)], lambda a: a[:, :, (3, 0, 2, 1)],
            lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (1, 3, 0, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (2, 3, 0, 1)], lambda a: a[:, :, (3, 2, 0, 1)],
            lambda a: a[:, :, (1, 2, 3, 0)], lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (2, 1, 3, 0)],
            lambda a: a[:, :, (3, 1, 2, 0)], lambda a: a[:, :, (2, 3, 1, 0)], lambda a: a[:, :, (3, 2, 1, 0)])
    }

    index_dict = {
        7245409237690708392: [0], -6258529559168087954: [0], 8845706618679074035: [0], 4480416093559622028: [0], -5021629377307685470: [0], 8733206854025664795: [0],
        9206708773934830827: [0, 1, 2, 3, 4, 5], 2352335208718012026: [0, 1, 2, 3, 4, 5], -4149246186050457657: [0, 1, 2, 3, 4, 5],
        -7458687224047931163: [0, 1, 2, 3, 4, 5], -84722638022233667: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]    }

    # print({k: list(range(len(v))) for k, v in encrypt.items() if v is not None})


FlipFuncV1: 'tuple[Callable[[Image], Image], ...]' = (
    lambda img: img,
    lambda img: img.transpose(FLIP_LEFT_RIGHT),
    lambda img: img.transpose(FLIP_TOP_BOTTOM),
    lambda img: img.transpose(FLIP_LEFT_RIGHT).transpose(FLIP_TOP_BOTTOM)
)


FlipFuncV2: 'tuple[Callable[[ndarray], ndarray], ...]' = (
    lambda arr: arr,
    lambda arr: arr[:, ::-1],    # 左右翻转
    lambda arr: arr[::-1],       # 上下翻转
    lambda arr: arr[::-1, ::-1]  # 上下左右翻转
)
