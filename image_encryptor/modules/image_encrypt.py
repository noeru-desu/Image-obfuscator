'''
Author       : noeru_desu
Date         : 2021-08-30 21:22:02
LastEditors  : noeru_desu
LastEditTime : 2021-10-16 21:05:25
Description  : 图片加密模块
'''
from math import ceil
from random import randrange, seed, shuffle

from PIL import Image

flip_func = (
    lambda img: img,
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
)


mapping_func = (
    lambda r, g, b, a: (b, r, g, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (g, b, r, a),
)


class ImageEncrypt(object):
    '''
    用于图像的加解密
    '''
    def __init__(self, image: Image.Image, row: int, col: int, random_seed):
        '''
        :param image: 需要加密的图片
        :param row: 切割行数
        :param col: 切割列数
        :param random_seed: 加密密码
        '''
        self.row = row
        self.col = col
        self.random_seed = random_seed
        self.block_num = row * col
        self.block_width = ceil(image.size[0] / col)
        self.block_height = ceil(image.size[1] / row)
        self.ceil_size = (self.block_width * col, self.block_height * row)
        self.block_list = []
        self.block_pos_list = []
        self.block_flip_list = []

    def init_block_data(self, image: Image.Image, decryption_mode: bool, bar):
        '''
        :description: 生成打乱后的图片分块、翻转分块，与每个分块所在的坐标列表
        '''
        for y in range(self.row):
            for x in range(self.col):
                block_pos = (x * self.block_width, y * self.block_height)
                self.block_pos_list.append(block_pos)
                self.block_list.append(image.crop((block_pos[0], block_pos[1], block_pos[0] + self.block_width, block_pos[1] + self.block_height)))
                bar.update(bar.value + 1)
        self.block_flip_list = ([1, 2, 3, 0] * ceil(self.block_num / 4))[:self.block_num]
        seed(self.random_seed)
        if decryption_mode:
            shuffle(self.block_pos_list)
        else:
            shuffle(self.block_list)
        seed(self.random_seed)
        shuffle(self.block_flip_list)
        bar.finish()

    def get_encrypted_image(self, image: Image.Image, rgb_mapping: bool, bar):
        '''
        :description: 生成加密后的图片
        :return: 加密后的图片
        '''
        image = Image.new('RGBA', self.ceil_size)
        if rgb_mapping:
            for block, pos, flip in zip(self.block_list, self.block_pos_list, self.block_flip_list):
                block = Image.merge('RGBA', mapping_func[flip](*flip_func[flip](block).split()))
                image.paste(block, pos)
                bar.update(bar.value + 1)
        else:
            for block, pos, flip in zip(self.block_list, self.block_pos_list, self.block_flip_list):
                block = flip_func[flip](block)
                image.paste(block, pos)
                bar.update(bar.value + 1)
        bar.finish()
        return image

    def get_decrypted_image(self, image: Image.Image, rgb_mapping: bool, bar):
        '''
        :description: 生成解密后的图片
        :return: 解密后的图片
        '''
        image = Image.new('RGBA', self.ceil_size)
        if rgb_mapping:
            for block, pos, flip in zip(self.block_list, self.block_pos_list, self.block_flip_list):
                block = Image.merge('RGBA', mapping_func[flip](*flip_func[flip](block).split()))
                image.paste(block, pos)
                bar.update(bar.value + 1)
        else:
            for block, pos, flip in zip(self.block_list, self.block_pos_list, self.block_flip_list):
                block = flip_func[flip](block)
                image.paste(block, pos)
                bar.update(bar.value + 1)
        bar.finish()
        return image

    def _xor_pixel_data(self, pixel_data, xor_num: int, xor_alpha: bool):
        '''
        :description: 异或每个像素点的RGB(A)通道
        :return: 二维列表，包含被异或后的每个像素点各通道的值[[r, g, b, a], [r, g, b, a], ...]
        '''
        if xor_alpha:
            return [(r ^ xor_num, g ^ xor_num, b ^ xor_num, a ^ xor_num) for r, g, b, a in pixel_data]
        else:
            return [(r ^ xor_num, g ^ xor_num, b ^ xor_num, a) for r, g, b, a in pixel_data]

    def xor_pixels(self, image: Image.Image, xor_alpha: bool, process_pool=None, process_count: int = None):
        '''
        :description: 异或图片中每个像素点的RGB(A)通道
        :return: 异或后的图片
        '''
        seed(self.random_seed)
        xor_num = randrange(256)
        pixel_list = list(image.getdata())
        future_list = []
        if process_pool is None:
            pixel_list = self._xor_pixel_data(pixel_list, xor_num, xor_alpha)
        else:
            num = 0
            for i in range(0, len(pixel_list), ceil(len(pixel_list) / process_count)):
                if i == 0:
                    continue
                future_list.append(process_pool.submit(self._xor_pixel_data, pixel_list[num:i], xor_num, xor_alpha))
                num = i
            future_list.append(process_pool.submit(self._xor_pixel_data, pixel_list[num:], xor_num, xor_alpha))
            pixel_list = []
            for i in future_list:
                pixel_list.extend(i.result())
        image.putdata(pixel_list)
        return image
