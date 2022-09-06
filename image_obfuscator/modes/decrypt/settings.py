"""
Author       : noeru_desu
Date         : 2022-04-17 08:39:57
LastEditors  : noeru_desu
LastEditTime : 2022-09-06 21:32:50
Description  : 设置选项
"""
from base64 import b85decode
from pickle import loads as pickle_loads
from typing import TYPE_CHECKING, Callable, Iterable, Any

from image_obfuscator.modes.base import BaseSettings, Channels

if TYPE_CHECKING:
    from image_obfuscator.modes.base import ModeConstants
    from image_obfuscator.modes.decrypt.controller import DecryptModeController
    from image_obfuscator.modes.decrypt.panel import ProcSettingsPanel


class EncryptionParametersData(BaseSettings):
    __slots__ = SETTING_NAMES = (
        'cutting_row', 'cutting_col', 'orig_width', 'orig_height', 'shuffle_chunks',
        'flip_chunks', 'mapping_channels', 'XOR_channels', 'XOR_encryption', 'noise_XOR', 'noise_factor',
        'has_password', 'password_base85', 'version', 'dynamic_auth', 'password'
        # 需保证dynamic_auth与password在最后，参考self.serialize_encryption_parameters
    )

    def __init__(self, parameters: Iterable[Any], data = None):
        """
        Args:
            parameters: 加密参数字典或加密参数元组(一般由`self.settings_tuple`生成)
        """
        if isinstance(parameters, tuple):
            self.sync_from_tuple(parameters, False)
        else:
            self.sync_from_dict(parameters)
        self.dynamic_auth: bool = self.version >= 6
        self.password: str = None

    def sync_from_dict(self, parameters_dict: dict[str, Any]):
        self.cutting_row: int = parameters_dict['cutting_row']
        self.cutting_col: int = parameters_dict['cutting_col']
        self.orig_width: int = parameters_dict['orig_width']
        self.orig_height: int = parameters_dict['orig_height']
        self.shuffle_chunks: bool = parameters_dict['shuffle_chunks']
        self.flip_chunks: bool = parameters_dict['flip_chunks']
        self.mapping_channels: Channels = Channels(tuple(parameters_dict['mapping_channels']))
        self.XOR_channels: Channels = Channels(tuple(parameters_dict['XOR_channels']))
        self.XOR_encryption: bool = parameters_dict.get('XOR_encryption', bool(self.XOR_channels))
        self.noise_XOR: bool = parameters_dict['noise_XOR']
        self.noise_factor: int = parameters_dict['noise_factor']
        self.has_password: bool = parameters_dict['has_password']
        self.password_base85: str = parameters_dict['password_base85']
        self.version: int = parameters_dict['version']

    @staticmethod
    def deserialize_encrypted_parameters(data: str):
        pickle_data = b85decode(data)
        try:
            return pickle_loads(pickle_data)
        except ModuleNotFoundError:         # 转换旧版本pickle数据
            return pickle_loads(pickle_data.replace(
                    b'\x1aimage_encryptor', # 对2.1版本前的模块名进行转换
                    b'\x1bimage_obfuscator'
                ).replace(
                    b'\x0c_channels_id',    # 对2.0-beta版本的属性名进行转换
                    b'\r_channels_num'
            ))

    @property
    def settings(self):
        return (
            self.cutting_row, self.cutting_col,
            self.shuffle_chunks, self.flip_chunks,
            self.mapping_channels, self.XOR_encryption,
            self.XOR_channels, self.noise_XOR,
            self.noise_factor, 100 if self.password is None else self.password
        )


class EncryptionParameters(EncryptionParametersData):
    __slots__ = ()
    mode_controller: 'DecryptModeController'
    settings_panel: 'ProcSettingsPanel'
    PASSWORD_PROPERTY_NAME = 'password'
    mode_constants: 'ModeConstants' = ...

    def __init__(self, parameters: dict[str, Any] | Iterable[Any], data = None):
        super().__init__(parameters)
        super(EncryptionParametersData, self).__init__()
        self.enable_password = self.has_password

    def get_password(self):
        if not self.has_password:
            return 100
        self.password = self.main_controller.frame.password_dict.get_password(self.password_base85)
        return self.password

    def backtrack_interface(self):
        """将加密参数显示到界面"""
        self.mode_controller.cutting_row = self.cutting_row
        self.mode_controller.cutting_col = self.cutting_col
        self.mode_controller.shuffle_chunks = self.shuffle_chunks
        self.mode_controller.mapping_channels = self.mapping_channels
        self.mode_controller.flip_chunks = self.flip_chunks
        self.mode_controller.noise_XOR = self.noise_XOR
        self.mode_controller.noise_factor = self.noise_factor
        self.mode_controller.noise_factor_info = str(self.noise_factor)
        self.mode_controller.XOR_encryption = self.XOR_encryption
        self.mode_controller.XOR_channels = self.XOR_channels
        self.mode_controller.core_version = self.version
        self.settings_panel.origWidth.SetMax(self.orig_width)
        self.settings_panel.origHeight.SetMax(self.orig_height)
        w, h = self.main_frame.image_item.cache.loaded_image_size
        if self.orig_width > w:
            self.main_frame.dialog.async_warning(f'加密参数指定的裁切宽度({self.orig_width}px)超出当前图像宽度({w}px), 已自动设置为{w}px', '越界警告')
            self.orig_width = w
        if self.orig_height > h:
            self.main_frame.dialog.async_warning(f'加密参数指定的裁切高度({self.orig_height}px)超出当前图像高度({h}px), 已自动设置为{h}px', '越界警告')
            self.orig_height = h
        self.mode_controller.orig_width = self.orig_width
        self.mode_controller.orig_height = self.orig_height
        if self.has_password:
            while self.password is None:
                self.password = self.main_controller.frame.password_dict.get_password(self.password_base85)
                if self.password is not None:
                    break
                self.password = self.main_controller.frame.dialog.password_dialog(self.main_controller.frame.image_item.path_data.file_name, self.password_base85, True)
                if self.password is not None:
                    break
                self.main_controller.password = ''
                self.set_enable_password(True)
                return
            self.set_enable_password(False)
            self.main_controller.password = self.password
        else:
            self.main_controller.password = 'none'


class Settings(BaseSettings):
    __slots__ = SETTING_NAMES = (
        'cutting_row', 'cutting_col', 'shuffle_chunks', 'flip_chunks',
        'mapping_channels', 'XOR_encryption', 'XOR_channels', 'noise_XOR', 'noise_factor',
        'password', 'orig_width', 'orig_height', 'version'
    )
    mode_controller: 'DecryptModeController'
    settings_panel: 'ProcSettingsPanel'
    PASSWORD_PROPERTY_NAME = 'password'

    def __init__(self, settings: Iterable[Any] = None, data = None):
        """
        Args:
            controller (Controller): Controller实例.\n
            settings (Iterable[Any], optional): settings (Iterable[Any]): 可迭代对象(一般是由`(self.settings_tuple)`生成的元组)
            默认为None, 为None时将从界面中获取加密设置
        """
        if settings is None:
            self.sync_from_interface()
        else:
            self.sync_from_tuple(settings)
        super().__init__(settings)

    @classmethod
    def gen_settings_mapping_kwargs(cls) -> dict[int, tuple[str, Callable]]:
        mode_controller: 'DecryptModeController' = cls.mode_constants.mode_controller
        settings_panel: 'ProcSettingsPanel' = cls.mode_constants.settings_panel
        mapping_channels = ('mapping_channels', lambda event: mode_controller.mapping_channels)
        XOR_channels = ('XOR_channels', lambda event: mode_controller.XOR_channels)
        return {
            hash(settings_panel.cuttingRow): ('cutting_row', lambda event: mode_controller.cutting_row),
            hash(settings_panel.cuttingCol): ('cutting_col', lambda event: mode_controller.cutting_col),
            hash(settings_panel.shuffleChunks): ('shuffle_chunks', lambda event: mode_controller.shuffle_chunks),
            hash(settings_panel.flipChunks): ('flip_chunks', lambda event: mode_controller.flip_chunks),
            hash(settings_panel.mappingR): mapping_channels, hash(settings_panel.mappingG): mapping_channels,
            hash(settings_panel.mappingB): mapping_channels, hash(settings_panel.mappingA): mapping_channels,
            hash(settings_panel.XOREncryption): ('XOR_encryption', lambda event: mode_controller.XOR_encryption),
            hash(settings_panel.XORR): XOR_channels, hash(settings_panel.XORG): XOR_channels,
            hash(settings_panel.XORB): XOR_channels, hash(settings_panel.XORA): XOR_channels,
            hash(settings_panel.noiseXor): ('noise_XOR', lambda event: mode_controller.noise_XOR),
            hash(settings_panel.noiseFactor): ('noise_factor', lambda event: mode_controller.noise_factor),
            hash(settings_panel.origWidth): ('orig_width', lambda event: mode_controller.orig_width),
            hash(settings_panel.origHeight): ('orig_height', lambda event: mode_controller.orig_height),
            hash(settings_panel.coreVersion): ('version', lambda event: mode_controller.core_version)
        }

    def get_password(self):
        return 100 if self.password == 'none' else self.password

    def sync_from_interface(self):
        self.cutting_row = self.mode_controller.cutting_row
        self.cutting_col = self.mode_controller.cutting_col
        self.shuffle_chunks = self.mode_controller.shuffle_chunks
        self.flip_chunks = self.mode_controller.flip_chunks
        self.mapping_channels = self.mode_controller.mapping_channels
        self.XOR_encryption = self.mode_controller.XOR_encryption
        self.XOR_channels = self.mode_controller.XOR_channels
        self.noise_XOR = self.mode_controller.noise_XOR
        self.noise_factor = self.mode_controller.noise_factor
        self.version = self.mode_controller.core_version
        self.password = self.main_controller.password
        self.orig_width = self.mode_controller.orig_width
        self.orig_height = self.mode_controller.orig_height

    def backtrack_interface(self):
        """将加密设置显示到界面"""
        self.mode_controller.cutting_row = self.cutting_row
        self.mode_controller.cutting_col = self.cutting_col
        self.mode_controller.shuffle_chunks = self.shuffle_chunks
        self.mode_controller.mapping_channels = self.mapping_channels
        self.mode_controller.flip_chunks = self.flip_chunks
        self.main_controller.password = self.password
        self.mode_controller.XOR_encryption = self.XOR_encryption
        self.mode_controller.XOR_channels = self.XOR_channels
        self.mode_controller.noise_XOR = self.noise_XOR
        self.mode_controller.noise_factor = self.noise_factor
        self.mode_controller.noise_factor_info = str(self.noise_factor)
        self.mode_controller.core_version = self.version
        self.settings_panel.xorPanel.Enable(self.XOR_encryption)
        self.settings_panel.noiseFactor.Enable(self.XOR_encryption and self.noise_XOR)
        w, h = self.main_frame.image_item.cache.loaded_image_size
        self.settings_panel.origWidth.SetMax(w)
        self.settings_panel.origHeight.SetMax(h)
        if self.orig_width == 1 and self.orig_height == 1:
            self.orig_width = w
            self.orig_height = h
        else:
            if self.orig_width > w:
                self.main_frame.dialog.async_warning(f'加密参数指定的裁切宽度({self.orig_width}px)超出当前图像宽度({w}px), 已自动设置为{w}px', '越界警告')
                self.orig_width = w
            if self.orig_height > h:
                self.main_frame.dialog.async_warning(f'加密参数指定的裁切高度({self.orig_height}px)超出当前图像高度({h}px), 已自动设置为{h}px', '越界警告')
                self.orig_height = h
        self.mode_controller.orig_width = self.orig_width
        self.mode_controller.orig_height = self.orig_height
