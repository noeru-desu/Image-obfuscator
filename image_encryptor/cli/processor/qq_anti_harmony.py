'''
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2021-11-14 19:15:11
Description  : 主要针对QQ群的图片反阻止发送功能(测试中)
'''
from numpy.random import randint
from os.path import join, split, splitext
from sys import exit

from image_encryptor.cli.modules.loader import load_program
from image_encryptor.common.utils.utils import open_image, pause


def main():
    program = load_program()

    image, error = open_image(program.parameters['input_path'])
    if error is not None:
        program.logger.error(error)
        pause()
        exit()

    name, suffix = splitext(split(program.parameters['input_path'])[1])
    suffix = program.parameters['format'] if program.parameters['format'] is not None else 'png'
    suffix = suffix.strip('.')

    program.logger.info('开始处理')

    image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((0, image.size[1] - 1), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(256), randint(256), randint(256)))

    program.logger.info('完成，正在保存文件')
    name = f'{name}-anti-harmony.{suffix}'
    output_path = join(program.parameters['output_path'], name)
    if suffix.lower() in ('jpg', 'jpeg'):
        image = image.convert('RGB')

    image.save(output_path, quality=95, subsampling=0)
