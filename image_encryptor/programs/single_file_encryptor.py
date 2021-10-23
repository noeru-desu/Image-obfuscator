'''
Author       : noeru_desu
Date         : 2021-09-25 20:43:02
LastEditors  : noeru_desu
LastEditTime : 2021-10-23 11:46:31
Description  : 单文件加密功能
'''
from json import dumps
from os.path import join, split, splitext
from sys import exit

from Crypto.Cipher import AES

from image_encryptor.modules.image_encrypt import ImageEncrypt
from image_encryptor.modules.loader import load_program
from image_encryptor.utils.AES import encrypt
from image_encryptor.utils.utils import calculate_formula_string, open_image, pause


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

    if isinstance(program.parameters['row'], str):
        program.parameters['row'], error = calculate_formula_string(program.parameters['row'], width=image.size[0], height=image.size[1])
        if error is not None:
            program.logger.error('动态运算切割行数参数时出现错误：')
            program.logger.error(error)
            pause()
            exit()
        elif program.parameters['row'] < 1:
            program.logger.error(f"动态运算的切割行数参数不正确：切割行数小于1 (结果为{program.parameters['row']})")
            pause()
            exit()
        elif program.parameters['row'] > image.size[1]:
            program.logger.error(f"动态运算的切割行数参数不正确：切割行数大于图片宽度 (结果为{program.parameters['row']})")
            pause()
            exit()

    if isinstance(program.parameters['col'], str):
        program.parameters['col'], error = calculate_formula_string(program.parameters['col'], width=image.size[0], height=image.size[1])
        if error is not None:
            program.logger.error('动态运算切割列数参数时出现错误：')
            program.logger.error(error)
            pause()
            exit()
        elif program.parameters['col'] < 1:
            program.logger.error(f"动态运算的切割列数参数不正确：切割列数小于1 (结果为{program.parameters['col']})")
            pause()
            exit()
        elif program.parameters['col'] > image.size[0]:
            program.logger.error(f"动态运算的切割列数参数不正确：切割列数大于图片宽度 (结果为{program.parameters['col']})")
            pause()
            exit()

    has_password = True if program.parameters['password'] != 100 else False
    name, suffix = splitext(split(program.parameters['input_path'])[1])
    suffix = program.parameters['format'] if program.parameters['format'] is not None else 'png'
    suffix = suffix.strip('.')

    if suffix in ('jpg', 'jpeg', 'wmf', 'webp'):
        program.logger.warning('当前保存格式为有损压缩格式')
        if program.parameters['mapping']:
            program.logger.warning('在此情况下，使用RGB(A)随机映射会导致图片在解密后出现轻微的分界线，按任意键确定')
            pause()
        if program.parameters['xor_rgb']:
            program.logger.warning('在此情况下，使用异或加密会导致图片解密后出现严重失真，按任意键确定')
            pause()

    widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
    image_encrypt = ImageEncrypt(image, program.parameters['row'], program.parameters['col'], program.parameters['password'])
    original_image = image.size
    program.logger.info(f"分块数量：{program.parameters['col']}x{program.parameters['row']}; 分块大小：{image_encrypt.block_width}x{image_encrypt.block_height}")
    program.logger.info('开始处理')

    if program.parameters['normal_encryption']:
        program.logger.info('正在分割原图')
        bar = ProgressBar(max_value=program.parameters['col'] * program.parameters['row'], widgets=widgets)
        image_encrypt.init_block_data(image, False, bar)

        program.logger.info(f"分割完成，补全后大小：{image_encrypt.block_width * program.parameters['col']}x{image_encrypt.block_height * program.parameters['row']}")

        program.logger.info('正在重组')
        bar = ProgressBar(max_value=program.parameters['col'] * program.parameters['row'], widgets=widgets)
        image = image_encrypt.get_image(image, program.parameters['mapping'], bar)

    if program.parameters['xor_rgb']:
        program.logger.info('正在异或加密，性能较低，请耐心等待')
        image = image_encrypt.xor_pixels(image, program.parameters['xor_alpha'], program.process_pool, program.parameters['process_count'])

    program.logger.info('完成，正在保存文件')
    name = f"{name.replace('-decrypted', '')}-encrypted.{suffix}"
    output_path = join(program.parameters['output_path'], name)
    if suffix.lower() in ['jpg', 'jpeg']:
        image.convert('RGB')

    image.save(output_path, quality=95, subsampling=0)

    json = {
        'width': original_image[0],
        'height': original_image[1],
        'col': program.parameters['col'],
        'row': program.parameters['row'],
        'has_password': has_password,
        'password_base64': encrypt(AES.MODE_CFB, program.parameters['password'], 'PASS', base64=True) if has_password else 0,
        'normal_encryption': program.parameters['normal_encryption'],
        'rgb_mapping': program.parameters['mapping'],
        'xor_rgb': program.parameters['xor_rgb'],
        'xor_alpha': program.parameters['xor_alpha'],
        'version': 2
    }

    with open(output_path, "a") as f:
        f.write('\n' + dumps(json, separators=(',', ':')))
