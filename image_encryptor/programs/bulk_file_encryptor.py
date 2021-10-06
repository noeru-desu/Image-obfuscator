'''
Author       : noeru_desu
Date         : 2021-09-30 20:33:30
LastEditors  : noeru_desu
LastEditTime : 2021-10-06 07:20:36
Description  : 批量加密功能
'''
from json import dumps
from math import ceil
from os import makedirs
from os.path import exists, join, split, splitext

from Crypto.Cipher import AES
from PIL import Image, UnidentifiedImageError
from PIL.Image import EXTENSION, DecompressionBombWarning
from PIL.Image import init as PIL_init
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.utils.AES import encrypt
from image_encryptor.modules.image_cryptor import XOR_image, generate_encrypted_image, map_image
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.utils import fake_bar, pause, walk_file


def encrypt_image(path, parameters, save_relative_path):
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
    col = parameters['col']
    row = parameters['row']
    rgb_mapping = parameters['mapping']
    xor_rgb = parameters['xor_rgb']
    xor_alpha = parameters['xor_alpha']
    password = parameters['password']
    has_password = True if password != 100 else False
    name, suffix = splitext(split(path)[1])
    suffix = parameters['format'] if parameters['format'] is not None else 'png'
    suffix = suffix.strip('.')

    block_width = ceil(size[0] / col)
    block_height = ceil(size[1] / row)

    bar = fake_bar()
    regions, pos_list, flip_list = map_image(img, password, row, col, block_width, block_height, bar)

    new_image = generate_encrypted_image(regions, pos_list, flip_list, (block_width * col, block_height * row), rgb_mapping, bar)

    if xor_rgb:
        new_image = XOR_image(new_image, password, xor_alpha)

    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    save_path = join(parameters['save_path'], save_relative_path, name)
    if suffix.lower() in ['jpg', 'jpeg']:
        new_image = new_image.convert('RGB')

    new_image.save(save_path, quality=95, subsampling=0)

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

    with open(save_path, "a") as f:
        f.write('\n' + dumps(json, separators=(',', ':')))


def main():
    program = load_program()

    if program.parameters['format'] in ('jpg', 'jpeg', 'wmf', 'webp'):
        program.logger.warning('当前保存格式为有损压缩格式')
        if program.parameters['mapping']:
            program.logger.warning('在此情况下，使用RGB(A)随机映射会导致图片在解密后出现轻微的分界线，按任意键确定')
            pause()
        if program.parameters['xor_rgb']:
            program.logger.warning('在此情况下，使用异或加密会导致图片解密后出现严重失真，按任意键确定')
            pause()

    future_list = []

    if not EXTENSION:
        PIL_init()
    for relative_path, files in walk_file(program.parameters['path'], program.parameters['topdown']):
        save_dir = join(program.parameters['save_path'], relative_path)
        for file in files:
            path = join(program.parameters['path'], relative_path, file)
            '''if is_using(path):
                program.logger.warning(f'文件[{file}]正在被使用，跳过处理')
                continue'''
            if not exists(save_dir):
                makedirs(save_dir)
            name, suffix = splitext(file)
            if suffix in EXTENSION and not (name.endswith('-encrypted') or name.endswith('-decrypted')):
                future_list.append(program.process_pool.submit(encrypt_image, path, program.parameters, relative_path))

    if future_list:
        widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
        bar = ProgressBar(max_value=len(future_list), widgets=widgets)

        for future in future_list:
            result = future.result()
            bar.update(bar.value + 1)
            if result is not None:
                program.logger.warning(f'[{result[0]}]{result[1]}')

        bar.finish()
    program.logger.info('完成')
