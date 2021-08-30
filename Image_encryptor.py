from math import ceil
from os.path import join, normpath, split, splitext
from random import seed, shuffle

from Crypto.Cipher import AES
from PIL import Image

from modules.AES import encrypt
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

w = int(program.parameter['col']) if 'col' in program.parameter else 25
h = int(program.parameter['row']) if 'row' in program.parameter else 25
pw = program.parameter['password'] if 'password' in program.parameter else 100
pw = 100 if pw == '100' else pw
has_pw = True if pw != 100 else False

weight = ceil(size[0] / w)
height = ceil(size[1] / h)
program.logger.info(f'分块数量：{w}x{h}; 分块大小：{weight}x{height}')
program.logger.info('正在处理')

regions = []
flip_list = []
num = 0
for j in range(h):
    for i in range(w):
        num += 1
        flip_list.append(num % 4)
        box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
        regions.append(img.crop(box))

seed(pw)
shuffle(regions)
seed(pw)
shuffle(flip_list)

new_image = Image.new('RGB', (weight * w, height * h))
program.logger.info(f'补全后大小：{weight * w}x{height * h}')
index = -1
for y in range(h):
    for x in range(w):
        index += 1
        if flip_list[index] == 1:
            regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
        elif flip_list[index] == 2:
            regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
        elif flip_list[index] == 3:
            regions[index] = regions[index].transpose(Image.FLIP_LEFT_RIGHT)
            regions[index] = regions[index].transpose(Image.FLIP_TOP_BOTTOM)
        new_image.paste(regions[index], (x * weight, y * height))


program.logger.info('完成，正在保存文件')
name, suffix = splitext(program.parameter['path'])
name = name.replace('-decrypted', '') + '-encrypted' + suffix
path, file = split(program.parameter['path'])
new_image.save(name, quality=100)
with open(join(path, name), "a") as f:
    if has_pw:
        f.write('\n' + f"{size[0]},{size[1]},{w},{h},T,{encrypt(AES.MODE_CFB, pw, 'PASS', str(size[0]) + str(size[1]), True)}")
    else:
        f.write('\n' + f'{size[0]},{size[1]},{w},{h},F,0')
