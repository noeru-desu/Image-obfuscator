from base64 import encodebytes as base64_encodebytes
from math import ceil
from os.path import normpath, splitext
from random import seed, shuffle

from Crypto.Cipher import AES
from PIL import Image

from modules.loader import get_instances


def add_to_16(par):
    par = par.encode()
    while len(par) % 16 != 0:
        par += b'\x00'
    return par


program = get_instances()

if 'path' not in program.parameter:
    program.logger.error('没有输入文件')
    exit()
program.parameter['path'] = normpath(program.parameter['path'])
img = Image.open(program.parameter['path'])
size = img.size
program.logger.info(f'导入大小：{size[0]}x{size[1]}')
data = None

with open(program.parameter['path'], 'rb') as f:
    offset = -25
    while True:
        f.seek(offset, 2)
        lines = f.readlines()
        if len(lines) >= 2:
            last_line = lines[-1]
            break
        offset *= 2
    data = last_line.decode()


o_width, o_height, w, h, has_pw, o_base64 = data.split(',')
o_base64 = o_base64.replace('\r', '').replace('\n', '')
pw = 100
if has_pw == 'T':
    input_pw = ''
    while True:
        input_pw = input('需要解密的图片被密码保护，请输入密码：')
        if input_pw == '':
            continue
        aes = AES.new(add_to_16(input_pw), AES.MODE_ECB)
        en_text = aes.encrypt(add_to_16('PASS'))
        base64 = base64_encodebytes(en_text).replace(b'\n', b'')
        if base64.decode() == o_base64:
            break
        else:
            program.logger.warning('密码错误！')
    pw = input_pw
w = int(w)
h = int(h)
program.logger.info(f'原始图片信息：大小：{o_width}x{o_height}; 分块数量：{w}x{h}')

width = ceil(size[0] / w)
height = ceil(size[1] / h)
program.logger.info(f'单位大小：{width}x{height}')
program.logger.info('正在处理')

regions = []
keys = []
flip_list = []

num = 0
for y in range(h):
    for x in range(w):
        num += 1
        flip_list.append(num % 4)
        keys.append((x * width, y * height))

seed(pw)
shuffle(keys)
seed(pw)
shuffle(flip_list)

for j in range(h):
    for i in range(w):
        box = (width * i, height * j, width * (i + 1), height * (j + 1))
        regions.append(img.crop(box))

index = -1
new_image = Image.new('RGB', (width * w, height * h))
for i in keys:
    index += 1
    if flip_list[index] == 1:
        regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_list[index] == 2:
        regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
    elif flip_list[index] == 3:
        regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
        regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
    new_image.paste(regions[index], i)

program.logger.info('完成，正在保存文件')
original_image = new_image.crop((0, 0, int(o_width), int(o_height)))
name, suffix = splitext(program.parameter['path'])
name = name.replace('-encrypted', '')
original_image.save(name + '-decrypted' + suffix, quality=100)
