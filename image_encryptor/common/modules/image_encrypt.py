'''
Author       : noeru_desu
Date         : 2021-08-30 21:22:02
LastEditors  : noeru_desu
LastEditTime : 2021-11-28 14:45:43
Description  : 图片加密模块
'''
import random
from math import ceil

from numpy import random as np_random
from numpy import array, squeeze, uint8
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

channel_num = {'r': 0, 'g': 1, 'b': 2, 'a': 3}


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

    def init_block_data(self, decryption_mode: bool, shuffle: bool, flip: bool, rgb_mapping: bool, bar):
        '''
        :description: 生成打乱后的图片分块、翻转分块，与每个分块所在的坐标列表
        '''
        assert not self.init, 'ImageEncrypt instance has been initialized.'
        self.init = True
        self.decryption_mode = decryption_mode
        self.shuffle = shuffle
        self.flip = flip
        self.rgb_mapping = rgb_mapping
        for y in range(self.row):
            for x in range(self.col):
                block_pos = (x * self.block_width, y * self.block_height)
                self.block_pos_list.append(block_pos)
                self.block_list.append(self.image.crop((*block_pos, block_pos[0] + self.block_width, block_pos[1] + self.block_height)))
                bar.update(bar.value + 1)
        self.random.seed(self.random_seed)
        if shuffle:
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

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255):
        '''
        :description: 异或图片中每个像素点的RGB(A)通道
        :return: 异或后的图片
        '''
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


def random_noise(width: int, height: int, nc: int, seed, factor: int, ndarray=True):
    '''Generator a random noise image from numpy.array.

    If nc is 1, the Grayscale image will be created.
    If nc is 3, the RGB image will be generated.
    If nc is 4, the RGBA image will be generated.

    Args:
        nc (int): (1, 3 or 4) number of channels.
        width (int): width of output image.
        height (int): height of output image.
    Returns:
        PIL Image.
    '''
    if factor > 255:
        factor = 255
    elif factor < 1:
        factor = 1
    random.seed(seed)
    seed = random.randrange(0, 2 ** 32)
    np_random.seed(seed)
    image = (np_random.rand(height, width, nc) * factor).astype(uint8)
    if ndarray:
        return image
    else:
        if nc == 1:
            return Image.fromarray(squeeze(image), mode='L')
        elif nc == 3:
            return Image.fromarray(image, mode='RGB')
        elif nc == 4:
            return Image.fromarray(image, mode='RGBA')
        else:
            raise ValueError(f'Input nc should be 1/3/4. Got {nc}.')
