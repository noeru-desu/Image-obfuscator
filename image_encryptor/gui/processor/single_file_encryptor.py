'''
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2021-10-26 21:32:42
Description  : 单文件加密功能
'''
from json import dumps
from os.path import join, split, splitext

from Crypto.Cipher import AES
from PIL import Image

from image_encryptor.common.modules.image_encrypt import ImageEncrypt
from image_encryptor.common.utils.AES import encrypt
from image_encryptor.gui.modules.loader import load_program
from image_encryptor.gui.utils.utils import ProgressBar


def main(frame, logger, gauge, image: Image.Image, save: bool):
    program = load_program()

    password = 100 if frame.password.Value == 'none' else frame.password.Value
    if save:
        has_password = True if frame.password.Value != 'none' else False
        name, suffix = splitext(split(program.data.loaded_image_path)[1])
        suffix = Image.EXTENSION_KEYS[frame.selectFormat.Selection]
        suffix = suffix.strip('.')
        original_image_size = image.size

        if suffix in ('jpg', 'jpeg', 'wmf', 'webp'):
            if frame.rgbMapping.IsChecked():
                frame.warning('注意：当前保存格式为有损压缩格式，在此情况下，使用RGB(A)随机映射会导致图片在解密后出现轻微的分界线', '不可逆处理警告')
            if frame.xorRgb.Selection != 0:
                frame.warning('注意：当前保存格式为有损压缩格式，在此情况下，使用异或加密会导致图片解密后出现严重失真', '不可逆处理警告')

    step_count = 0
    if frame.normalEncryption.IsChecked():
        step_count += 2
    if frame.xorRgb.Selection != 0:
        step_count += 1
    if save:
        step_count += 1

    image_encrypt = ImageEncrypt(image, frame.row.Value, frame.col.Value, password)
    logger('开始处理')

    bar = ProgressBar(gauge, step_count)

    if frame.normalEncryption.IsChecked():
        block_num = frame.row.Value * frame.col.Value
        logger('正在分割原图')
        bar.next_step(block_num)
        image_encrypt.init_block_data(image, False, bar)

        logger('正在重组')
        bar.next_step(block_num)
        image = image_encrypt.get_image(image, frame.rgbMapping.IsChecked(), bar)

    if frame.xorRgb.Selection != 0:
        bar.next_step(1)
        logger('正在异或加密')
        image = image_encrypt.xor_pixels(image, True if frame.xorRgb.Selection == 2 else False)
        bar.finish()

    if save:
        bar.next_step(1)
        logger('完成，正在保存文件')
        name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
        output_path = join(frame.selectSavePath.Path, name)
        if suffix.lower() in ['jpg', 'jpeg']:
            image.convert('RGB')

        image.save(output_path, quality=frame.saveQuality.Value, subsampling=frame.subsamplingLevel.Value)

        json = {
            'width': original_image_size[0],
            'height': original_image_size[1],
            'col': frame.col.Value,
            'row': frame.row.Value,
            'has_password': has_password,
            'password_base64': encrypt(AES.MODE_CFB, password, 'PASS', base64=True) if has_password else 0,
            'normal_encryption': frame.normalEncryption.IsChecked(),
            'rgb_mapping': frame.rgbMapping.IsChecked(),
            'xor_rgb': True if frame.xorRgb.Selection != 0 else False,
            'xor_alpha': True if frame.xorRgb.Selection == 2 else False,
            'version': 2
        }

        with open(output_path, "a") as f:
            f.write('\n' + dumps(json, separators=(',', ':')))
        bar.finish()
    bar.over()
    logger('完成')
    return image, save
