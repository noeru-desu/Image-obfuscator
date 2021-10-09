'''
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2021-10-08 20:57:27
Description  : 单文件解密功能
'''
from math import ceil
from os.path import join, split, splitext
from sys import exit

from PIL import Image, UnidentifiedImageError
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.modules.image_cryptor import XOR_image, generate_decrypted_image, map_image
from image_encryptor.modules.loader import create_process_pool, load_program
from image_encryptor.utils.utils import check_password, pause


def main():
    program = load_program()

    '''if is_using(program.parameters['input_path']):
        program.logger.error('文件正在被使用')
        pause()
        exit()'''

    try:
        image = Image.open(program.parameters['input_path']).convert('RGBA')
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

    size = image.size
    program.logger.info(f'导入大小：{size[0]}x{size[1]}')

    image_data, _, error = check_password(program.parameters['input_path'])
    if error is not None:
        program.logger.error(image_data)
        pause()
        exit()
    program.logger.info(f"原始图片信息：大小：{image_data['width']}x{image_data['height']}; 分块数量：{image_data['col']}x{image_data['row']}")

    block_width = ceil(size[0] / image_data['col'])
    block_height = ceil(size[1] / image_data['row'])
    program.logger.info(f'分块大小：{block_width}x{block_height}')
    widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
    program.logger.info('正在处理')

    if image_data['normal_encryption']:
        program.logger.info('正在分割加密图像')
        bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
        regions, pos_list, flip_list = map_image(image, image_data['password'], True, image_data['row'], image_data['col'], block_width, block_height, bar)

        program.logger.info('正在重组')

        bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
        new_image = generate_decrypted_image(regions, pos_list, flip_list, (block_width * image_data['col'], block_height * image_data['row']), image_data['rgb_mapping'], bar)
    else:
        new_image = image

    if image_data['xor_rgb']:
        create_process_pool()
        program.logger.info('正在异或解密，性能较低，请耐心等待')
        size = new_image.size
        new_image = XOR_image(new_image, image_data['password'], image_data['xor_alpha'], program.process_pool, program.parameters['process_count'])

    program.logger.info('正在保存文件')
    original_image = new_image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(split(program.parameters['input_path'])[1])
    suffix = program.parameters['format'] if program.parameters['format'] is not None else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ['jpg', 'jpeg']:
        original_image = original_image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

    original_image.save(join(program.parameters['output_path'], name), quality=95, subsampling=0)
