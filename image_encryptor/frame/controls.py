'''
Author       : noeru_desu
Date         : 2021-12-18 21:01:55
LastEditors  : noeru_desu
LastEditTime : 2022-02-05 17:59:42
Description  : 整理
'''
from abc import ABC
from typing import TYPE_CHECKING, Callable, Iterable, Optional
from hashlib import md5

from wx import Bitmap
from image_encryptor.constants import ANTY_HARMONY_MODE, DECRYPTION_MODE, ENCRYPTION_MODE, EXTENSION_KEYS, RESAMPLING_FILTERS

from image_encryptor.modules.password_verifier import PasswordDict
from image_encryptor.utils.misc_util import scale

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Gauge

    from image_encryptor.frame.events import MainFrame


class ItemNotFoundError(Exception):
    pass


class Controls(object):
    "控件/控制器"
    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.mapping_checkboxes = {'r': frame.mappingR, 'g': frame.mappingG, 'b': frame.mappingB, 'a': frame.mappingA}
        self.XOR_checkboxes = {'r': frame.XORR, 'g': frame.XORG, 'b': frame.XORB, 'a': frame.XORA}
        self.previous_saving_format = 'png'
        self.previous_proc_mode = ENCRYPTION_MODE

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
        self.frame.imageInfo.Label = v

    @property
    def imported_bitmap(self) -> Bitmap:
        return self.frame.importedBitmap.Bitmap

    @imported_bitmap.setter
    def imported_bitmap(self, v: 'Image'):
        self.frame.importedBitmap.Bitmap = Bitmap.FromBuffer(*v.size, v.convert('RGB').tobytes())
        self.frame.importedBitmapPlanel.Layout()

    @property
    def previewed_bitmap(self) -> Bitmap:
        return self.frame.previewedBitmap.Bitmap

    @previewed_bitmap.setter
    def previewed_bitmap(self, v: 'Image'):
        self.frame.previewedBitmap.Bitmap = Bitmap.FromBuffer(*v.size, v.convert('RGB').tobytes())
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
    def resampling_filter(self):
        return RESAMPLING_FILTERS[self.frame.resamplingFilter.Selection]

    @resampling_filter.setter
    def resampling_filter(self, v):
        self.frame.resamplingFilter.Selection = RESAMPLING_FILTERS.index(v)

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
    def saving_progress(self, v):
        self.frame.savingProgress.Value = v

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

    def clear_preview(self):
        self.frame.importedBitmap.Bitmap = self.frame.previewedBitmap.Bitmap = Bitmap()

    def regen_initial_preview(self, force=False):
        size = self.preview_size
        if not force and self.frame.image_item.initial_preview is not None and size == self.frame.image_item.preview_size:
            self.imported_bitmap = self.frame.image_item.initial_preview
            return False
        initial_preview = self.frame.image_item.loaded_image.resize(scale(self.frame.image_item.loaded_image, *size), self.resampling_filter)
        self.imported_bitmap = initial_preview
        self.frame.image_item.preview_size = size
        self.frame.image_item.initial_preview = initial_preview
        return True

    def regen_processed_preview(self, image: 'Image', try_not_to_zoom=False):
        size = self.preview_size
        md5 = self.frame.settings.encryption_settings_md5
        if try_not_to_zoom and self.frame.image_item.processed_preview is not None and size == self.frame.image_item.preview_size and self.frame.image_item.encryption_settings_md5 == md5:
            self.previewed_bitmap = image
        else:
            self.previewed_bitmap = image.resize(scale(image, *size), self.resampling_filter)
            self.frame.image_item.processed_preview = image
            self.frame.image_item.encryption_settings_md5 = self.frame.settings.encryption_settings_md5


class SettingsManager(object):
    def __init__(self, controls: 'Controls'):
        self.controls = controls
        '''{
            'proc_mode': 0,
            'cutting_row': 25,
            'cutting_col': 25,
            'shuffle': True,
            'flip': True,
            'mapping_channels': '',
            'xor_encryption': False,
            'xor_channels': 'rgb',
            'noise_xor': False,
            'noise_factor': 128,
            'password': None,
            'saving_path': '',
            'saving_format': 2,
            'quality': 98,
            'subsampling': 0
        }'''
        self.default = Settings(self.controls, (0, 25, 25, True, True, '', False, 'rgb', False, 128, None, '', 'png', 2, 98, 0))

    @property
    def encryption_settings(self):
        return (self.controls.proc_mode, self.controls.cutting_row, self.controls.cutting_col,
                self.controls.shuffle_chunks, self.controls.flip_chunks, self.controls.mapping_R,
                self.controls.mapping_G, self.controls.mapping_B, self.controls.mapping_A,
                self.controls.XOR_encryption, self.controls.noise_XOR, self.controls.XOR_R,
                self.controls.XOR_G, self.controls.XOR_B, self.controls.XOR_A,
                self.controls.noise_XOR, self.controls.noise_factor, self.controls.password,
                self.controls.resampling_filter)

    @property
    def encryption_settings_md5(self):
        return md5(str(self.encryption_settings).encode()).digest()

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
    SETTING_NAMES: tuple

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


class SettingsData(SettingsBase):
    SETTING_NAMES = ('proc_mode', 'cutting_row', 'cutting_col', 'shuffle_chunks', 'flip_chunks',
                     'mapping_channels', 'XOR_encryption', 'XOR_channels', 'noise_XOR', 'noise_factor',
                     'password', 'saving_path', 'saving_format', 'saving_format_index', 'saving_quality',
                     'saving_subsampling_level')

    def __init__(self, settings):
        if isinstance(settings, dict):
            self._inherit_dict_settings(settings)
        elif isinstance(settings, tuple):
            self.inherit_tuple(settings)

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

    def deepcopy(self):
        return SettingsData(tuple(self.properties))

    def encryption_parameters_data(self, orig_width, orig_height):
        has_password = self.password != 'none'
        password = 100 if has_password else self.password
        return EncryptionParametersData((self.cutting_col, self.cutting_row, orig_width, orig_height, self.shuffle_chunks,
                                        self.flip_chunks, False, self.mapping_channels, self.XOR_channels if self.XOR_encryption else '',
                                        self.noise_XOR, self.noise_factor, has_password,
                                        PasswordDict.get_validation_field_base64(password) if has_password else 0, self.password))


class Settings(SettingsData):
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

    def deepcopy(self):
        return Settings(self.controls, self.properties_tuple)


class SavingSettings(SettingsBase):
    SETTING_NAMES = ('path', 'format_index', 'format', 'quality', 'subsampling_level')

    def __init__(self, path: str, format_index: int, format: str, quality: int, subsampling_level: int):
        self.path = path
        self.format_index = format_index
        self.format = format
        self.quality = quality
        self.subsampling_level = subsampling_level


class EncryptionParametersData(SettingsBase):
    SETTING_NAMES = ('cutting_row', 'cutting_col', 'orig_width', 'orig_height', 'shuffle_chunks',
                     'flip_chunks', 'old_mapping', 'mapping_channels', 'XOR_channels', 'noise_XOR',
                     'noise_factor', 'has_password', 'password_base64', 'password')

    def __init__(self, parameters):
        if isinstance(parameters, dict):
            self._inherit_dict_settings(parameters)
        elif isinstance(parameters, tuple):
            self.inherit_tuple(parameters)

    def _inherit_dict_settings(self, parameters_dict):
        self.cutting_row = parameters_dict['cutting_row']
        self.cutting_col = parameters_dict['cutting_col']
        self.orig_width = parameters_dict['orig_width']
        self.orig_height = parameters_dict['orig_height']
        self.shuffle_chunks = parameters_dict['shuffle_chunks']
        self.flip_chunks = parameters_dict['flip_chunks']
        self.old_mapping = parameters_dict['old_mapping']
        self.mapping_channels = parameters_dict['mapping_channels']
        self.XOR_channels = parameters_dict['XOR_channels']
        self.noise_XOR = parameters_dict['noise_XOR']
        self.noise_factor = parameters_dict['noise_factor']
        self.has_password = parameters_dict['has_password']
        self.password_base64 = parameters_dict['password_base64']
        self.password = None

    @property
    def encryption_parameters_dict(self):
        parameters = {k: getattr(self, k) for k in self.SETTING_NAMES}
        del parameters['password']
        parameters['version'] = 5
        return parameters


class EncryptionParameters(EncryptionParametersData):
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
            if self.password is None:
                self.password = self.controls.frame.password_dict.get_password(self.password_base64)
                if self.password is None:
                    self.controls.password = ''
                    self.controls.frame.passwordCtrl.Enable()
                else:
                    self.controls.frame.passwordCtrl.Disable()
                    self.controls.password = self.password
            else:
                self.controls.frame.passwordCtrl.Disable()
                self.controls.password = self.password
        else:
            self.controls.frame.passwordCtrl.Disable()
            self.controls.password = 'none'


class ProgressBar(object):
    def __init__(self, target: 'Gauge', step_count: int = 1):
        self.target = target
        self.step_count = step_count
        self.step = -1
        self.value = 0
        self.finished_step = True
        self.max_value = 0
        self.step_progress = 0
        self.next_step_progress = 0
        self.target.SetValue(0)

    def next_step(self, max_value: int):
        if not self.finished_step:
            self.finish()
        self.finished_step = False
        self.step += 1
        self.max_value = max_value
        self.max = self.max_value * self.step_count
        self.value = 0
        self.step_progress = 0 if self.next_step_progress == 0 else self.next_step_progress
        self.next_step_progress = (self.step + 1) / self.step_count * 100 if self.step < self.step_count else 100

    def update(self, value):
        if value > self.max_value:
            return
        self.value = value
        self.target.SetValue(int(self.step_progress + value / self.max * 100))

    def add(self):
        self.update(self.value + 1)

    def finish(self):
        self.target.SetValue(int(self.next_step_progress))
        self.finished_step = True

    def over(self):
        if not self.finished_step:
            self.finish()
        self.target.SetValue(100)


class SegmentTrigger(object):
    def __init__(self, callbacks: Iterable[Callable], initcall: Optional[Callable] = None, *args, **kwargs):
        self._callbacks = callbacks
        self._initcall = initcall
        self._args = args
        self._kwargs = kwargs
        self._max_num = len(callbacks)
        self._num = -1

    @property
    def call(self) -> Callable:
        if self._num >= self._max_num:
            self.init()
        self._num += 1
        return self._callbacks[self._num]

    def init(self):
        self._num = -1
        if self._initcall is not None:
            self._initcall(*self._args, **self._kwargs)
