"""
Author       : noeru_desu
Date         : 2021-12-18 21:01:55
LastEditors  : noeru_desu
LastEditTime : 2022-05-02 16:01:43
Description  : 界面控制相关
"""
from abc import ABC
from os.path import splitext
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Union

from wx import Bitmap

from image_encryptor.constants import (ANTY_HARMONY_MODE, DECRYPTION_MODE,
                                       EA_VERSION, ENCRYPTION_MODE,
                                       EXTENSION_KEYS)
from image_encryptor.modules.password_verifier import PasswordDict

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Gauge
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.tree_manager import ImageItem
    from image_encryptor.modules.image import WrappedImage


class ItemNotFoundError(Exception):
    pass


class Controls(object):
    "控件/控制器"
    __slots__ = ('frame', 'mapping_checkboxes', 'XOR_checkboxes', 'previous_saving_format', 'previous_proc_mode', 'imported_image_id')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.mapping_checkboxes = {'r': frame.mappingR, 'g': frame.mappingG, 'b': frame.mappingB, 'a': frame.mappingA}
        self.XOR_checkboxes = {'r': frame.XORR, 'g': frame.XORG, 'b': frame.XORB, 'a': frame.XORA}
        self.previous_saving_format = 'png'
        self.previous_proc_mode = ENCRYPTION_MODE
        self.imported_image_id = 0

    # ----------
    # properties
    # ----------

    @property
    def loading_prograss_info(self) -> str:
        return self.frame.loadingPrograssInfo.Label

    @loading_prograss_info.setter
    def loading_prograss_info(self, v: str):
        self.frame.loadingPrograssInfo.Label = v

    @property
    def loading_prograss(self) -> int:
        return self.frame.loadingPrograss.Value

    @loading_prograss.setter
    def loading_prograss(self, v: int):
        self.frame.loadingPrograss.Value = v

    @property
    def image_info(self) -> str:
        return self.frame.imageInfo.Label

    @image_info.setter
    def image_info(self, v: str):
        try:
            self.frame.imageInfo.Label = v
        except RuntimeError:
            return

    @property
    def imported_bitmap(self) -> 'Bitmap':
        return self.frame.importedBitmap.Bitmap

    @imported_bitmap.setter
    def imported_bitmap(self, v: 'Bitmap'):
        self.frame.importedBitmap.Bitmap = v
        self.frame.importedBitmapPanel.Layout()

    @property
    def imported_image(self) -> 'Image':
        raise NotImplementedError

    @imported_image.setter
    def imported_image(self, v: 'Image'):
        addr = id(v)
        if addr == self.imported_image_id:  # 防止重复的Image->Bitmap转换
            return
        self.imported_image_id = addr
        self.frame.importedBitmap.Bitmap = Bitmap.FromBufferRGBA(*v.size, v.tobytes())
        self.frame.importedBitmapPanel.Layout()

    @property
    def previewed_bitmap(self) -> 'Bitmap':
        return self.frame.previewedBitmap.Bitmap

    @previewed_bitmap.setter
    def previewed_bitmap(self, v: 'Bitmap'):
        self.frame.previewedBitmap.Bitmap = v
        self.frame.previewedBitmapPanel.Layout()

    @property
    def previewed_image(self) -> 'Image':
        raise NotImplementedError

    @previewed_image.setter
    def previewed_image(self, v: 'WrappedImage'):
        self.frame.previewedBitmap.Bitmap = v.wxBitmap
        self.frame.previewedBitmapPanel.Layout()

    @property
    def proc_mode(self) -> int:
        return self.frame.procMode.Selection

    @proc_mode.setter
    def proc_mode(self, v: int):
        self.frame.procMode.Selection = v

    @property
    def password(self) -> str:
        return self.frame.passwordCtrl.Value

    @password.setter
    def password(self, v: str):
        self.frame.passwordCtrl.Value = v

    @property
    def cutting_row(self) -> int:
        return self.frame.cuttingRow.Value

    @cutting_row.setter
    def cutting_row(self, v: int):
        self.frame.cuttingRow.Value = v

    @property
    def cutting_col(self) -> int:
        return self.frame.cuttingCol.Value

    @cutting_col.setter
    def cutting_col(self, v: int):
        self.frame.cuttingCol.Value = v

    @property
    def shuffle_chunks(self) -> bool:
        return self.frame.shuffleChunks.Value

    @shuffle_chunks.setter
    def shuffle_chunks(self, v: bool):
        self.frame.shuffleChunks.Value = v

    @property
    def flip_chunks(self) -> bool:
        return self.frame.flipChunks.Value

    @flip_chunks.setter
    def flip_chunks(self, v: bool):
        self.frame.flipChunks.Value = v

    @property
    def mapping_R(self) -> bool:
        return self.frame.mappingR.Value

    @mapping_R.setter
    def mapping_R(self, v: bool):
        self.frame.mappingR.Value = v

    @property
    def mapping_G(self) -> bool:
        return self.frame.mappingG.Value

    @mapping_G.setter
    def mapping_G(self, v: bool):
        self.frame.mappingG.Value = v

    @property
    def mapping_B(self) -> bool:
        return self.frame.mappingB.Value

    @mapping_B.setter
    def mapping_B(self, v: bool):
        self.frame.mappingB.Value = v

    @property
    def mapping_A(self) -> bool:
        return self.frame.mappingA.Value

    @mapping_A.setter
    def mapping_A(self, v: bool):
        self.frame.mappingA.Value = v

    @property
    def XOR_encryption(self) -> bool:
        return self.frame.XOREncryption.Value

    @XOR_encryption.setter
    def XOR_encryption(self, v: bool):
        self.frame.XOREncryption.Value = v

    @property
    def XOR_R(self) -> bool:
        return self.frame.XORR.Value

    @XOR_R.setter
    def XOR_R(self, v: bool):
        self.frame.XORR.Value = v

    @property
    def XOR_G(self) -> bool:
        return self.frame.XORG.Value

    @XOR_G.setter
    def XOR_G(self, v: bool):
        self.frame.XORG.Value = v

    @property
    def XOR_B(self) -> bool:
        return self.frame.XORB.Value

    @XOR_B.setter
    def XOR_B(self, v: bool):
        self.frame.XORB.Value = v

    @property
    def XOR_A(self) -> bool:
        return self.frame.XORA.Value

    @XOR_A.setter
    def XOR_A(self, v: bool):
        self.frame.XORA.Value = v

    @property
    def noise_XOR(self) -> bool:
        return self.frame.noiseXor.Value

    @noise_XOR.setter
    def noise_XOR(self, v: bool):
        self.frame.noiseXor.Value = v

    @property
    def noise_factor(self) -> int:
        return self.frame.noiseFactor.Value

    @noise_factor.setter
    def noise_factor(self, v: int):
        self.frame.noiseFactor.Value = v

    @property
    def noise_factor_info(self) -> str:
        return self.frame.noiseFactorNum.Label

    @noise_factor_info.setter
    def noise_factor_info(self, v):
        self.frame.noiseFactorNum.Label = v

    @property
    def preview_mode(self) -> int:
        return self.frame.previewMode.Selection

    @preview_mode.setter
    def preview_mode(self, v: int):
        self.frame.previewMode.Selection = v

    @property
    def preview_source(self) -> int:
        return self.frame.previewSource.Selection

    @preview_source.setter
    def preview_source(self, v: int):
        self.frame.previewSource.Selection = v

    @property
    def saving_progress(self) -> int:
        return self.frame.savingProgress.Value

    @saving_progress.setter
    def saving_progress(self, v):
        self.frame.savingProgress.Value = v

    @property
    def preview_progress_info(self) -> str:
        return self.frame.previewProgressInfo.Label

    @preview_progress_info.setter
    def preview_progress_info(self, v):
        self.frame.previewProgressInfo.Label = v

    @property
    def preview_progress(self) -> int:
        return self.frame.previewProgress.Value

    @preview_progress.setter
    def preview_progress(self, v):
        self.frame.previewProgress.Value = v

    @property
    def resampling_filter_id(self) -> int:
        return self.frame.resamplingFilter.Selection

    @resampling_filter_id.setter
    def resampling_filter_id(self, v: int):
        self.frame.resamplingFilter.Selection = v

    @property
    def resampling_filter_name(self) -> str:
        return self.frame.resamplingFilter.StringSelection

    @resampling_filter_name.setter
    def resampling_filter_name(self, v: str):
        self.frame.resamplingFilter.StringSelection = v

    @property
    def max_image_pixels(self) -> int:
        return self.frame.maxImagePixels.Value

    @max_image_pixels.setter
    def max_image_pixels(self, v):
        self.frame.maxImagePixels.Value = v

    @property
    def stop_loading_btn_text(self) -> str:
        return self.frame.stopLoadingBtn.Label

    @stop_loading_btn_text.setter
    def stop_loading_btn_text(self, v):
        self.frame.stopLoadingBtn.Label = v

    @property
    def reloading_btn_text(self) -> str:
        return self.frame.reloadingBtn.Label

    @reloading_btn_text.setter
    def reloading_btn_text(self, v):
        self.frame.reloadingBtn.Label = v

    @property
    def saving_quality_info(self) -> str:
        return self.frame.qualityInfo.Label

    @saving_quality_info.setter
    def saving_quality_info(self, v):
        self.frame.qualityInfo.Label = v

    @property
    def saving_quality(self) -> int:
        return self.frame.savingQuality.Value

    @saving_quality.setter
    def saving_quality(self, v: int):
        self.frame.savingQuality.Value = v

    @property
    def saving_subsampling_info(self) -> str:
        return self.frame.subsamplingInfo.Label

    @saving_subsampling_info.setter
    def saving_subsampling_info(self, v):
        self.frame.subsamplingInfo.Label = v

    @property
    def saving_subsampling_level(self) -> int:
        return self.frame.subsamplingLevel.Value

    @saving_subsampling_level.setter
    def saving_subsampling_level(self, v: int):
        self.frame.subsamplingLevel.Value = v

    @property
    def saving_path(self) -> str:
        return self.frame.selectSavingPath.Path

    @saving_path.setter
    def saving_path(self, v: str):
        self.frame.selectSavingPath.Path = v

    @property
    def saving_format(self) -> str:
        return self.frame.savingFormat.Value

    @saving_format.setter
    def saving_format(self, v: str):
        self.frame.savingFormat.Value = v

    @property
    def saving_format_index(self) -> int:
        return EXTENSION_KEYS.index(self.frame.savingFormat.Value)

    @saving_format_index.setter
    def saving_format_index(self, v: int):
        self.frame.savingFormat.Selection = v

    @property
    def preview_size(self) -> tuple[int, int]:
        return self.frame.importedBitmapPanel.Size

    @property
    def saving_progress_info(self) -> str:
        return self.frame.savingProgressInfo.Label

    @saving_progress_info.setter
    def saving_progress_info(self, v: str):
        self.frame.savingProgressInfo.Label = v

    @property
    def saving_progress(self) -> int:
        return self.frame.savingProgress.Value

    @saving_progress.setter
    def saving_progress(self, v: int):
        self.frame.savingProgress.Value = v

    @property
    def redundant_cache_length(self) -> int:
        """启动参数: 冗余缓存最大长度

        处理结果缓存中会同时缓存多个不同加密设置生成的图像数据
        (处理结果缓存类似于LRU缓存)
        除最新缓存外的其他缓存都将在取消选择图像项目时删除

        Returns:
            int: 冗余缓存最大长度
        """
        return self.frame.redundantCacheLength.Value

    @redundant_cache_length.setter
    def redundant_cache_length(self, v: int):
        self.frame.redundantCacheLength.Value = v

    @property
    def low_memory_mode(self) -> bool:
        """启动参数: 低内存占用模式

        开启后，将在取消选中图像项目时删除相关的图像数据(包括原始数据与缓存，图像和文件信息除外)

        Returns:
            bool: 是否开启
        """
        return self.frame.lowMemoryMode.Value

    @low_memory_mode.setter
    def low_memory_mode(self, v: bool):
        self.frame.lowMemoryMode.Value = v

    @property
    def disable_cache(self) -> bool:
        """启动参数: 禁用处理结果缓存

        Returns:
            bool: 是否禁用
        """
        return self.frame.disableCache.Value

    @disable_cache.setter
    def disable_cache(self, v: bool):
        self.frame.disableCache.Value = v

    @property
    def mapping_channels(self) -> str:
        """选择的需要随机映射的各通道字符串

        Returns:
            str: 选择的需要随机映射的各通道(如`rgb`/`b`/`rgba`/`ga`)
        """
        channels = []
        if self.mapping_R:
            channels.append('r')
        if self.mapping_G:
            channels.append('g')
        if self.mapping_B:
            channels.append('b')
        if self.mapping_A:
            channels.append('a')
        return ''.join(channels)

    @mapping_channels.setter
    def mapping_channels(self, v: Iterable[str]):
        for i in 'rgba':
            self.mapping_checkboxes[i].SetValue(i in v)

    @property
    def XOR_channels(self):
        """选择的需要异或加密的各通道字符串

        Returns:
            str: 选择的需要异或加密的各通道(如`rgb`/`b`/`rgba`/`ga`)
        """
        channels = []
        if self.XOR_R:
            channels.append('r')
        if self.XOR_G:
            channels.append('g')
        if self.XOR_B:
            channels.append('b')
        if self.XOR_A:
            channels.append('a')
        return ''.join(channels)

    @XOR_channels.setter
    def XOR_channels(self, v: Iterable[str]):
        for i in 'rgba':
            self.XOR_checkboxes[i].SetValue(i in v)

    def gen_image_info(self, item: 'ImageItem' = None):
        """输出图像信息至界面

        Args:
            item (ImageItem, optional): ImageItem实例. 默认为None, 输出为`未选择图像`
        """
        if item is None:
            self.image_info = '未选择图像'
        else:
            self.image_info = '大小: {}x{} 格式: {}'.format(*item.cache.loaded_image.size,
                                                        '未知' if item.no_file else splitext(item.loaded_image_path)[1].lstrip('.')
                                                        )

    def clear_preview(self):
        """取消显示所有缓存"""
        self.frame.importedBitmap.Bitmap = self.frame.previewedBitmap.Bitmap = Bitmap()

    def display_and_cache_processed_preview(self, image: 'WrappedImage'):
        """显示并缓存处理结果

        如果`image`参数传入的实例支持缩放操作，则添加到可缩放缓存，反之则添加到普通缓存

        Args:
            image (WrappedImage): 需要显示并缓存的WrappedImage的子类实例
        """
        if image.scalable:
            self.frame.image_item.cache.previews.add_scalable_cache(self.frame.settings.encryption_settings_hash, image)
            self.previewed_bitmap = image.gen_wxBitmap(self.preview_size, self.resampling_filter_id)
        else:
            bitmap = image.wxBitmap
            self.frame.image_item.cache.previews.add_normal_cache(self.frame.settings.encryption_settings_hash_with_size, bitmap)
            self.previewed_bitmap = bitmap


class SettingsManager(object):
    __slots__ = ('controls', 'default')

    def __init__(self, controls: 'Controls'):
        self.controls = controls
        self.default = Settings(self.controls, (0, 25, 25, True, True, '', False, 'rgb', False, 128, None, '', 'png', 2, 98, 0))

    @property
    def encryption_settings(self):
        """当前所有加密设置的元组, 一般为生成encryption_settings_hash时使用"""
        return (
            self.controls.proc_mode, self.controls.cutting_row, self.controls.cutting_col,
            self.controls.shuffle_chunks, self.controls.flip_chunks, self.controls.mapping_channels,
            self.controls.XOR_encryption, self.controls.XOR_channels, self.controls.noise_XOR,
            self.controls.noise_factor, self.controls.password
        )

    @property
    def encryption_settings_hash(self):
        """当前加密设置的hash(已加盐)"""
        # hash(self.encryption_settings) 耗时约为 hashlib.md5(repr(self.encryption_settings).encode()).digest() 的 55%
        return hash(self.encryption_settings)

    @property
    def encryption_settings_hash_with_size(self):
        """在encryption_settings_hash的基础上添加resampling_filter_id/preview_source/preview_size"""
        return hash((self.encryption_settings, self.controls.resampling_filter_id, self.controls.preview_source, *self.controls.preview_size))

    @property
    def all_dict(self):
        """所有加密设置的字典(此方法尚未被使用)"""
        return {
            'proc_mode': self.controls.proc_mode,
            'cutting_row': self.controls.cutting_row,
            'cutting_col': self.controls.cutting_col,
            'shuffle_chunks': self.controls.shuffle_chunks,
            'flip_chunks': self.controls.flip_chunks,
            'mapping_channels': self.controls.mapping_channels,
            'XOR_encryption': self.controls.XOR_encryption,
            'XOR_channels': self.controls.XOR_channels,
            'noise_XOR': self.controls.noise_XOR,
            'noise_factor': self.controls.noise_factor,
            'password': self.controls.password,
            'saving_path': self.controls.saving_path,
            'saving_format': self.controls.saving_format,
            'saving_format_index': self.controls.saving_format_index,
            'saving_quality': self.controls.saving_quality,
            'saving_subsampling_level': self.controls.saving_subsampling_level
        }

    @property
    def all(self) -> 'Settings':
        """以当前的所有加密设置实例化Settings类"""
        return Settings(self.controls)

    @property
    def saving_settings(self) -> 'SavingSettings':
        """以当前的所有保存设置实例化SavingSettings类"""
        return SavingSettings(self.controls.saving_path, self.controls.saving_format_index, EXTENSION_KEYS[self.controls.saving_format_index],
                              self.controls.saving_quality, self.controls.saving_subsampling_level)


class SettingsBase(ABC):
    __slots__ = ()
    SETTING_NAMES: Iterable[str]

    def __repr__(self) -> str:
        return ', '.join(f'{i}: {getattr(self, i)}' for i in self.SETTING_NAMES)

    def __getitem__(self, i: Any):
        if isinstance(i, str):
            return getattr(self, i)

    def inherit_tuple(self, settings: Iterable[Any]):
        """将可迭代对象(一般是由`self.properties_tuple`生成的元组)中的数据同步到自身

        Args:
            settings (Iterable[Any]): 可迭代对象(一般是由`(self.properties_tuple)`生成的元组)
        """
        assert len(self.SETTING_NAMES) == len(settings), f'Wrong settings arguments length, currently {len(settings)} (expected {len(self.SETTING_NAMES)})'
        for n, v in zip(self.SETTING_NAMES, settings):
            setattr(self, n, v)

    @property
    def properties(self):
        """返回`self.SETTING_NAMES`中每个属性名的值的生成器

        Returns:
            Generator: `self.SETTING_NAMES`中每个属性名的值
        """
        return (getattr(self, i) for i in self.SETTING_NAMES)

    @property
    def properties_tuple(self):
        """将`self.properties`转换为元组

        Returns:
            tuple: `self.SETTING_NAMES`中每个属性名的值的元组
        """
        return tuple(self.properties)

    @property
    def properties_hash(self):
        """`self.properties_tuple`的hash值

        Returns:
            int: hash结果(已加盐)
        """
        return hash(self.properties)

    def copy(self):
        """返回当前实例的浅拷贝

        Returns:
            Type[Self]: 当前实例的浅拷贝
        """
        raise NotImplementedError()


class SettingsData(SettingsBase):
    __slots__ = SETTING_NAMES = (
        'proc_mode', 'cutting_row', 'cutting_col', 'shuffle_chunks', 'flip_chunks',
        'mapping_channels', 'XOR_encryption', 'XOR_channels', 'noise_XOR', 'noise_factor',
        'password', 'saving_path', 'saving_format', 'saving_format_index', 'saving_quality',
        'saving_subsampling_level'
    )

    def __init__(self, settings: Iterable[Any]):
        """
        Args:
            settings (Iterable[Any]): 可迭代对象(一般是由`(self.properties_tuple)`生成的元组)
        """
        self.inherit_tuple(settings)
        # if isinstance(settings, tuple):
        #     self.inherit_tuple(settings)
        # elif isinstance(settings, dict):
        #     self._inherit_dict_settings(settings)

    def _inherit_dict_settings(self, settings_dict: dict[str, Any]):
        """尚未使用

        Args:
            settings_dict (dict[str, Any]): 所有加密设置的字典
        """
        self.proc_mode = settings_dict['proc_mode']
        self.cutting_row = settings_dict['cutting_row']
        self.cutting_col = settings_dict['cutting_col']
        self.shuffle_chunks = settings_dict['shuffle_chunks']
        self.flip_chunks = settings_dict['flip_chunks']
        self.mapping_channels = settings_dict['mapping_channels']
        self.XOR_channels = settings_dict['XOR_channels']
        self.XOR_encryption = settings_dict.get('XOR_encryption', bool(self.XOR_channels))
        self.noise_XOR = settings_dict['noise_XOR']
        self.noise_factor = settings_dict['noise_factor']
        self.password = settings_dict['password']
        self.saving_path = settings_dict['saving_path']
        self.saving_format = settings_dict['saving_format']
        self.saving_format_index = settings_dict['saving_format_index']
        self.saving_quality = settings_dict['saving_quality']
        self.saving_subsampling_level = settings_dict['saving_subsampling_level']

    def encryption_parameters_data(self, orig_width: int, orig_height: int):
        """根据当前实例的数据与给出的参数实例化EncryptionParametersData类

        Args:
            orig_width (int): 原始图像宽度
            orig_height (int): 原始图像高度

        Returns:
            EncryptionParametersData
        """
        has_password = self.password != 'none'
        password = self.password if has_password else 100
        return EncryptionParametersData((self.cutting_col, self.cutting_row, orig_width, orig_height, self.shuffle_chunks,
                                        self.flip_chunks, self.mapping_channels, self.XOR_channels if self.XOR_encryption else '',
                                        self.noise_XOR, self.noise_factor, has_password,
                                        PasswordDict.get_validation_field_base64(password) if has_password else 0, EA_VERSION,
                                        True, self.password))

    @property
    def available_password(self):
        return 100 if self.password == 'none' else self.password

    @property
    def encryption_settings(self) -> tuple[Any]:
        """当前实例中加密设置的元组, 一般为生成encryption_settings_hash时使用"""
        return (
            self.proc_mode, self.cutting_row, self.cutting_col,
            self.shuffle_chunks, self.flip_chunks, self.mapping_channels,
            self.XOR_encryption, self.XOR_channels, self.noise_XOR,
            self.noise_factor, self.password
        )

    @property
    def encryption_settings_hash(self) -> int:
        """当前加密设置的hash(已加盐)"""
        return hash(self.encryption_settings)

    def copy(self):
        return SettingsData(self.properties_tuple)

class Settings(SettingsData):
    __slots__ = ('controls',)

    def __init__(self, controls: 'Controls', settings: Iterable[Any] = None):
        """
        Args:
            controls (Controls): Controls实例.\n
            settings (Iterable[Any], optional): settings (Iterable[Any]): 可迭代对象(一般是由`(self.properties_tuple)`生成的元组)
            默认为None, 为None时将从界面中获取加密设置
        """
        self.controls = controls
        if settings is None:
            self._init()
        else:
            super().__init__(settings)

    def _init(self):
        self.proc_mode = self.controls.proc_mode
        self.cutting_row = self.controls.cutting_row
        self.cutting_col = self.controls.cutting_col
        self.shuffle_chunks = self.controls.shuffle_chunks
        self.flip_chunks = self.controls.flip_chunks
        self.mapping_channels = self.controls.mapping_channels
        self.XOR_encryption = self.controls.XOR_encryption
        self.XOR_channels = self.controls.XOR_channels
        self.noise_XOR = self.controls.noise_XOR
        self.noise_factor = self.controls.noise_factor
        self.password = self.controls.password
        self.saving_path = self.controls.saving_path
        self.saving_format = self.controls.saving_format
        self.saving_format_index = self.controls.saving_format_index
        self.saving_quality = self.controls.saving_quality
        self.saving_subsampling_level = self.controls.saving_subsampling_level

    def backtrack_interface(self):
        """将加密设置显示到界面"""
        self.controls.proc_mode = self.proc_mode if self.proc_mode != DECRYPTION_MODE else ENCRYPTION_MODE
        if self.controls.proc_mode == ANTY_HARMONY_MODE:
            self.controls.frame.processingSettingsPanel.Disable()
            self.controls.frame.passwordCtrl.Disable()
        else:
            self.controls.frame.processingSettingsPanel.Enable()
            self.controls.frame.passwordCtrl.Enable()
        self.controls.cutting_row = self.cutting_row
        self.controls.cutting_col = self.cutting_col
        self.controls.shuffle_chunks = self.shuffle_chunks
        self.controls.mapping_channels = self.mapping_channels
        self.controls.flip_chunks = self.flip_chunks
        self.controls.password = self.password
        self.controls.XOR_encryption = self.XOR_encryption
        self.controls.XOR_channels = self.XOR_channels
        self.controls.noise_XOR = self.noise_XOR
        self.controls.noise_factor = self.noise_factor
        self.controls.noise_factor_info = str(self.noise_factor)
        self.controls.frame.xorPanel.Enable(self.XOR_encryption)
        self.controls.frame.processingSettingsPanel.Enable()
        self.controls.frame.passwordCtrl.Enable()

    def copy(self):
        return Settings(self.controls, self.properties_tuple)


class SavingSettings(SettingsBase):
    __slots__ = SETTING_NAMES = ('path', 'format_index', 'format', 'quality', 'subsampling_level')

    def __init__(self, path: str, format_index: int, format: str, quality: int, subsampling_level: int):
        self.path = path
        self.format_index = format_index
        self.format = format
        self.quality = quality
        self.subsampling_level = subsampling_level


class EncryptionParametersData(SettingsBase):
    __slots__ = SETTING_NAMES = (
        'cutting_row', 'cutting_col', 'orig_width', 'orig_height', 'shuffle_chunks',
        'flip_chunks', 'mapping_channels', 'XOR_channels', 'noise_XOR', 'noise_factor',
        'has_password', 'password_base64', 'version', 'dynamic_auth', 'password'
        # 需保证dynamic_auth与password在最后，参考self.encryption_parameters_dict
    )

    def __init__(self, parameters: Union[dict[str, Any], Iterable[Any]]):
        """
        Args:
            parameters: 加密参数字典(一般由`self.encryption_parameters_dict`生成)或加密参数元组(一般由`self.properties_tuple`生成)
        """
        if isinstance(parameters, dict):
            self._inherit_dict_settings(parameters)
        elif isinstance(parameters, Iterable):
            self.inherit_tuple(parameters)

    def _inherit_dict_settings(self, parameters_dict: dict[str, Any]):
        self.cutting_row: int = parameters_dict['cutting_row']
        self.cutting_col: int = parameters_dict['cutting_col']
        self.orig_width: int = parameters_dict['orig_width']
        self.orig_height: int = parameters_dict['orig_height']
        self.shuffle_chunks: bool = parameters_dict['shuffle_chunks']
        self.flip_chunks: bool = parameters_dict['flip_chunks']
        self.mapping_channels: str = parameters_dict['mapping_channels']
        self.XOR_channels: str = parameters_dict['XOR_channels']
        self.noise_XOR: bool = parameters_dict['noise_XOR']
        self.noise_factor: int = parameters_dict['noise_factor']
        self.has_password: bool = parameters_dict['has_password']
        self.password_base64: str = parameters_dict['password_base64']
        self.version: int = parameters_dict['version']
        self.dynamic_auth: bool = self.version >= 6
        self.password: str = None

    @property
    def encryption_parameters_dict(self) -> dict[str, Any]:
        """生成用于添加到被加密文件末尾的加密参数字典"""
        return {k: getattr(self, k) for k in self.SETTING_NAMES[:-2]}


class EncryptionParameters(EncryptionParametersData):
    __slots__ = ('controls',)

    def __init__(self, controls: 'Controls', parameters: dict[str, Any] | Iterable[Any]):
        self.controls = controls
        super().__init__(parameters)

    def get_password(self):
        if not self.has_password:
            return 100
        if self.password is not None:
            return self.password
        self.password = self.controls.frame.password_dict.get_password(self.password_base64)
        return None if self.password is None else self.password

    def backtrack_interface(self):
        """将加密参数显示到界面"""
        self.controls.proc_mode = DECRYPTION_MODE
        self.controls.frame.processingSettingsPanel.Disable()
        self.controls.cutting_row = self.cutting_row
        self.controls.cutting_col = self.cutting_col
        self.controls.shuffle_chunks = self.shuffle_chunks
        self.controls.mapping_channels = self.mapping_channels
        self.controls.flip_chunks = self.flip_chunks
        self.controls.noise_XOR = self.noise_XOR
        self.controls.noise_factor = self.noise_factor
        self.controls.noise_factor_info = str(self.noise_factor)
        if self.XOR_channels:
            self.controls.XOR_encryption = True
        self.controls.XOR_channels = self.XOR_channels
        if self.has_password:
            while self.password is None:
                self.password = self.controls.frame.password_dict.get_password(self.password_base64)
                if self.password is not None:
                    break
                self.password = self.controls.frame.dialog.password_dialog(self.controls.frame.image_item.path_data.file_name, self.password_base64, True)
                if self.password is not None:
                    break
                self.controls.password = ''
                self.controls.frame.passwordCtrl.Enable()
                return
            self.controls.frame.passwordCtrl.Disable()
            self.controls.password = self.password
        else:
            self.controls.frame.passwordCtrl.Disable()
            self.controls.password = 'none'


class ProgressBar(object):
    __slots__ = (
        'gauge', 'gauge_range', 'total_steps', 'step_size', 'finished_step',
        'step', 'basic_progress', 'value', 'max_value', '_coefficient'
    )

    def __init__(self, gauge: 'Gauge', total_steps: int = 1):
        assert total_steps > 0, f'total_steps must be greater than 0 (currently {total_steps})'
        gauge.Value = 0
        self.gauge = gauge
        self.gauge_range: int = gauge.Range
        self.total_steps = total_steps
        self.step_size = self.gauge_range // total_steps
        self.finished_step = True
        self.step = 0
        self.basic_progress = 0
        self.value = 0
        self.max_value = 0
        self._coefficient = 0

    def next_step(self, max_value: int):
        if not self.finished_step:
            self.finish()
        self.finished_step = False
        self.step += 1
        self.max_value = max_value
        self.value = 0
        self._coefficient = self.step_size / max_value

    def update(self, value: int):
        assert not self.finished_step, 'Step information is not initialized, please call next_step first.'
        if value > self.max_value:
            return
        self.value = value
        self.gauge.Value = int(value * self._coefficient) + self.basic_progress

    def add(self):
        self.update(self.value + 1)

    def finish(self):
        self.gauge.Value = self.basic_progress = self.step_size * self.step
        self.finished_step = True

    def over(self):
        self.gauge.Value = self.gauge_range


class SegmentTrigger(object):
    __slots__ = ('_callbacks', '_initcall', '_args', '_kwargs', '_max_num', '_num')

    def __init__(self, callbacks: Iterable[Callable], initcall: Optional[Callable] = None, *init_args, **init_kwargs):
        self._callbacks = callbacks
        self._initcall = initcall
        self._args = init_args
        self._kwargs = init_kwargs
        self._max_num = len(callbacks)
        self._num = -1

    @property
    def call(self) -> Callable:
        self._num += 1
        if self._num >= self._max_num:
            self.init()
        return self._callbacks[self._num]

    def init(self):
        self._num = -1
        if self._initcall is not None:
            self._initcall(*self._args, **self._kwargs)
