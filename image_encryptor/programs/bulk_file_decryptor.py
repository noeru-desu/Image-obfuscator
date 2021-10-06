'''
Author       : noeru_desu
Date         : 2021-09-30 20:33:28
LastEditors  : noeru_desu
LastEditTime : 2021-10-06 07:19:59
Description  : 批量解密功能
'''
from math import ceil
from ntpath import join
from os import makedirs
from os.path import exists, split, splitext

from PIL import Image, UnidentifiedImageError
from PIL.Image import EXTENSION, DecompressionBombWarning
from PIL.Image import init as PIL_init
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.modules.image_cryptor import XOR_image, generate_decrypted_image, map_image
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.utils import check_password, fake_bar, walk_file


def decrypt_image(path, parameters, image_data, save_relative_path):
    try:
        img = Image.open(path).convert('RGBA')
    except FileNotFoundError:
        return split(path)[1], '文件不存在'
    except UnidentifiedImageError:
        return split(path)[1], '无法打开或识别图像格式，或输入了不受支持的格式'
    except DecompressionBombWarning:
        return split(path)[1], '图片像素量过多，为防止被解压炸弹DOS攻击，自动跳过'
    except Exception as e:
        return split(path)[1], repr(e)

    size = img.size
    block_width = ceil(size[0] / image_data['col'])
    block_height = ceil(size[1] / image_data['row'])

    bar = fake_bar()
    regions, pos_list, flip_list = map_image(img, image_data['password'], image_data['row'], image_data['col'], block_width, block_height, bar)

    new_image = generate_decrypted_image(regions, pos_list, flip_list, image_data['row'], image_data['col'], block_width, block_height, image_data['rgb_mapping'], bar)

    if image_data['xor_rgb']:
        new_image = XOR_image(new_image, image_data['password'], image_data['xor_alpha'])

    original_image = new_image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(split(path)[1])
    suffix = parameters['format'] if parameters['format'] is not None else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ['jpg', 'jpeg']:
        original_image = original_image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

    original_image.save(join(parameters['save_path'], save_relative_path, name), quality=95, subsampling=0)


def main():
    program = load_program()

    future_list = []

    if not EXTENSION:
        PIL_init()
    password_set = set()
    for relative_path, files in walk_file(program.parameters['path'], program.parameters['topdown']):
        save_dir = join(program.parameters['save_path'], relative_path)
        for file in files:
            name, suffix = splitext(file)
            path = join(program.parameters['path'], relative_path, file)
            '''if is_using(path):
                program.logger.warning(f'文件[{file}]正在被使用，跳过处理')
                continue'''
            if suffix not in EXTENSION or name.endswith('-decrypted'):
                continue
            image_data, password_base64 = check_password(path, f'[{file}]', password_set)
            if isinstance(image_data, str):
                program.logger.warning(f'跳过处理[{file}]{image_data}')
                continue
            if image_data['password'] != 100 and password_base64 != 0:
                password_set.add((password_base64, image_data['password']))
            if not exists(save_dir):
                makedirs(save_dir)
            future_list.append(program.process_pool.submit(decrypt_image, path, program.parameters, image_data, relative_path))

    if future_list:
        widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
        bar = ProgressBar(max_value=len(future_list), widgets=widgets)

        for future in future_list:
            result = future.result()
            bar.update(bar.value + 1)
            if result is not None:
                program.logger.warning(f'{result[1]}[{result[0]}]')

        bar.finish()
    program.logger.info('完成')
