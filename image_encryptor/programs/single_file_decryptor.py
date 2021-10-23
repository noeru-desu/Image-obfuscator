'''
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2021-10-23 17:43:34
Description  : 单文件解密功能
'''
from os.path import join, split, splitext
from sys import exit

from PIL import Image

from image_encryptor.modules.image_encrypt import ImageEncrypt
from image_encryptor.modules.loader import create_process_pool, load_program
from image_encryptor.utils.password_verifier import get_image_data


def main(frame, logger, gauge, image: Image.Image, save: bool):
    program = load_program()

    image_data, error = get_image_data(program.parameters['input_path'], password_dict=program.password_dict)
    if error is not None:
        frame.error(error, '读取加密参数时出现问题')

    image_encrypt = ImageEncrypt(image, image_data['row'], image_data['col'], image_data['password'])
    program.logger.info('正在处理')

    if image_data['normal_encryption']:
        program.logger.info('正在分割加密图像')
        bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
        image_encrypt.init_block_data(image, True, bar)

        program.logger.info('正在重组')

        bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
        image = image_encrypt.get_image(image, image_data['rgb_mapping'], bar)

    if image_data['xor_rgb']:
        create_process_pool()
        program.logger.info('正在异或解密，性能较低，请耐心等待')
        image = image_encrypt.xor_pixels(image, image_data['xor_alpha'], program.process_pool, program.parameters['process_count'])

    program.logger.info('正在保存文件')
    image = image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    name, suffix = splitext(split(program.parameters['input_path'])[1])
    suffix = program.parameters['format'] if program.parameters['format'] is not None else suffix
    suffix = suffix.strip('.')
    if suffix.lower() in ['jpg', 'jpeg']:
        image = image.convert('RGB')
    name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

    image.save(join(program.parameters['output_path'], name), quality=95, subsampling=0)
