"""
Author       : noeru_desu
Date         : 2022-04-04 10:35:30
LastEditors  : noeru_desu
LastEditTime : 2022-06-07 06:21:45
Description  : 预生成模板
"""
from time import asctime, localtime

gen_func = lambda: template.format(
    generated_time=asctime(localtime()),
    hash_r=hash((True, False, False, False)),
    hash_g=hash((False, True, False, False)),
    hash_b=hash((False, False, True, False)),
    hash_a=hash((False, False, False, True)),
    hash_rg=hash((True, True, False, False)),
    hash_rb=hash((True, False, True, False)),
    hash_ra=hash((True, False, False, True)),
    hash_gb=hash((False, True, True, False)),
    hash_ga=hash((False, True, False, True)),
    hash_ba=hash((False, False, True, True)),
    hash_rgb=hash((True, True, True, False)),
    hash_rga=hash((True, True, False, True)),
    hash_rba=hash((True, False, True, True)),
    hash_gba=hash((False, True, True, True)),
    hash_rgba=hash((True, True, True, True))
)

template = """# Generated on {generated_time}
from typing import TYPE_CHECKING

from PIL.Image import FLIP_LEFT_RIGHT, FLIP_TOP_BOTTOM

# from image_obfuscator.modules.image import obverse_mapping, reverse_mapping

if TYPE_CHECKING:
    from typing import Any, Callable, Optional
    from PIL.Image import Image
    from numpy import ndarray


class MappingFuncV1(object):
    __slots__ = ()
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
    __slots__ = ()
    encrypt: 'dict[int, Optional[tuple[Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Any]], ...]]]' = `
        {hash_r}: None, {hash_g}: None, {hash_b}: None, {hash_a}: None,
        {hash_rg}: (lambda r, g, b, a: (g, r, b, a),), {hash_rb}: (lambda r, g, b, a: (b, g, r, a),),
        {hash_ra}: (lambda r, g, b, a: (a, g, b, r),), {hash_gb}: (lambda r, g, b, a: (r, b, g, a),),
        {hash_ga}: (lambda r, g, b, a: (r, a, b, g),), {hash_ba}: (lambda r, g, b, a: (r, g, a, b),),
        {hash_rgb}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, b, g, a), lambda r, g, b, a: (g, r, b, a),
            lambda r, g, b, a: (g, b, r, a), lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (b, g, r, a)
        ),
        {hash_rga}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, a, b, g), lambda r, g, b, a: (g, r, b, a),
            lambda r, g, b, a: (g, a, b, r), lambda r, g, b, a: (a, r, b, g), lambda r, g, b, a: (a, g, b, r)
        ),
        {hash_rba}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (b, g, r, a),
            lambda r, g, b, a: (b, g, a, r), lambda r, g, b, a: (a, g, r, b), lambda r, g, b, a: (a, g, b, r)
        ),
        {hash_gba}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (r, b, g, a),
            lambda r, g, b, a: (r, b, a, g), lambda r, g, b, a: (r, a, g, b), lambda r, g, b, a: (r, a, b, g)
        ),
        {hash_rgba}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, b, a: (r, g, a, b), lambda r, g, b, a: (r, b, g, a),
            lambda r, g, b, a: (r, b, a, g), lambda r, g, b, a: (r, a, g, b), lambda r, g, b, a: (r, a, b, g),
            lambda r, g, b, a: (g, r, b, a), lambda r, g, b, a: (g, r, a, b), lambda r, g, b, a: (g, b, r, a),
            lambda r, g, b, a: (g, b, a, r), lambda r, g, b, a: (g, a, r, b), lambda r, g, b, a: (g, a, b, r),
            lambda r, g, b, a: (b, r, g, a), lambda r, g, b, a: (b, r, a, g), lambda r, g, b, a: (b, g, r, a),
            lambda r, g, b, a: (b, g, a, r), lambda r, g, b, a: (b, a, r, g), lambda r, g, b, a: (b, a, g, r),
            lambda r, g, b, a: (a, r, g, b), lambda r, g, b, a: (a, r, b, g), lambda r, g, b, a: (a, g, r, b),
            lambda r, g, b, a: (a, g, b, r), lambda r, g, b, a: (a, b, r, g), lambda r, g, b, a: (a, b, g, r)
        )
    ~

    decrypt: 'dict[int, Optional[tuple[Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Any]], ...]]]' = `
        {hash_r}: None, {hash_g}: None, {hash_b}: None, {hash_a}: None,
        {hash_rg}: (lambda g, r, b, a: (r, g, b, a),), {hash_rb}: (lambda b, g, r, a: (r, g, b, a),),
        {hash_ra}: (lambda a, g, b, r: (r, g, b, a),), {hash_gb}: (lambda r, b, g, a: (r, g, b, a),),
        {hash_ga}: (lambda r, a, b, g: (r, g, b, a),), {hash_ba}: (lambda r, g, a, b: (r, g, b, a),),
        {hash_rgb}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, b, g, a: (r, g, b, a), lambda g, r, b, a: (r, g, b, a),
            lambda g, b, r, a: (r, g, b, a), lambda b, r, g, a: (r, g, b, a), lambda b, g, r, a: (r, g, b, a)
        ),
        {hash_rga}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, a, b, g: (r, g, b, a), lambda g, r, b, a: (r, g, b, a),
            lambda g, a, b, r: (r, g, b, a), lambda a, r, b, g: (r, g, b, a), lambda a, g, b, r: (r, g, b, a)
        ),
        {hash_rba}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda b, g, r, a: (r, g, b, a),
            lambda b, g, a, r: (r, g, b, a), lambda a, g, r, b: (r, g, b, a), lambda a, g, b, r: (r, g, b, a)
        ),
        {hash_gba}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda r, b, g, a: (r, g, b, a),
            lambda r, b, a, g: (r, g, b, a), lambda r, a, g, b: (r, g, b, a), lambda r, a, b, g: (r, g, b, a)
        ),
        {hash_rgba}: (
            lambda r, g, b, a: (r, g, b, a), lambda r, g, a, b: (r, g, b, a), lambda r, b, g, a: (r, g, b, a),
            lambda r, b, a, g: (r, g, b, a), lambda r, a, g, b: (r, g, b, a), lambda r, a, b, g: (r, g, b, a),
            lambda g, r, b, a: (r, g, b, a), lambda g, r, a, b: (r, g, b, a), lambda g, b, r, a: (r, g, b, a),
            lambda g, b, a, r: (r, g, b, a), lambda g, a, r, b: (r, g, b, a), lambda g, a, b, r: (r, g, b, a),
            lambda b, r, g, a: (r, g, b, a), lambda b, r, a, g: (r, g, b, a), lambda b, g, r, a: (r, g, b, a),
            lambda b, g, a, r: (r, g, b, a), lambda b, a, r, g: (r, g, b, a), lambda b, a, g, r: (r, g, b, a),
            lambda a, r, g, b: (r, g, b, a), lambda a, r, b, g: (r, g, b, a), lambda a, g, r, b: (r, g, b, a),
            lambda a, g, b, r: (r, g, b, a), lambda a, b, r, g: (r, g, b, a), lambda a, b, g, r: (r, g, b, a)
        )
    ~

    index_dict = `
        {hash_rg}: [0], {hash_rb}: [0], {hash_ra}: [0], {hash_gb}: [0], {hash_ga}: [0], {hash_ba}: [0],
        {hash_rgb}: [0, 1, 2, 3, 4, 5], {hash_rga}: [0, 1, 2, 3, 4, 5], {hash_rba}: [0, 1, 2, 3, 4, 5],
        {hash_gba}: [0, 1, 2, 3, 4, 5], {hash_rgba}: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    ~

    # print(`k: list(range(len(v))) for k, v in encrypt.items() if v is not None~)


class MappingFuncV3(object):
    __slots__ = ()
    encrypt: 'dict[int, Optional[tuple[Callable[[ndarray], ndarray], ...]]]' = `
        {hash_r}: None, {hash_g}: None, {hash_b}: None, {hash_a}: None,
        {hash_rg}: (lambda a: a[:, :, (1, 0, 2, 3)],), {hash_rb}: (lambda a: a[:, :, (2, 1, 0, 3)],),
        {hash_ra}: (lambda a: a[:, :, (3, 1, 2, 0)],), {hash_gb}: (lambda a: a[:, :, (0, 2, 1, 3)],),
        {hash_ga}: (lambda a: a[:, :, (0, 3, 2, 1)],), {hash_ba}: (lambda a: a[:, :, (0, 1, 3, 2)],),
        {hash_rgb}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 2, 1, 3)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (2, 1, 0, 3)]
        ),
        {hash_rga}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 3, 2, 1)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        {hash_rba}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        {hash_gba}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 3, 2, 1)]
        ),
        {hash_rgba}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 3, 2, 1)],
            lambda a: a[:, :, (1, 0, 2, 3)], lambda a: a[:, :, (1, 0, 3, 2)], lambda a: a[:, :, (1, 2, 0, 3)],
            lambda a: a[:, :, (1, 2, 3, 0)], lambda a: a[:, :, (1, 3, 0, 2)], lambda a: a[:, :, (1, 3, 2, 0)],
            lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (2, 0, 3, 1)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (2, 3, 0, 1)], lambda a: a[:, :, (2, 3, 1, 0)],
            lambda a: a[:, :, (3, 0, 1, 2)], lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (3, 1, 0, 2)],
            lambda a: a[:, :, (3, 1, 2, 0)], lambda a: a[:, :, (3, 2, 0, 1)], lambda a: a[:, :, (3, 2, 1, 0)]
            )
    ~

    decrypt: 'dict[int, Optional[tuple[Callable[[ndarray], ndarray], ...]]]' = `
        {hash_r}: None, {hash_g}: None, {hash_b}: None, {hash_a}: None,
        {hash_rg}: (lambda a: a[:, :, (1, 0, 2, 3)],), {hash_rb}: (lambda a: a[:, :, (2, 1, 0, 3)],),
        {hash_ra}: (lambda a: a[:, :, (3, 1, 2, 0)],), {hash_gb}: (lambda a: a[:, :, (0, 2, 1, 3)],),
        {hash_ga}: (lambda a: a[:, :, (0, 3, 2, 1)],), {hash_ba}: (lambda a: a[:, :, (0, 1, 3, 2)],),
        {hash_rgb}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 2, 1, 3)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (2, 0, 1, 3)], lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (2, 1, 0, 3)]
        ),
        {hash_rga}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 3, 2, 1)], lambda a: a[:, :, (1, 0, 2, 3)],
            lambda a: a[:, :, (3, 0, 2, 1)], lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        {hash_rba}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (2, 1, 3, 0)], lambda a: a[:, :, (3, 1, 2, 0)]
        ),
        {hash_gba}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 2, 1)]
        ),
        {hash_rgba}: (
            lambda a: a[:, :, (0, 1, 2, 3)], lambda a: a[:, :, (0, 1, 3, 2)], lambda a: a[:, :, (0, 2, 1, 3)],
            lambda a: a[:, :, (0, 3, 1, 2)], lambda a: a[:, :, (0, 2, 3, 1)], lambda a: a[:, :, (0, 3, 2, 1)],
            lambda a: a[:, :, (1, 0, 2, 3)], lambda a: a[:, :, (1, 0, 3, 2)], lambda a: a[:, :, (2, 0, 1, 3)],
            lambda a: a[:, :, (3, 0, 1, 2)], lambda a: a[:, :, (2, 0, 3, 1)], lambda a: a[:, :, (3, 0, 2, 1)],
            lambda a: a[:, :, (1, 2, 0, 3)], lambda a: a[:, :, (1, 3, 0, 2)], lambda a: a[:, :, (2, 1, 0, 3)],
            lambda a: a[:, :, (3, 1, 0, 2)], lambda a: a[:, :, (2, 3, 0, 1)], lambda a: a[:, :, (3, 2, 0, 1)],
            lambda a: a[:, :, (1, 2, 3, 0)], lambda a: a[:, :, (1, 3, 2, 0)], lambda a: a[:, :, (2, 1, 3, 0)],
            lambda a: a[:, :, (3, 1, 2, 0)], lambda a: a[:, :, (2, 3, 1, 0)], lambda a: a[:, :, (3, 2, 1, 0)])
    ~

    index_dict = `
        {hash_rg}: [0], {hash_rb}: [0], {hash_ra}: [0], {hash_gb}: [0], {hash_ga}: [0], {hash_ba}: [0],
        {hash_rgb}: [0, 1, 2, 3, 4, 5], {hash_rga}: [0, 1, 2, 3, 4, 5], {hash_rba}: [0, 1, 2, 3, 4, 5],
        {hash_gba}: [0, 1, 2, 3, 4, 5], {hash_rgba}: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]\
    ~

    # print(`k: list(range(len(v))) for k, v in encrypt.items() if v is not None~)


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
"""