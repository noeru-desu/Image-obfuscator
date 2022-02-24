"""
Author       : noeru_desu
Date         : 2021-08-30 21:22:02
LastEditors  : noeru_desu
LastEditTime : 2022-02-24 21:14:21
Description  : 图片加密模块
"""
from abc import ABC
import random
from math import ceil

from numpy.random import randint
from numpy import array, uint8
from PIL import Image

from image_encryptor.utils.image import gen_mapping_table, random_noise
from image_encryptor.utils.utils import FakeBar

flip_func = (
    lambda img: img,
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
)


old_encrypt_mapping_func = (
    lambda r, g, b, a: (b, r, g, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (g, b, r, a)
)


old_decrypt_mapping_func = (
    lambda r, g, b, a: (g, b, r, a),
    lambda r, g, b, a: (g, r, b, a),
    lambda r, g, b, a: (b, g, r, a),
    lambda r, g, b, a: (b, r, g, a)
)

channel_num = {'r': 0, 'g': 1, 'b': 2, 'a': 3}


class ImageEncryptBase(ABC):
    """
    用于图像的加解密
    """
    random = random

    def __init__(self, image: Image.Image, row: int, col: int, random_seed):
        """
        :param image: 需要加密的图片
        :param row: 切割行数
        :param col: 切割列数
        :param random_seed: 加密密码
        """
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

    def init_block_data(self, decryption_mode: bool, shuffle: bool, flip: bool, mapped_channels: str, old_mapping: bool, bar=FakeBar):
        """
        :old_mapping: 用于1.0.0-rc.12版本前的RGB随机映射, 为保证兼容性而保留
        :description: 生成打乱后的图片分块、翻转分块, 与每个分块所在的坐标列表
        """
        assert not self.init, 'ImageEncrypt instance has been initialized.'
        self.init = True
        self.decryption_mode = decryption_mode
        self.shuffle = shuffle
        self.flip = flip
        # 使用对应的映射表
        if old_mapping:
            self.mapped_channels = mapped_channels
            self.encryption_mapping_table = old_encrypt_mapping_func
            self.decryption_mapping_table = old_decrypt_mapping_func
        elif len(mapped_channels) > 1:
            self.mapped_channels = mapped_channels
            self.encryption_mapping_table, self.decryption_mapping_table = gen_mapping_table(mapped_channels)
        else:
            self.mapped_channels = False
            self.encryption_mapping_table, self.decryption_mapping_table = None, None
        # 切割图片并记录坐标
        for y in range(self.row):
            for x in range(self.col):
                block_pos = (x * self.block_width, y * self.block_height)
                self.block_pos_list.append(block_pos)
                self.block_list.append(self.image.crop((*block_pos, block_pos[0] + self.block_width, block_pos[1] + self.block_height)))
                bar.update(bar.value + 1)
        # 随机打乱
        if shuffle:
            self.random.seed(self.random_seed)
            if decryption_mode:
                self.random.shuffle(self.block_pos_list)
            else:
                self.random.shuffle(self.block_list)
        # 随机翻转
        if flip:
            self.block_flip_list = ([1, 2, 3, 0] * ceil(self.block_num / 4))[:self.block_num]
            self.random.seed(self.random_seed)
            self.random.shuffle(self.block_flip_list)
        if old_mapping and flip:
            self.block_mapping_list = self.block_flip_list
        elif old_mapping:
            self.block_mapping_list = ([1, 2, 3, 0] * ceil(self.block_num / 4))[:self.block_num]
            self.random.seed(self.random_seed)
            self.random.shuffle(self.block_mapping_list)
        else:
            if self.encryption_mapping_table is not None:
                if len(self.encryption_mapping_table) != 1:
                    self.block_mapping_list = (list(range(len(self.encryption_mapping_table))) * ceil(self.block_num / len(self.encryption_mapping_table)))[:self.block_num]
                else:
                    self.block_mapping_list = ([0] * ceil(self.block_num))
        if not old_mapping:
            self.random.seed(self.random_seed)
            self.random.shuffle(self.block_mapping_list)
        bar.finish()

    def generate_image(self, bar=FakeBar):
        """
        :description: 生成处理后的图片
        :return: 处理后的图片
        """
        assert self.init, 'ImageEncrypt instance is not initialized.'
        self.image = Image.new('RGBA', self.ceil_size)
        mapping_func = self.decryption_mapping_table if self.decryption_mode else self.encryption_mapping_table
        block_list = None
        if self.flip and self.mapped_channels:
            if block_list is None:
                block_list = []
            for block, pos, flip, mapping in zip(self.block_list, self.block_pos_list, self.block_flip_list, self.block_mapping_list):
                block = Image.merge('RGBA', mapping_func[mapping](*flip_func[flip](block).split()))
                self.image.paste(block, pos)
                bar.update(bar.value + 1)
        elif self.flip:
            if block_list is None:
                block_list = []
            for block, pos, flip in zip(self.block_list, self.block_pos_list, self.block_flip_list):
                self.image.paste(flip_func[flip](block), pos)
                bar.update(bar.value + 1)
        elif self.mapped_channels:
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

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255):
        """
        :description: 异或图片中每个像素点的RGB(A)通道
        :return: 异或后的图片
        """
        pixel_array = array(self.image, uint8)
        if noise:
            noise_array = random_noise(*self.image.size, len(channels), self.random_seed, noise_factor)
            for index, channel in enumerate(channels):
                pixel_array[:, :, channel_num[channel]] ^= noise_array[:, :, index]
        else:
            self.random.seed(self.random_seed)
            xor_num = self.random.randrange(256)
            for channel in channels:
                pixel_array[:, :, channel_num[channel]] ^= xor_num
        self.image = Image.fromarray(pixel_array)
        return self.image


class ImageEncrypt(ImageEncryptBase):
    def init_block_data(self, shuffle: bool, flip: bool, mapped_channels: str, bar):
        return super().init_block_data(False, shuffle, flip, mapped_channels, False, bar)


class ImageDecrypt(ImageEncryptBase):
    def init_block_data(self, shuffle: bool, flip: bool, mapped_channels: str, old_mapping: bool, bar):
        return super().init_block_data(True, shuffle, flip, mapped_channels, old_mapping, bar)


class AntiHarmony(object):
    def __init__(self, image: 'Image.Image'):
        self.image = image
        self.right_pos = self.image.size[0] - 1
        self.button_pos = self.image.size[1] - 1

    def generate_image(self):
        self.image.putpixel((0, 0), (randint(256), randint(256), randint(256)))
        self.image.putpixel((self.right_pos, 0), (randint(256), randint(256), randint(256)))
        self.image.putpixel((0, self.button_pos), (randint(256), randint(256), randint(256)))
        self.image.putpixel((self.right_pos, self.button_pos), (randint(256), randint(256), randint(256)))
        return self.image
