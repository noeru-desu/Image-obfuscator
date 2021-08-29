from PIL import Image
from random import shuffle, seed
from modules.loader import get_instances
from math import ceil
from os.path import normpath, splitext

program = get_instances()

if 'path' not in program.parameter:
    program.logger.error('没有输入文件')
    exit()
program.parameter['path'] = normpath(program.parameter['path'])
img = Image.open(program.parameter['path'])
size = img.size
program.logger.info(f'导入大小：{size[0]}x{size[1]}')

w = program.parameter['col'] if 'col' in program.parameter else 10
h = program.parameter['row'] if 'row' in program.parameter else 10
pw = program.parameter['password'] if 'password' in program.parameter else 100

weight = ceil(size[0] / w)
height = ceil(size[1] / h)
program.logger.info(f'单位大小：{weight}x{height}')
program.logger.info('正在处理')

regions = []
for j in range(h):
    for i in range(w):
        box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
        regions.append(img.crop(box))

seed(pw)
shuffle(regions)

index = -1
new_image = Image.new('RGB', (weight * w, height * h))
program.logger.info(f'补全后大小：{weight * w}x{height * h}')
for y in range(h):
    for x in range(w):
        index += 1
        new_image.paste(regions[index], (x * weight, y * height))

program.logger.info('完成')
name, suffix = splitext(program.parameter['path'])
name.replace('-decrypted', '')
new_image.save(name + '-encrypted' + suffix)
