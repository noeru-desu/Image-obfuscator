from json import dumps
from math import ceil
from os import walk
from os.path import join, split, splitext
from sys import exit

from Crypto.Cipher import AES
from PIL import Image, UnidentifiedImageError
from PIL.Image import EXTENSION
from PIL.Image import init as PIL_init
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from modules.AES import encrypt
from modules.image_cryptor import XOR_image, generate_encrypted_image, get_encrypted_lists
from modules.loader import load_program
from modules.utils import fake_bar, pause


def encrypt_image(path, parameters):
    try:
        img = Image.open(path).convert('RGBA')
    except FileNotFoundError:
        return split(path)[1], '文件不存在'
    except UnidentifiedImageError:
        return split(path)[1], '无法打开或识别图像格式，或输入了不受支持的格式'
    except Exception as e:
        return split(path)[1], repr(e)

    size = img.size
    col = parameters['col']
    row = parameters['row']
    rgb_mapping = parameters['mapping']
    xor_rgb = parameters['xor_rgb']
    xor_alpha = parameters['xor_alpha']
    password = parameters['password']
    has_password = True if password != 100 else False
    name, suffix = splitext(path)
    suffix = parameters['format'] if parameters['format'] != 'normal' else 'png'
    suffix = suffix.strip('.')

    if (rgb_mapping or xor_rgb) and suffix.upper() in ['JPG', 'JPEG', 'WMF', 'WEBP']:
        rgb_mapping = False
        xor_rgb = False
        xor_alpha = False

    block_width = ceil(size[0] / col)
    block_height = ceil(size[1] / row)

    bar = fake_bar()
    regions, flip_list = get_encrypted_lists(img, password, row, col, block_width, block_height, bar)

    new_image = generate_encrypted_image(regions, flip_list, row, col, block_width, block_height, rgb_mapping, bar)

    if xor_rgb:
        new_image = XOR_image(new_image, password, xor_alpha)

    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    path, file = split(path)
    if suffix.lower() in ['jpg', 'jpeg']:
        new_image = new_image.convert('RGB')

    new_image.save(name, quality=95, subsampling=0)

    json = {
        'width': size[0],
        'height': size[1],
        'col': col,
        'row': row,
        'has_password': has_password,
        'password_base64': encrypt(AES.MODE_CFB, password, 'PASS', base64=True) if has_password else 0,
        'rgb_mapping': rgb_mapping,
        'xor_rgb': xor_rgb,
        'xor_alpha': xor_alpha,
        'version': 1
    }

    with open(join(path, name), "a") as f:
        f.write('\n' + dumps(json, separators=(',', ':')))


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
    for file in files:
        name, suffix = splitext(file)
        if suffix in EXTENSION and not (name.endswith('-encrypted') or name.endswith('-decrypted')):
            future_list.append(program.process_pool.submit(encrypt_image, f"{program.parameters['path']}/{file}", program.parameters))

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
