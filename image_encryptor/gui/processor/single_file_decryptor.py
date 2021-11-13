'''
Author       : noeru_desu
Date         : 2021-09-25 20:45:37
LastEditors  : noeru_desu
LastEditTime : 2021-11-13 11:42:30
Description  : 单文件解密功能
'''
from os.path import join, split, splitext
from typing import TYPE_CHECKING

from image_encryptor.common.modules.image_encrypt import ImageEncrypt
from image_encryptor.gui.modules.password_verifier import get_image_data
from image_encryptor.gui.utils.utils import ProgressBar

if TYPE_CHECKING:
    from PIL.Image import Image
    from image_encryptor.gui.frame.main_frame import MainFrame


def main(frame: 'MainFrame', logger, gauge, image: 'Image', save: bool):
    image_data, error = get_image_data(frame.loaded_image_path, password_dict=frame.program.password_dict)
    if error is not None:
        frame.error(error, '读取加密参数时出现问题')
        return frame.initial_preview
    image_encrypt = ImageEncrypt(image, image_data['row'], image_data['col'], image_data['password'])
    logger('正在处理')

    step_count = 0
    if image_data['upset'] or image_data['flip'] or image_data['rgb_mapping']:
        step_count += 2
    if image_data['xor_rgb']:
        step_count += 1
    if save:
        step_count += 1

    bar = ProgressBar(gauge, step_count)

    if image_data['upset'] or image_data['flip'] or image_data['rgb_mapping']:
        bar.next_step(image_data['col'] * image_data['row'])
        logger('正在分割加密图像')
        image_encrypt.init_block_data(True, image_data['upset'], image_data['flip'], image_data['rgb_mapping'], bar)

        logger('正在重组')

        bar.next_step(image_data['col'] * image_data['row'])
        image = image_encrypt.generate_image(bar)

    if image_data['xor_rgb']:
        logger('正在异或解密')
        bar.next_step(1)
        image = image_encrypt.xor_pixels(image_data['xor_alpha'])

    image = image.crop((0, 0, int(image_data['width']), int(image_data['height'])))

    if save:
        bar.next_step(1)
        logger('正在保存文件')
        name, suffix = splitext(split(frame.loaded_image_path)[1])
        suffix = frame.program.EXTENSION_KEYS[frame.selectFormat.Selection]
        if suffix.lower() in ['jpg', 'jpeg']:
            image = image.convert('RGB')
        name = f"{name.replace('-encrypted', '')}-decrypted.{suffix}"

        image.save(join(frame.selectSavePath.Path, name), quality=frame.saveQuality.Value, subsampling=frame.subsamplingLevel.Value)
        bar.finish()
    bar.over()
    logger('完成')
    return image
