"""
Author       : noeru_desu
Date         : 2021-12-18 21:01:55
LastEditors  : noeru_desu
LastEditTime : 2022-03-27 08:33:40
Description  : 整理
"""
from abc import ABC
from os.path import splitext
from typing import TYPE_CHECKING, Callable, Iterable, Optional

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
    def loading_prograss_info(self, v):
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
    def image_info(self, v):
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
        self.frame.importedBitmapPlanel.Layout()

    @property
    def imported_image(self) -> 'Image':
        raise NotImplementedError

    @imported_image.setter
    def imported_image(self, v: 'Image'):
        addr = id(v)
        if addr == self.imported_image_id:
            return
        self.imported_image_id = addr
        self.frame.importedBitmap.Bitmap = Bitmap.FromBufferRGBA(*v.size, v.tobytes())
        self.frame.importedBitmapPlanel.Layout()

    @property
    def previewed_bitmap(self) -> 'Bitmap':
        return self.frame.previewedBitmap.Bitmap

    @previewed_bitmap.setter
    def previewed_bitmap(self, v: 'Bitmap'):
        self.frame.previewedBitmap.Bitmap = v
        self.frame.previewedBitmapPlanel.Layout()

    @property
    def previewed_image(self):
        raise NotImplementedError

    @previewed_image.setter
    def previewed_image(self, v: 'WrappedImage'):
        self.frame.previewedBitmap.Bitmap = v.wxBitmap
        self.frame.previewedBitmapPlanel.Layout()

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
    def resampling_filter_id(self):
        return self.frame.resamplingFilter.Selection

    @resampling_filter_id.setter
    def resampling_filter_id(self, v):
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
        return self.frame.importedBitmapPlanel.Size

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
        return self.frame.redundantCacheLength.Value

    @redundant_cache_length.setter
    def redundant_cache_length(self, v: int):
        self.frame.redundantCacheLength.Value = v

    @property
    def low_memory_mode(self) -> bool:
        return self.frame.lowMemoryMode.Value

    @low_memory_mode.setter
    def low_memory_mode(self, v: bool):
        self.frame.lowMemoryMode.Value = v

    @property
    def mapping_channels(self):
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
    def mapping_channels(self, v):
        for i in 'rgba':
            self.mapping_checkboxes[i].SetValue(i in v)

    @property
    def XOR_channels(self):
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
    def XOR_channels(self, v):
        for i in 'rgba':
            self.XOR_checkboxes[i].SetValue(i in v)

    def gen_image_info(self, item: 'ImageItem' = None):
        if item is None:
            self.image_info = '未选择图像'
        else:
            self.image_info = '大小: {}x{} 格式: {}'.format(*item.cache.loaded_image.size,
                                                        '未知' if item.no_file else splitext(item.loaded_image_path)[1].lstrip('.')
                                                        )

    def clear_preview(self):
        self.frame.importedBitmap.Bitmap = self.frame.previewedBitmap.Bitmap = Bitmap()

    def display_and_cache_processed_preview(self, image: 'WrappedImage'):
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
        return (
            self.controls.proc_mode, self.controls.cutting_row, self.controls.cutting_col,
            self.controls.shuffle_chunks, self.controls.flip_chunks, self.controls.mapping_R,
            self.controls.mapping_G, self.controls.mapping_B, self.controls.mapping_A,
            self.controls.XOR_encryption, self.controls.noise_XOR, self.controls.XOR_R,
            self.controls.XOR_G, self.controls.XOR_B, self.controls.XOR_A,
            self.controls.noise_XOR, self.controls.noise_factor, self.controls.password,    # 后面是预览设置
            self.controls.resampling_filter_id, self.controls.preview_source
        )

    @property
    def encryption_settings_hash(self):
        # hash(self.encryption_settings) 耗时约为 hashlib.md5(repr(self.encryption_settings).encode()).digest() 的 55%
        return hash(self.encryption_settings)

    @property
    def encryption_settings_hash_with_size(self):
        return hash((self.encryption_settings, *self.controls.preview_size))

    @property
    def all_dict(self):
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
    def all(self):
        return Settings(self.controls)

    @property
    def saving_settings(self):
        return SavingSettings(self.controls.saving_path, self.controls.saving_format_index, EXTENSION_KEYS[self.controls.saving_format_index],
                              self.controls.saving_quality, self.controls.saving_subsampling_level)


class SettingsBase(ABC):
    __slots__ = ()
    SETTING_NAMES: Iterable

    def __repr__(self) -> str:
        return ', '.join(f'{i}: {getattr(self, i)}' for i in self.SETTING_NAMES)

    def __getitem__(self, i):
        if isinstance(i, str):
            return getattr(self, i)

    def inherit_tuple(self, settings: tuple):
        for n, v in zip(self.SETTING_NAMES, settings):
            setattr(self, n, v)

    @property
    def properties(self):
        return (getattr(self, i) for i in self.SETTING_NAMES)

    @property
    def properties_tuple(self):
        return tuple(self.properties)

    @property
    def properties_hash(self):
        return hash(self.properties)


class SettingsData(SettingsBase):
    __slots__ = SETTING_NAMES = (
        'proc_mode', 'cutting_row', 'cutting_col', 'shuffle_chunks', 'flip_chunks',
        'mapping_channels', 'XOR_encryption', 'XOR_channels', 'noise_XOR', 'noise_factor',
        'password', 'saving_path', 'saving_format', 'saving_format_index', 'saving_quality',
        'saving_subsampling_level'
    )

    def __init__(self, settings: tuple):
        self.inherit_tuple(settings)
        # if isinstance(settings, tuple):
        #     self.inherit_tuple(settings)
        # elif isinstance(settings, dict):
        #     self._inherit_dict_settings(settings)

    def _inherit_dict_settings(self, settings_dict):
        self.proc_mode = settings_dict['proc_mode']
        self.cutting_row = settings_dict['cutting_row']
        self.cutting_col = settings_dict['cutting_col']
        self.shuffle_chunks = settings_dict['shuffle_chunks']
        self.flip_chunks = settings_dict['flip_chunks']
        self.mapping_channels = settings_dict['mapping_channels']
        self.XOR_channels = settings_dict['XOR_channels']
        self.XOR_encryption = settings_dict['XOR_encryption'] if 'XOR_encryption' in settings_dict else bool(self.XOR_channels)
        self.noise_XOR = settings_dict['noise_XOR']
        self.noise_factor = settings_dict['noise_factor']
        self.password = settings_dict['password']
        self.saving_path = settings_dict['saving_path']
        self.saving_format = settings_dict['saving_format']
        self.saving_format_index = settings_dict['saving_format_index']
        self.saving_quality = settings_dict['saving_quality']
        self.saving_subsampling_level = settings_dict['saving_subsampling_level']

    def copy(self):
        return SettingsData(tuple(self.properties))

    def encryption_parameters_data(self, orig_width, orig_height):
        has_password = self.password != 'none'
        password = self.password if has_password else 100
        return EncryptionParametersData((self.cutting_col, self.cutting_row, orig_width, orig_height, self.shuffle_chunks,
                                        self.flip_chunks, self.mapping_channels, self.XOR_channels if self.XOR_encryption else '',
                                        self.noise_XOR, self.noise_factor, has_password,
                                        PasswordDict.get_validation_field_base64(password) if has_password else 0, EA_VERSION,
                                        True, self.password))


class Settings(SettingsData):
    __slots__ = ('controls',)

    def __init__(self, controls: 'Controls', settings=None):
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
        self.controls.proc_mode = self.proc_mode if self.proc_mode != DECRYPTION_MODE else ENCRYPTION_MODE
        if self.controls.proc_mode == ANTY_HARMONY_MODE:
            self.controls.frame.processingSettingsPanel1.Disable()
            self.controls.frame.passwordCtrl.Disable()
        else:
            self.controls.frame.processingSettingsPanel1.Enable()
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
        self.controls.frame.processingSettingsPanel1.Enable()
        self.controls.frame.passwordCtrl.Enable()

    def copy(self):
        """将设置实例浅拷贝"""
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

    def __init__(self, parameters):
        if isinstance(parameters, dict):
            self._inherit_dict_settings(parameters)
        elif isinstance(parameters, tuple):
            self.inherit_tuple(parameters)

    def _inherit_dict_settings(self, parameters_dict):
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
    def encryption_parameters_dict(self):
        return {k: getattr(self, k) for k in self.SETTING_NAMES[:-2]}


class EncryptionParameters(EncryptionParametersData):
    __slots__ = ('controls',)

    def __init__(self, controls: 'Controls', parameters):
        self.controls = controls
        super().__init__(parameters)

    def backtrack_interface(self):
        self.controls.proc_mode = DECRYPTION_MODE
        self.controls.frame.processingSettingsPanel1.Disable()
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
            while True:
                if self.password is not None:
                    break
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
        self.gauge_range = gauge.Range
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

    def update(self, value):
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
