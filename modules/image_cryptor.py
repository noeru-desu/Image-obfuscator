from random import randrange, seed, shuffle

import numpy as np
from PIL import Image


def get_encrypted_lists(image, random_seed, row, col, block_width, block_height, bar=None):
    regions = []
    flip_list = []
    num = 0
    for j in range(row):
        for i in range(col):
            num += 1
            flip_list.append(num % 4)
            box = (block_width * i, block_height * j, block_width * (i + 1), block_height * (j + 1))
            regions.append(image.crop(box))
            if bar is not None:
                bar.update(num)
    seed(random_seed)
    shuffle(regions)
    seed(random_seed)
    shuffle(flip_list)
    if bar is not None:
        bar.finish()
    return regions, flip_list


def generate_encrypted_image(regions, flip_list, random_seed, row, col, block_width, block_height, rgb_mapping, xor_alpha, bar=None):
    image = Image.new('RGBA', (block_width * col, block_height * row))
    index = -1
    for y in range(row):
        for x in range(col):
            index += 1
            if flip_list[index] == 0 and rgb_mapping:
                b, r, g, a = regions[index].split()
            elif flip_list[index] == 1:
                regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
                if rgb_mapping:
                    g, r, b, a = regions[index].split()
            elif flip_list[index] == 2:
                regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
                if rgb_mapping:
                    b, g, r, a = regions[index].split()
            elif flip_list[index] == 3:
                regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
                regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
                if rgb_mapping:
                    g, b, r, a = regions[index].split()
            if rgb_mapping:
                regions[index] = Image.merge('RGBA', (r, g, b, a))
            image.paste(regions[index], (x * block_width, y * block_height))
            if bar is not None:
                bar.update(index + 1)
    if rgb_mapping:
        seed(random_seed)
        image = XOR_image(image, randrange(256), xor_alpha)
    if bar is not None:
        bar.finish()
    return image


def XOR_image(region, xor_num: int, xor_alpha):
    region = np.array(region, np.uint8)
    if not xor_alpha:
        region_alpha = region[:, :, 3]
        region = region[:, :, :3]
    region ^= xor_num
    if not xor_alpha:
        region = np.dstack((region, region_alpha))
    return Image.fromarray(region)


def get_mapping_lists(image, random_seed, row, col, block_width, block_height, bar=None):
    regions = []
    pos_list = []
    flip_list = []
    num = 0
    for y in range(row):
        for x in range(col):
            num += 1
            flip_list.append(num % 4)
            pos_list.append((x * block_width, y * block_height))
            regions.append(image.crop((block_width * x, block_height * y, block_width * (x + 1), block_height * (y + 1))))
            if bar is not None:
                bar.update(num)
    seed(random_seed)
    shuffle(pos_list)
    seed(random_seed)
    shuffle(flip_list)
    if bar is not None:
        bar.finish()
    return regions, pos_list, flip_list


def generate_decrypted_image(regions, pos_list, flip_list, random_seed, row, col, block_width, block_height, rgb_mapping, xor_alpha, bar=None):
    image = Image.new('RGBA', (block_width * col, block_height * row))
    index = -1
    for i in pos_list:
        index += 1
        if flip_list[index] == 0 and rgb_mapping:
            g, b, r, a = regions[index].split()
        elif flip_list[index] == 1:
            regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
            if rgb_mapping:
                g, r, b, a = regions[index].split()
        elif flip_list[index] == 2:
            regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
            if rgb_mapping:
                b, g, r, a = regions[index].split()
        elif flip_list[index] == 3:
            regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
            regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
            if rgb_mapping:
                b, r, g, a = regions[index].split()
        if rgb_mapping:
            regions[index] = Image.merge('RGBA', (r, g, b, a))
        image.paste(regions[index], i)
        if bar is not None:
            bar.update(index + 1)
    if rgb_mapping:
        seed(random_seed)
        image = XOR_image(image, randrange(256), xor_alpha)
    if bar is not None:
        bar.finish()
    return image
