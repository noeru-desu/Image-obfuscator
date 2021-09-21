from json import loads
from math import ceil
from os.path import normpath, splitext
from sys import exit

from Crypto.Cipher import AES
from PIL import Image
from progressbar import Bar, Percentage, ProgressBar, SimpleProgress

from modules.AES import decrypt
from modules.image_cryptor import generate_decrypted_image, get_mapping_lists, XOR_image
from modules.loader import get_instances

program = get_instances()

if 'path' not in program.parameter:
    program.logger.error('没有输入文件')
    exit()
program.parameter['path'] = normpath(program.parameter['path'])
img = Image.open(program.parameter['path']).convert('RGBA')
size = img.size
program.logger.info(f'导入大小：{size[0]}x{size[1]}')
data = None

with open(program.parameter['path'], 'rb') as f:
    offset = -35
    while True:
        f.seek(offset, 2)
        lines = f.readlines()
        if len(lines) >= 2:
            last_line = lines[-1]
            break
        offset *= 2
    data = last_line.decode()

image_data = loads(data)
pw = 100
if image_data['has_password']:
    input_pw = ''
    while True:
        input_pw = input('需要解密的图片被密码保护，请输入密码：')
        if input_pw == '':
            continue
        try:
            if decrypt(AES.MODE_CFB, input_pw, image_data['password_base64'], str(image_data['width']) + str(image_data['height']), True) == 'PASS':
                break
            else:
                program.logger.warning('密码错误！')
        except UnicodeDecodeError:
            program.logger.warning('密码错误！')
    pw = input_pw
program.logger.info(f"原始图片信息：大小：{image_data['width']}x{image_data['height']}; 分块数量：{image_data['col']}x{image_data['row']}")

block_width = ceil(size[0] / image_data['col'])
block_height = ceil(size[1] / image_data['row'])
program.logger.info(f'分块大小：{block_width}x{block_height}')
widgets = [Percentage(), ' ', SimpleProgress(), ' ', Bar('█'), ' ']
program.logger.info('正在处理')
program.logger.info('正在生成映射列表')

bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
regions, pos_list, flip_list = get_mapping_lists(img, pw, image_data['row'], image_data['col'], block_width, block_height, bar)

program.logger.info('正在重组')

bar = ProgressBar(max_value=image_data['col'] * image_data['row'], widgets=widgets)
new_image = generate_decrypted_image(regions, pos_list, flip_list, image_data['row'], image_data['col'], block_width, block_height, image_data['rgb_mapping'], bar)

if image_data['rgb_mapping']:
    program.logger.info('正在异或加密')
    size = new_image.size
    bar = ProgressBar(max_value=size[0] * size[1], widgets=widgets)
    new_image = XOR_image(new_image, pw, image_data['xor_alpha'], bar)

program.logger.info('正在保存文件')
original_image = new_image.crop((0, 0, int(image_data['width']), int(image_data['height'])))
name, suffix = splitext(program.parameter['path'])
name = name.replace('-encrypted', '')
original_image.save(name + '-decrypted' + suffix, quality=100)
