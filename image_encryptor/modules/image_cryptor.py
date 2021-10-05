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


def get_encrypted_lists(image, random_seed, row, col, block_width, block_height, bar):
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
    shuffle(regions)
    seed(random_seed)
    shuffle(flip_list)
    bar.finish()
    return regions, pos_list, flip_list


def generate_encrypted_image(regions, pos_list, flip_list, size, rgb_mapping, bar):
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


def get_mapping_lists(image, random_seed, row, col, block_width, block_height, bar):
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
    shuffle(pos_list)
    seed(random_seed)
    shuffle(flip_list)
    bar.finish()
    return regions, pos_list, flip_list


def generate_decrypted_image(regions, pos_list, flip_list, size, rgb_mapping, bar):
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


def xor(xor_num, xor_alpha, pixel_data):
    if xor_alpha:
        return [(r ^ xor_num, g ^ xor_num, b ^ xor_num, a ^ xor_num) for r, g, b, a in pixel_data]
    else:
        return [(r ^ xor_num, g ^ xor_num, b ^ xor_num, a) for r, g, b, a in pixel_data]


def XOR_image(region, random_seed, xor_alpha, process_pool=None, process_count=None):
    seed(random_seed)
    xor_num = randrange(256)
    pixel_list = list(region.getdata())
    future_list = []
    num = 0
    if process_pool is None:
        pixel_list = xor(xor_num, xor_alpha, pixel_list)
    else:
        for i in range(0, len(pixel_list), ceil(len(pixel_list) / process_count)):
            if i == 0:
                continue
            future_list.append(process_pool.submit(xor, xor_num, xor_alpha, pixel_list[num:i]))
            num = i + 1
        future_list.append(process_pool.submit(xor, xor_num, xor_alpha, pixel_list[num:]))
        pixel_list = []
        for i in future_list:
            pixel_list.extend(i.result())
    region.putdata(pixel_list)
    return region
