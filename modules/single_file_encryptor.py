from json import dumps
from math import ceil
from os.path import join, split, splitext
from sys import exit

from Crypto.Cipher import AES
from PIL import Image, UnidentifiedImageError
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from modules.AES import encrypt
from modules.image_cryptor import XOR_image, generate_encrypted_image, get_encrypted_lists
from modules.loader import load_program
from modules.utils import pause


def main():
    program = load_program()

    try:
        img = Image.open(program.parameters['path']).convert('RGBA')
    except FileNotFoundError:
        program.logger.error('文件不存在')
        pause()
        exit()
    except UnidentifiedImageError:
        program.logger.error('无法打开或识别图像格式，或输入了不受支持的格式')
        pause()
        exit()
    except Exception as e:
        program.logger.error(repr(e))
        pause()
        exit()

    size = img.size
    program.logger.info(f'导入大小：{size[0]}x{size[1]}')

    col = program.parameters['col']
    row = program.parameters['row']
    rgb_mapping = program.parameters['mapping']
    xor_rgb = program.parameters['xor_rgb']
    xor_alpha = program.parameters['xor_alpha']
    password = program.parameters['password']
    has_password = True if password != 100 else False
    name, suffix = splitext(program.parameters['path'])
    suffix = program.parameters['format'] if program.parameters['format'] != 'normal' else 'png'
    suffix = suffix.strip('.')

    if (rgb_mapping or xor_rgb) and suffix.upper() in ['JPG', 'JPEG', 'WMF', 'WEBP']:
        rgb_mapping = False
        xor_rgb = False
        xor_alpha = False
        program.logger.warning('你指定了一个有损压缩的图像格式来保存文件，已自动关闭RGB随机映射与异或加密')

    block_width = ceil(size[0] / col)
    block_height = ceil(size[1] / row)
    program.logger.info(f'分块数量：{col}x{row}; 分块大小：{block_width}x{block_height}')
    widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
    program.logger.info('开始处理')
    program.logger.info('正在分割原图')

    bar = ProgressBar(max_value=col * row, widgets=widgets)
    regions, flip_list = get_encrypted_lists(img, password, row, col, block_width, block_height, bar)

    program.logger.info(f'分割完成，补全后大小：{block_width * col}x{block_height * row}')

    program.logger.info('正在重组')
    bar = ProgressBar(max_value=col * row, widgets=widgets)
    new_image = generate_encrypted_image(regions, flip_list, row, col, block_width, block_height, rgb_mapping, bar)

    if xor_rgb:
        program.logger.info('正在异或加密，性能较低，请耐心等待')
        new_image = XOR_image(new_image, password, xor_alpha, program.process_pool, program.parameters['process_count'])

    program.logger.info('完成，正在保存文件')
    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    path, file = split(program.parameters['path'])
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
