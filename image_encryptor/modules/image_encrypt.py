"""
Author       : noeru_desu
Date         : 2021-08-30 21:22:02
LastEditors  : noeru_desu
LastEditTime : 2022-03-08 20:29:41
Description  : 图片加密模块
"""
from math import ceil
from random import Random
from typing import TYPE_CHECKING, Union

from numpy import ascontiguousarray, hsplit, uint8, vsplit, zeros
from numpy.random import randint
from PIL import Image

from image_encryptor.utils.image import (array_to_image, gen_mapping_table,
                                         merge_channels, random_noise,
                                         split_channels)
from image_encryptor.utils.misc_util import FakeBar

if TYPE_CHECKING:
    from typing import Iterable
    from numpy import ndarray

flip_func = (
    lambda arr: arr,
    lambda arr: arr[:, ::-1],    # 左右翻转
    lambda arr: arr[::-1],       # 上下翻转
    lambda arr: arr[::-1, ::-1]  # 上下左右翻转
)

old_flip_func = (
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
random = Random()


class ImageEncryptBaseV2(object):
    """
    用于图像的加解密(1.0.0-rc.12 ~ 1.2.1)
    """
    __slots__ = (
        'row', 'col', 'block_num', 'block_width', 'block_height', 'ceil_size', 'block_list',
        'block_pos_list', 'block_mapping_list', 'image', 'init', 'decryption_mode', 'shuffle',
        'flip', 'mapped_channels', 'mapping_table', 'block_flip_list', '_shuffle'
    )

    def __init__(self, image: Image.Image, row: int, col: int, random_seed):
        """
        :param image: 需要加密的图片
        :param row: 切割行数
        :param col: 切割列数
        :param random_seed: 加密密码
        """
        self.row = row
        self.col = col
        self.block_num = row * col
        self.block_width = ceil(image.size[0] / col)
        self.block_height = ceil(image.size[1] / row)
        self.ceil_size = (self.block_width * col, self.block_height * row)
        self.block_list = []
        self.block_pos_list = []
        self.block_mapping_list = []
        self.image = image
        self.init = False
        self._shuffle = Shuffle(random_seed)

    def init_block_data(self, decryption_mode: bool, shuffle: bool, flip: bool, mapped_channels: str, bar=FakeBar):
        """
        :description: 生成打乱后的图片分块、翻转分块, 与每个分块所在的坐标列表
        """
        assert not self.init, 'ImageEncrypt instance has been initialized.'
        self.init = True
        self.decryption_mode = decryption_mode
        self.shuffle = shuffle
        self.flip = flip
        # 使用对应的映射表
        if len(mapped_channels) > 1:
            self.mapped_channels = mapped_channels
            self.mapping_table = gen_mapping_table(mapped_channels, decryption_mode)
        else:
            self.mapped_channels = False
            self.mapping_table = None
        # 切割图片并记录坐标
        for y in range(self.row):
            for x in range(self.col):
                block_pos = (x * self.block_width, y * self.block_height)
                self.block_pos_list.append(block_pos)
                self.block_list.append(self.image.crop((*block_pos, block_pos[0] + self.block_width, block_pos[1] + self.block_height)))
                bar.add()
        # 随机打乱
        if shuffle:
            if decryption_mode:
                self._shuffle.obverse(self.block_pos_list)
            else:
                self._shuffle.obverse(self.block_list)
        # 随机翻转
        if flip:
            self.block_flip_list = ([1, 2, 3, 0] * ceil(self.block_num / 4))[:self.block_num]
            self._shuffle.obverse(self.block_flip_list)
        if self.mapping_table is not None:
            if len(self.mapping_table) != 1:
                self.block_mapping_list = (list(range(len(self.mapping_table))) * ceil(self.block_num / len(self.mapping_table)))[:self.block_num]
                self._shuffle.obverse(self.block_mapping_list)
            else:
                self.block_mapping_list = ([0] * self.block_num)
        bar.finish()

    def generate_image(self, bar=FakeBar):
        """
        :description: 生成处理后的图片
        :return: 处理后的图片
        """
        assert self.init, 'ImageEncrypt instance is not initialized.'
        self.image = Image.new('RGBA', self.ceil_size)
        if self.flip and self.mapped_channels:
            for block, pos, flip, mapping in zip(self.block_list, self.block_pos_list, self.block_flip_list, self.block_mapping_list):
                block = Image.merge('RGBA', self.mapping_table[mapping](*old_flip_func[flip](block).split()))
                self.image.paste(block, pos)
                bar.add()
        elif self.flip:
            for block, pos, flip in zip(self.block_list, self.block_pos_list, self.block_flip_list):
                self.image.paste(old_flip_func[flip](block), pos)
                bar.add()
        elif self.mapped_channels:
            for block, pos, mapping in zip(self.block_list, self.block_pos_list, self.block_mapping_list):
                block = Image.merge('RGBA', self.mapping_table[mapping](*block.split()))
                self.image.paste(block, pos)
                bar.add()
        else:
            for block, pos in zip(self.block_list, self.block_pos_list):
                self.image.paste(block, pos)
                bar.add()
        bar.finish()
        return self.image

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255):
        """
        :description: 异或图片中每个像素点的RGB(A)通道
        :return: 异或后的图片
        """
        # ! Image转array时默认shape为(高, 宽, 通道数)，使用与保存时需要将高与宽数值对调
        pixel_array = ascontiguousarray(self.image, uint8)
        w, h = self.image.size
        if noise:
            noise_array = random_noise(h, w, len(channels), self._shuffle.seed, noise_factor)
            for index, channel in enumerate(channels):
                pixel_array[:, :, channel_num[channel]] ^= noise_array[:, :, index]
        else:
            random.seed(self._shuffle.seed)
            xor_num = random.randrange(256)
            for channel in channels:
                pixel_array[:, :, channel_num[channel]] ^= xor_num
        self.image = array_to_image(pixel_array, (w, h))
        return self.image


class ImageEncryptBaseV1(ImageEncryptBaseV2):
    """
    用于图像的加解密(0.1.0 ~ 1.0.0-rc.11)
    """
    __slots__ = ()

    def init_block_data(self, decryption_mode: bool, shuffle: bool, flip: bool, mapped_channels: str, bar=FakeBar):
        """
        :description: 生成打乱后的图片分块、翻转分块, 与每个分块所在的坐标列表
        """
        assert not self.init, 'ImageEncrypt instance has been initialized.'
        self.init = True
        self.decryption_mode = decryption_mode
        self.shuffle = shuffle
        self.flip = flip
        # 使用对应的映射表
        self.mapped_channels = mapped_channels
        self.mapping_table = old_decrypt_mapping_func if decryption_mode else old_encrypt_mapping_func
        # 切割图片并记录坐标
        for y in range(self.row):
            for x in range(self.col):
                block_pos = (x * self.block_width, y * self.block_height)
                self.block_pos_list.append(block_pos)
                self.block_list.append(self.image.crop((*block_pos, block_pos[0] + self.block_width, block_pos[1] + self.block_height)))
                bar.add()
        # 随机打乱
        if shuffle:
            if decryption_mode:
                self._shuffle.obverse(self.block_pos_list)
            else:
                self._shuffle.obverse(self.block_list)
        # 随机翻转
        if flip or mapped_channels:
            self.block_mapping_list = ([1, 2, 3, 0] * ceil(self.block_num / 4))[:self.block_num]
            self._shuffle.obverse(self.block_mapping_list)
        if flip:
            self.block_flip_list = self.block_mapping_list
        bar.finish()


class ImageEncryptBaseV3(object):
    """
    用于图像的加解密(1.3.0 ~)
    """
    # ! Image转换为narray后会逆时针旋转90度，因此处理时宽高需对调
    __slots__ = (
        'row', 'col', 'block_num', 'block_width', 'block_height', 'ceil_size', 'block_list',
        'block_mapping_list', 'image_array', 'init', 'shuffle', 'flip', 'mapped_channels',
        'mapping_table', 'mapping_table', 'block_pos_list', '_shuffle'
    )

    def __init__(self, image: Image.Image, row: int, col: int, random_seed):
        """
        :param image: 需要加密的图片
        :param row: 切割行数
        :param col: 切割列数
        :param random_seed: 加密密码
        """
        self.row = row
        self.col = col
        self.block_num = row * col
        self.block_width = ceil(image.size[0] / col)
        self.block_height = ceil(image.size[1] / row)
        self.ceil_size = (self.block_width * col, self.block_height * row)
        self.block_list = []
        self.block_mapping_list = []
        self.block_pos_list = []
        self.init = False
        self.image_array = zeros((self.ceil_size[1], self.ceil_size[0], 4), uint8)
        self.image_array[0:image.size[1], 0:image.size[0]] = ascontiguousarray(image, uint8)
        self._shuffle = Shuffle(random_seed)

    def init_block_data(self, decryption_mode: bool, shuffle: bool, flip: bool, mapped_channels: str, bar=FakeBar):
        """
        :description: 生成打乱后的图片分块、翻转分块, 与每个分块所在的坐标列表
        """
        assert not self.init, 'ImageEncrypt instance has been initialized.'
        self.init = True
        self.shuffle = shuffle
        self.flip = flip
        # 使用对应的映射表
        if len(mapped_channels) > 1:
            self.mapped_channels = mapped_channels
            self.mapping_table = gen_mapping_table(mapped_channels, decryption_mode)
        else:
            self.mapped_channels = False
            self.mapping_table = None
        # 切割图片并记录坐标
        for i, arr in enumerate(vsplit(self.image_array, self.row)):
            self.block_list.extend(hsplit(arr, self.col))
            h_pos = i * self.block_height
            self.block_pos_list.extend((h_pos, j) for j in range(0, self.ceil_size[0], self.block_width))
            bar.add()
        # 随机映射
        if self.mapping_table is not None:
            if len(self.mapping_table) != 1:
                self.block_mapping_list = (list(range(len(self.mapping_table))) * ceil(self.block_num / len(self.mapping_table)))[:self.block_num]
                self._shuffle.obverse(self.block_mapping_list)
            else:
                self.block_mapping_list = ([0] * self.block_num)
        # 随机打乱
        if self.shuffle:
            if decryption_mode:
                self._shuffle.obverse(self.block_pos_list)
            else:
                self._shuffle.obverse(self.block_list)
        bar.finish()

    def generate_image(self, bar=FakeBar):
        """
        :description: 生成处理后的图片
        :return: 处理后的图片
        """
        assert self.init, 'ImageEncrypt instance is not initialized.'
        random.seed(self._shuffle.seed)
        randbelow = random._randbelow
        new_image_array = zeros((self.ceil_size[1], self.ceil_size[0], 4), uint8)
        if self.flip and self.mapped_channels:
            shape = (self.block_height, self.block_width, 4)
            for block, pos, mapping in zip(self.block_list, self.block_pos_list, self.block_mapping_list):
                h, w = pos
                new_image_array[h:h + self.block_height, w:w + self.block_width] = merge_channels(self.mapping_table[mapping](*split_channels(flip_func[randbelow(4)](block))), shape)
                bar.add()
        elif self.flip:
            for block, pos in zip(self.block_list, self.block_pos_list):
                h, w = pos
                new_image_array[h:h + self.block_height, w:w + self.block_width] = flip_func[randbelow(4)](block)
                bar.add()
        elif self.mapped_channels:
            shape = (self.block_height, self.block_width, 4)
            for block, pos, mapping in zip(self.block_list, self.block_pos_list, self.block_mapping_list):
                h, w = pos
                new_image_array[h:h + self.block_height, w:w + self.block_width] = merge_channels(self.mapping_table[mapping](*split_channels(block)), shape)
                bar.add()
        else:
            for block, pos in zip(self.block_list, self.block_pos_list):
                h, w = pos
                new_image_array[h:h + self.block_height, w:w + self.block_width] = block
                bar.add()
        bar.finish()
        self.image_array = new_image_array
        return new_image_array, self.ceil_size

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255):
        """
        :description: 异或图片中每个像素点的RGB(A)通道
        :return: 异或后的图片
        """
        size = self.image_array.shape[:-1]
        if noise:
            noise_array = random_noise(*size, len(channels), self._shuffle.seed, noise_factor)
            for index, channel in enumerate(channels):
                self.image_array[:, :, channel_num[channel]] ^= noise_array[:, :, index]
        else:
            random.seed(self._shuffle.seed)
            xor_num = random.randrange(256)
            for channel in channels:
                self.image_array[:, :, channel_num[channel]] ^= xor_num
        return self.image_array, size[::-1]


class ImageEncrypt(object):
    __slots__ = ('base',)

    def __init__(self, image: Image.Image, row: int, col: int, random_seed, version=7) -> None:
        if version >= 7:
            self.base = ImageEncryptBaseV3(image, row, col, random_seed)
        elif version >= 5:
            self.base = ImageEncryptBaseV2(image, row, col, random_seed)
        else:
            self.base = ImageEncryptBaseV1(image, row, col, random_seed)

    def init_block_data(self, shuffle: bool, flip: bool, mapped_channels: str, bar):
        return self.base.init_block_data(False, shuffle, flip, mapped_channels, bar)

    def generate_image(self, bar=FakeBar) -> Union[tuple['ndarray', tuple[int, int]], 'Image.Image']:
        return self.base.generate_image(bar)

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255) -> Union[tuple['ndarray', tuple[int, int]], 'Image.Image']:
        return self.base.xor_pixels(channels, noise, noise_factor)


class ImageDecrypt(object):
    __slots__ = ('base',)

    def __init__(self, image: Image.Image, row: int, col: int, random_seed, version=7) -> None:
        if version >= 7:
            self.base = ImageEncryptBaseV3(image, row, col, random_seed)
        elif version >= 5:
            self.base = ImageEncryptBaseV2(image, row, col, random_seed)
        else:
            self.base = ImageEncryptBaseV1(image, row, col, random_seed)

    def init_block_data(self, shuffle: bool, flip: bool, mapped_channels: str, bar):
        return self.base.init_block_data(True, shuffle, flip, mapped_channels, bar)

    def generate_image(self, bar=FakeBar) -> Union[tuple['ndarray', tuple[int, int]], 'Image.Image']:
        return self.base.generate_image(bar)

    def xor_pixels(self, channels='rgb', noise=False, noise_factor=255) -> Union[tuple['ndarray', tuple[int, int]], 'Image.Image']:
        return self.base.xor_pixels(channels, noise, noise_factor)


class AntiHarmony(object):
    __slots__ = ('image', 'right_pos', 'button_pos')

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


class Shuffle(object):
    __slots__ = ('seed',)

    def __init__(self, seed) -> None:
        self.seed = seed

    def obverse(self, iterable: 'Iterable'):
        random.seed(self.seed)
        random.shuffle(iterable)

    def reverse(self, iterable: 'Iterable'):
        random.seed(self.seed)
        randbelow = random._randbelow
        index_tuple = range(1, len(iterable))
        randbelow_list = [randbelow(i + 1) for i in reversed(index_tuple)]
        randbelow_list.reverse()
        for i, j in zip(index_tuple, randbelow_list):
            # pick an element in x[:i+1] with which to exchange x[i]
            iterable[i], iterable[j] = iterable[j], iterable[i]
