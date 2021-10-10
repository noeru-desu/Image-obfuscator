'''
Author       : noeru_desu
Date         : 2021-09-30 20:33:28
LastEditors  : noeru_desu
LastEditTime : 2021-10-10 11:45:05
Description  : 批量解密功能
'''
from math import ceil
from ntpath import join
from os import makedirs
from os.path import exists, split, splitext

from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.modules.image_cryptor import XOR_image, generate_decrypted_image, map_image
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.password_verifier import PasswordSet, get_image_data
from image_encryptor.utils.utils import fake_bar, open_image, walk_file


def decrypt_image(path, parameters, image_data, save_relative_path):
    image, error = open_image(path)
    if error is not None:
        return image, error

    size = image.size
    block_width = ceil(size[0] / image_data['col'])
    block_height = ceil(size[1] / image_data['row'])

    if image_data['normal_encryption']:
        bar = fake_bar()
        regions, pos_list, flip_list = map_image(image, image_data['password'], True, image_data['row'], image_data['col'], block_width, block_height, bar)

        new_image = generate_decrypted_image(regions, pos_list, flip_list, (block_width * image_data['col'], block_height * image_data['row']), image_data['rgb_mapping'], bar)
    else:
        new_image = image

    if image_data['xor_rgb']:
        new_image = XOR_image(new_image, image_data['password'], image_data['xor_alpha'])

    original_image = new_image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(split(path)[1])
    suffix = parameters['format'] if parameters['format'] is not None else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ['jpg', 'jpeg']:
        original_image = original_image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

    original_image.save(join(parameters['output_path'], save_relative_path, name), quality=95, subsampling=0)


def main():
    program = load_program()

    future_list = []

    if not EXTENSION:
        PIL_init()
    password_set = PasswordSet(program.parameters['password'] if program.parameters['password'] != 100 else None)
    for relative_path, files in walk_file(program.parameters['input_path'], program.parameters['topdown']):
        save_dir = join(program.parameters['output_path'], relative_path)
        for file in files:
            name, suffix = splitext(file)
            path = join(program.parameters['input_path'], relative_path, file)
            '''if is_using(path):
                program.logger.warning(f'文件[{file}]正在被使用，跳过处理')
                continue'''
            if suffix not in EXTENSION or name.endswith('-decrypted'):
                continue
            image_data, error = get_image_data(path, f'[{file}]', password_set)
            if error is not None:
                program.logger.warning(f'跳过处理[{file}]{error}')
                continue
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
