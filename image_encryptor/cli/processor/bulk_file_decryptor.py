'''
Author       : noeru_desu
Date         : 2021-09-30 20:33:28
LastEditors  : noeru_desu
LastEditTime : 2021-11-14 19:24:31
Description  : 批量解密功能
'''
from os import makedirs
from os.path import exists, join, split, splitext

from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.cli.modules.loader import load_program
from image_encryptor.cli.modules.password_verifier import get_image_data
from image_encryptor.common.modules.image_encrypt import ImageEncrypt
from image_encryptor.common.modules.password_verifier import PasswordDict
from image_encryptor.common.utils.utils import open_image, walk_file, FakeBar


def decrypt_image(path, parameters, image_data, save_relative_path):
    image, error = open_image(path)
    if error is not None:
        return image, error

    image_encrypt = ImageEncrypt(image, image_data['row'], image_data['col'], image_data['password'])

    if image_data['upset'] or image_data['flip'] or image_data['rgb_mapping']:
        image_encrypt.init_block_data(True, image_data['upset'], image_data['flip'], image_data['rgb_mapping'], FakeBar)

        image_encrypt.generate_image(FakeBar)

    if image_data['xor_rgb']:
        image_encrypt.xor_pixels(image_data['xor_alpha'])

    image = image_encrypt.image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(split(path)[1])
    suffix = parameters['format'] if parameters['format'] is not None else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

    image.save(join(parameters['output_path'], save_relative_path, name), quality=95, subsampling=0)


def main():
    program = load_program()

    future_list = []

    if not EXTENSION:
        PIL_init()
    password_set = PasswordDict(program.parameters['password'] if program.parameters['password'] != 100 else None)
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
