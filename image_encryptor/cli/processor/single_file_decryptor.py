'''
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2021-11-14 19:23:46
Description  : 单文件解密功能
'''
from os.path import join, split, splitext
from sys import exit

from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from image_encryptor.cli.modules.loader import create_process_pool, load_program
from image_encryptor.cli.modules.password_verifier import get_image_data
from image_encryptor.common.modules.image_encrypt import ImageEncrypt
from image_encryptor.common.utils.utils import open_image, pause


def main():
    program = load_program()

    '''if is_using(program.parameters['input_path']):
        program.logger.error('文件正在被使用')
        pause()
        exit()'''

    image, error = open_image(program.parameters['input_path'])
    if error is not None:
        program.logger.error(error)
        pause()
        exit()

    program.logger.info(f'导入大小：{image.size[0]}x{image.size[1]}')

    image_data, error = get_image_data(program.parameters['input_path'])
    if error is not None:
        program.logger.error(error)
        pause()
        exit()

    program.logger.info(f"原始图片信息：大小：{image_data['width']}x{image_data['height']}; 分块数量：{image_data['col']}x{image_data['row']}")
    widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
    image_encrypt = ImageEncrypt(image, image_data['row'], image_data['col'], image_data['password'])
    program.logger.info('正在处理')

    if image_data['upset'] or image_data['flip'] or image_data['rgb_mapping']:
        program.logger.info('正在分割加密图像')
        bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
        image_encrypt.init_block_data(True, image_data['upset'], image_data['flip'], image_data['rgb_mapping'], bar)

        program.logger.info('正在重组')

        bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
        image_encrypt.generate_image(bar)

    if image_data['xor_rgb']:
        create_process_pool()
        program.logger.info('正在异或解密，性能较低，请耐心等待')
        image_encrypt.xor_pixels(image_data['xor_alpha'])

    program.logger.info('正在保存文件')
    image = image_encrypt.image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(split(program.parameters['input_path'])[1])
    suffix = program.parameters['format'] if program.parameters['format'] is not None else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

    image.save(join(program.parameters['output_path'], name), quality=95, subsampling=0)
