'''
Author       : noeru_desu
Date         : 2021-08-30 21:22:02
LastEditors  : noeru_desu
LastEditTime : 2021-10-06 08:13:40
Description  : 所有图片的加解密方法
'''
from math import ceil
from random import randrange, seed, shuffle

from PIL import Image

flip_func = [
    lambda img: img,
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
]


encrypt_mapping_func = [
    lambda r, g, b, a: (b, r, g, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (g, b, r, a),
]


decrypt_mapping_func = [
    lambda r, g, b, a: (g, b, r, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (b, r, g, a),
]


def map_image(image: Image, random_seed, decryption_mode: bool, row: int, col: int, block_width: int, block_height: int, bar):
    '''
    @description: 生成打乱后的图片分块、翻转分块，与每个分块所在的坐标列表
    @return {(regions, pos_list, flip_list)}
    '''
    block_num = row * col
    regions = []
    pos_list = []
    for y in range(row):
        for x in range(col):
            block_pos = (x * block_width, y * block_height)
            pos_list.append(block_pos)
            regions.append(image.crop((block_pos[0], block_pos[1], block_pos[0] + block_width, block_pos[1] + block_height)))
            bar.update(bar.value + 1)
    flip_list = ([1, 2, 3, 0] * ceil(block_num / 4))[:block_num]
    seed(random_seed)
    if decryption_mode:
        shuffle(pos_list)
    else:
        shuffle(regions)
    seed(random_seed)
    shuffle(flip_list)
    bar.finish()
    return regions, pos_list, flip_list


def generate_encrypted_image(regions: list, pos_list: list, flip_list: list, size: tuple, rgb_mapping: bool, bar) -> Image:
    '''
    @description: 根据map_image()获得的信息生成加密后的图片
    @return {PIL.Image}
    '''
    image = Image.new('RGBA', size)
    if rgb_mapping:
        for region, pos, flip in zip(regions, pos_list, flip_list):
            region = Image.merge('RGBA', encrypt_mapping_func[flip](flip_func[flip](region).split()))
            image.paste(region, pos)
            bar.update(bar.value + 1)
    else:
        for region, pos, flip in zip(regions, pos_list, flip_list):
            region = flip_func[flip](region)
            image.paste(region, pos)
            bar.update(bar.value + 1)
    bar.finish()
    return image


def generate_decrypted_image(regions: list, pos_list: list, flip_list: list, size, rgb_mapping, bar) -> Image:
    '''
    @description: 根据map_image()获得的信息生成解密后的图片
    @return {PIL.Image}
    '''
    image = Image.new('RGBA', size)
    if rgb_mapping:
        for region, pos, flip in zip(regions, pos_list, flip_list):
            region = Image.merge('RGBA', decrypt_mapping_func[flip](flip_func[flip](region).split()))
            image.paste(region, pos)
            bar.update(bar.value + 1)
    else:
        for region, pos, flip in zip(regions, pos_list, flip_list):
            region = flip_func[flip](region)
            image.paste(region, pos)
            bar.update(bar.value + 1)
    bar.finish()
    return image


def _xor_pixel_data(pixel_data: list, xor_num: int, xor_alpha: bool) -> list:
    '''
    @description: 异或每个像素点的RGB(A)通道
    @return {list}
    '''
    if xor_alpha:
        return [(r ^ xor_num, g ^ xor_num, b ^ xor_num, a ^ xor_num) for r, g, b, a in pixel_data]
    else:
        return [(r ^ xor_num, g ^ xor_num, b ^ xor_num, a) for r, g, b, a in pixel_data]


def XOR_image(image: Image, random_seed: int, xor_alpha: bool, process_pool=None, process_count: int = None) -> Image:
    '''
    @description: 异或图片中每个像素点的RGB(A)通道
    @return {PIL.Image}
    '''
    seed(random_seed)
    xor_num = randrange(256)
    pixel_list = list(image.getdata())
    future_list = []
    if process_pool is None:
        pixel_list = _xor_pixel_data(pixel_list, xor_num, xor_alpha)
    else:
        num = 0
        for i in range(0, len(pixel_list), ceil(len(pixel_list) / process_count)):
            if i == 0:
                continue
            future_list.append(process_pool.submit(_xor_pixel_data, pixel_list[num:i], xor_num, xor_alpha))
            num = i
        future_list.append(process_pool.submit(_xor_pixel_data, pixel_list[num:], xor_num, xor_alpha))
        pixel_list = []
        for i in future_list:
            pixel_list.extend(i.result())
    image.putdata(pixel_list)
    return image
