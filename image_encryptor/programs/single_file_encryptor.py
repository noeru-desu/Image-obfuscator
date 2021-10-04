from json import dumps
from math import ceil
from os.path import join, split, splitext
from sys import exit

from Crypto.Cipher import AES
from PIL import Image, UnidentifiedImageError
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.utils.AES import encrypt
from image_encryptor.modules.image_cryptor import XOR_image, generate_encrypted_image, get_encrypted_lists
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.utils import pause


def main():
    program = load_program()

    '''if is_using(program.parameters['path']):
        program.logger.error('文件正在被使用')
        pause()
        exit()'''

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
    except Image.DecompressionBombWarning:
        program.logger.error('图片像素量过多，为防止被解压炸弹DOS攻击，不进行处理')
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
    name, suffix = splitext(split(program.parameters['path'])[1])
    suffix = program.parameters['format'] if program.parameters['format'] is not None else 'png'
    suffix = suffix.strip('.')

    if suffix in ('jpg', 'jpeg', 'wmf', 'webp'):
        program.logger.warning('当前保存格式为有损压缩格式')
        if rgb_mapping:
            program.logger.warning('在此情况下，使用RGB(A)随机映射会导致图片在解密后出现轻微的分界线，按任意键确定')
            pause()
        if xor_rgb:
            program.logger.warning('在此情况下，使用异或加密会导致图片解密后出现严重失真，按任意键确定')
            pause()

    block_width = ceil(size[0] / col)
    block_height = ceil(size[1] / row)
    program.logger.info(f'分块数量：{col}x{row}; 分块大小：{block_width}x{block_height}')
    widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
    program.logger.info('开始处理')
    program.logger.info('正在分割原图')

    bar = ProgressBar(max_value=col * row, widgets=widgets)
    regions, pos_list, flip_list = get_encrypted_lists(img, password, row, col, block_width, block_height, bar)

    program.logger.info(f'分割完成，补全后大小：{block_width * col}x{block_height * row}')

    program.logger.info('正在重组')
    bar = ProgressBar(max_value=col * row, widgets=widgets)
    new_image = generate_encrypted_image(regions, pos_list, flip_list, (block_width * col, block_height * row), rgb_mapping, bar)

    if xor_rgb:
        program.logger.info('正在异或加密，性能较低，请耐心等待')
        new_image = XOR_image(new_image, password, xor_alpha, program.process_pool, program.parameters['process_count'])

    program.logger.info('完成，正在保存文件')
    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    save_path = join(program.parameters['save_path'], name)
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
