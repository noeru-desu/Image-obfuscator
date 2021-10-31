'''
Author       : noeru_desu
Date         : 2021-10-10 10:46:17
LastEditors  : noeru_desu
LastEditTime : 2021-10-31 15:45:55
Description  : 主要针对QQ群的图片反阻止发送功能(测试中)
'''
from numpy.random import randint
from os.path import join, split, splitext

from PIL import Image

from image_encryptor.gui.modules.loader import load_program


def main(frame, logger, gauge, image: Image.Image, save: bool):
    program = load_program()

    logger('开始处理')

    image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, 0), (randint(256), randint(256), randint(256)))
    image.putpixel((0, image.size[1] - 1), (randint(256), randint(256), randint(256)))
    image.putpixel((image.size[0] - 1, image.size[1] - 1), (randint(256), randint(256), randint(256)))

    if save:
        logger('完成，正在保存文件')
        name, suffix = splitext(split(program.data.loaded_image_path)[1])
        suffix = Image.EXTENSION_KEYS[frame.selectFormat.Selection]
        suffix = suffix.strip('.')
        name = f'{name}-anti-harmony.{suffix}'
        if suffix.lower() in ['jpg', 'jpeg']:
            image = image.convert('RGB')
        image.save(join(frame.selectSavePath.Path, name), quality=frame.saveQuality.Value, subsampling=frame.subsamplingLevel.Value)
    gauge.SetValue(100)
    logger('完成')
    return image
