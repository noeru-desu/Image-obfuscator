'''
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2021-10-10 12:18:48
Description  : 主要针对QQ群的图片反和谐功能(测试中)
'''
from random import randint
from os.path import join, split, splitext
from sys import exit

from image_encryptor.modules.loader import load_program
from image_encryptor.utils.utils import open_image, pause


def main():
    program = load_program()

    image, error = open_image(program.parameters['input_path'])
    if error is not None:
        program.logger.error(error)
        pause()
        exit()

    size = image.size

    name, suffix = splitext(split(program.parameters['input_path'])[1])
    suffix = suffix.strip('.')

    program.logger.info('开始处理')

    image.putpixel((0, 0), (randint(0, 255), randint(0, 255), randint(0, 255)))
    image.putpixel((size[0] - 1, 0), (randint(0, 255), randint(0, 255), randint(0, 255)))
    image.putpixel((0, size[1] - 1), (randint(0, 255), randint(0, 255), randint(0, 255)))
    image.putpixel((size[0] - 1, size[1] - 1), (randint(0, 255), randint(0, 255), randint(0, 255)))

    program.logger.info('完成，正在保存文件')
    name = f'{name}-anti-harmony.{suffix}'
    output_path = join(program.parameters['output_path'], name)
    if suffix.lower() in ['jpg', 'jpeg']:
        new_image = image.convert('RGB')

    new_image.save(output_path, quality=95, subsampling=0)
