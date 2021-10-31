'''
Author       : noeru_desu
Date         : 2021-08-30 21:22:02
LastEditors  : noeru_desu
LastEditTime : 2021-10-31 09:18:34
Description  : 图片加密模块
'''
from math import ceil
import random

import numpy as np
from PIL import Image

flip_func = (
    lambda img: img,
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
)


encrypt_mapping_func = (
    lambda r, g, b, a: (b, r, g, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (g, b, r, a),
)


decrypt_mapping_func = (
    lambda r, g, b, a: (g, b, r, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (b, r, g, a),
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
        self.block_mapping_list = []
        '''resized_image = Image.new("RGBA", self.ceil_size)
        resized_image.paste(image, (0, 0))
        self.pixel_array = array(resized_image, uint8)'''
        self.image = image
        self.init = False
        self.random = random

    def init_block_data(self, decryption_mode: bool, upset: bool, flip: bool, rgb_mapping: bool, bar):
        '''
        :description: 生成打乱后的图片分块、翻转分块，与每个分块所在的坐标列表
        '''
        assert not self.init, 'ImageEncrypt instance has been initialized.'
        self.init = True
        self.decryption_mode = decryption_mode
        self.upset = upset
        self.flip = flip
        self.rgb_mapping = rgb_mapping
        for y in range(self.row):
            for x in range(self.col):
                block_pos = (x * self.block_width, y * self.block_height)
                self.block_pos_list.append(block_pos)
                self.block_list.append(self.image.crop((*block_pos, block_pos[0] + self.block_width, block_pos[1] + self.block_height)))
                bar.update(bar.value + 1)
        self.random.seed(self.random_seed)
        if upset:
            if decryption_mode:
                self.random.shuffle(self.block_pos_list)
            else:
                self.random.shuffle(self.block_list)
        if flip or rgb_mapping:
            self.block_mapping_list = ([1, 2, 3, 0] * ceil(self.block_num / 4))[:self.block_num]
        self.random.seed(self.random_seed)
        self.random.shuffle(self.block_mapping_list)
        bar.finish()

    def generate_image(self, bar):
        '''
        :description: 生成处理后的图片
        :return: 处理后的图片
        '''
        assert self.init, 'ImageEncrypt instance is not initialized.'
        self.image = Image.new('RGBA', self.ceil_size)
        mapping_func = decrypt_mapping_func if self.decryption_mode else encrypt_mapping_func
        block_list = None
        if self.flip and self.rgb_mapping:
            if block_list is None:
                block_list = []
            for block, pos, mapping in zip(self.block_list, self.block_pos_list, self.block_mapping_list):
                block = Image.merge('RGBA', mapping_func[mapping](*flip_func[mapping](block).split()))
                self.image.paste(block, pos)
                bar.update(bar.value + 1)
        elif self.flip:
            if block_list is None:
                block_list = []
            for block, pos, mapping in zip(self.block_list, self.block_pos_list, self.block_mapping_list):
                self.image.paste(flip_func[mapping](block), pos)
                bar.update(bar.value + 1)
        elif self.rgb_mapping:
            if block_list is None:
                block_list = []
            for block, pos, mapping in zip(self.block_list, self.block_pos_list, self.block_mapping_list):
                block = Image.merge('RGBA', mapping_func[mapping](*block.split()))
                self.image.paste(block, pos)
                bar.update(bar.value + 1)
        else:
            for block, pos in zip(self.block_list, self.block_pos_list):
                self.image.paste(block, pos)
                bar.update(bar.value + 1)
        bar.finish()
        return self.image

    def xor_pixels(self, xor_alpha: bool, thread_pool=None, thread_count: int = None):
        '''
        :description: 异或图片中每个像素点的RGB(A)通道
        :return: 异或后的图片
        '''
        self.random.seed(self.random_seed)
        xor_num = self.random.randrange(256)
        pixel_array = np.array(self.image, np.uint8)
        if not xor_alpha:
            alpha_pixel_array = pixel_array[:, :, 3]
            pixel_array = pixel_array[:, :, :3]
        pixel_array ^= xor_num
        if not xor_alpha:
            pixel_array = np.dstack((pixel_array, alpha_pixel_array))
        self.image = Image.fromarray(pixel_array)
        return self.image
