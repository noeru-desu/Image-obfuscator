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

w = program.parameter['col'] if 'col' in program.parameter else 25
h = program.parameter['row'] if 'row' in program.parameter else 25
pw = program.parameter['password'] if 'password' in program.parameter else 100

weight = ceil(size[0] / w)
height = ceil(size[1] / h)
program.logger.info(f'单位大小：{weight}x{height}')
program.logger.info('正在处理')

regions = []
keys = []
for y in range(h):
    for x in range(w):
        keys.append((x * weight, y * height))

seed(pw)
shuffle(keys)

for j in range(h):
    for i in range(w):
        box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
        regions.append(img.crop(box))

index = -1
new_image = Image.new('RGB', (weight * w, height * h))
for i in keys:
    index += 1
    new_image.paste(regions[index], i)

program.logger.info('完成')
name, suffix = splitext(program.parameter['path'])
name.replace('-encrypted', '')
new_image.save(name + '-decrypted' + suffix)
