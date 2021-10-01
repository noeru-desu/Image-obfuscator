from math import ceil
from os import walk
from os.path import split, splitext
from sys import exit

from PIL import Image, UnidentifiedImageError
from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from modules.image_cryptor import XOR_image, generate_decrypted_image, get_mapping_lists
from modules.loader import load_program
from modules.utils import check_password, fake_bar, is_using, pause


def decrypt_image(path, parameters, image_data):
    try:
        img = Image.open(path).convert('RGBA')
    except FileNotFoundError:
        return split(path)[1], '文件不存在'
    except UnidentifiedImageError:
        return split(path)[1], '无法打开或识别图像格式，或输入了不受支持的格式'
    except Exception as e:
        return split(path)[1], repr(e)

    size = img.size
    block_width = ceil(size[0] / image_data['col'])
    block_height = ceil(size[1] / image_data['row'])

    bar = fake_bar()
    regions, pos_list, flip_list = get_mapping_lists(img, image_data['password'], image_data['row'], image_data['col'], block_width, block_height, bar)

    new_image = generate_decrypted_image(regions, pos_list, flip_list, image_data['row'], image_data['col'], block_width, block_height, image_data['rgb_mapping'], bar)

    if image_data['xor_rgb']:
        new_image = XOR_image(new_image, image_data['password'], image_data['xor_alpha'])

    original_image = new_image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(path)
    suffix = parameters['format'] if parameters['format'] != 'normal' else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ['jpg', 'jpeg']:
        original_image = original_image.convert('RGB')
    name = name.replace('-encrypted', '')

    original_image.save(f'{name}-decrypted.{suffix}', quality=95, subsampling=0)


def main():
    program = load_program()

    _, _, files = next(walk(program.parameters['path']))

    if not files:
        program.logger.error('输入了空的文件夹')
        pause()
        exit()

    future_list = []

    if not EXTENSION:
        PIL_init()
    password_set = set()
    for file in files:
        name, suffix = splitext(file)
        path = f"{program.parameters['path']}/{file}"
        if is_using(path):
            program.logger.warning(f'文件[{file}]正在被使用，跳过处理')
            continue
        if suffix not in EXTENSION or name.endswith('-decrypted'):
            continue
        image_data, password_base64 = check_password(path, f'[{file}]', password_set)
        if isinstance(image_data, str):
            program.logger.warning(f'跳过处理[{file}]{image_data}')
            continue
        if image_data['password'] != 100 and password_base64 != 0:
            password_set.add((password_base64, image_data['password']))
        future_list.append(program.process_pool.submit(decrypt_image, path, program.parameters, image_data))

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
