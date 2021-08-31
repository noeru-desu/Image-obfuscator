from PIL import Image
from random import seed, shuffle


def get_encrypted_lists(image, upset_seed, row, col, block_width, block_height, bar=None):
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
    seed(upset_seed)
    shuffle(regions)
    seed(upset_seed)
    shuffle(flip_list)
    if bar is not None:
        bar.finish()
    return regions, flip_list


def generate_encrypted_image(regions, flip_list, rgb_mapping, row, col, block_width, block_height, custom_func=None, bar=None):
    image = Image.new('RGB', (block_width * col, block_height * row))
    index = -1
    for y in range(row):
        for x in range(col):
            index += 1
            if flip_list[index] == 0:
                if custom_func is not None:
                    regions[index] = custom_func(regions[index], block_width, block_height)
                r, g, b, a = regions[index].split()
                regions[index] = Image.merge("RGBA", (g, b, r, a))
            elif flip_list[index] == 1:
                regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
                if rgb_mapping:
                    r, g, b, a = regions[index].split()
                    regions[index] = Image.merge("RGBA", (g, r, b, a))
            elif flip_list[index] == 2:
                regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
                if rgb_mapping:
                    r, g, b, a = regions[index].split()
                    regions[index] = Image.merge("RGBA", (b, g, r, a))
            elif flip_list[index] == 3:
                regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
                regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
                if rgb_mapping:
                    r, g, b, a = regions[index].split()
                    regions[index] = Image.merge("RGBA", (b, r, g, a))
            image.paste(regions[index], (x * block_width, y * block_height))
            if bar is not None:
                bar.update(index + 1)
    if bar is not None:
        bar.finish()
    return image


def get_mapping_lists(image, upset_seed, row, col, block_width, block_height, bar=None):
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
    seed(upset_seed)
    shuffle(pos_list)
    seed(upset_seed)
    shuffle(flip_list)
    if bar is not None:
        bar.finish()
    return regions, pos_list, flip_list


def generate_decrypted_image(regions, pos_list, flip_list, rgb_mapping, row, col, block_width, block_height, custom_func=None, bar=None):
    image = Image.new('RGB', (block_width * col, block_height * row))
    index = -1
    for i in pos_list:
        index += 1
        if flip_list[index] == 0:
            if custom_func is not None:
                regions[index] = custom_func(regions[index], block_width, block_height)
            if rgb_mapping:
                g, b, r, a = regions[index].split()
                regions[index] = Image.merge("RGBA", (r, g, b, a))
        elif flip_list[index] == 1:
            regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
            if rgb_mapping:
                g, r, b, a = regions[index].split()
                regions[index] = Image.merge("RGBA", (r, g, b, a))
        elif flip_list[index] == 2:
            regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
            if rgb_mapping:
                b, g, r, a = regions[index].split()
                regions[index] = Image.merge("RGBA", (r, g, b, a))
        elif flip_list[index] == 3:
            regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
            regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
            if rgb_mapping:
                b, r, g, a = regions[index].split()
                regions[index] = Image.merge("RGBA", (r, g, b, a))
        image.paste(regions[index], i)
        if bar is not None:
            bar.update(index + 1)
    if bar is not None:
        bar.finish()
    return image
