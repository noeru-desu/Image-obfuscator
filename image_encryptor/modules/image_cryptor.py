from math import ceil
from random import randrange, seed, shuffle

from PIL import Image


def get_encrypted_lists(image, random_seed, row, col, block_width, block_height, bar):
    regions = []
    flip_list = []
    num = 0
    for j in range(row):
        for i in range(col):
            num += 1
            flip_list.append(num % 4)
            regions.append(image.crop((block_width * i, block_height * j, block_width * (i + 1), block_height * (j + 1))))
            bar.update(num)
    seed(random_seed)
    shuffle(regions)
    seed(random_seed)
    shuffle(flip_list)
    bar.finish()
    return regions, flip_list


def generate_encrypted_image(regions, flip_list, row, col, block_width, block_height, rgb_mapping, bar):
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
            bar.update(index + 1)
    bar.finish()
    return image


def xor(xor_num, xor_alpha, pixel_data):
    pixel_list = []
    if xor_alpha:
        for i in pixel_data:
            r, g, b, a = i
            pixel_list.append((r ^ xor_num, g ^ xor_num, b ^ xor_num, a ^ xor_num))
    else:
        for i in pixel_data:
            r, g, b, a = i
            pixel_list.append((r ^ xor_num, g ^ xor_num, b ^ xor_num, a))
    return pixel_list


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


def get_mapping_lists(image, random_seed, row, col, block_width, block_height, bar):
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
            bar.update(num)
    seed(random_seed)
    shuffle(pos_list)
    seed(random_seed)
    shuffle(flip_list)
    bar.finish()
    return regions, pos_list, flip_list


def generate_decrypted_image(regions, pos_list, flip_list, row, col, block_width, block_height, rgb_mapping, bar):
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
        bar.update(index + 1)
    bar.finish()
    return image
