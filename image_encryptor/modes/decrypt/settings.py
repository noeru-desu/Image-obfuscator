"""
Author       : noeru_desu
Date         : 2022-04-17 08:39:57
LastEditors  : noeru_desu
LastEditTime : 2022-06-27 08:43:14
Description  : 设置选项
"""
from base64 import b85decode
from pickle import loads as pickle_loads
from typing import TYPE_CHECKING, Iterable, Any

from image_encryptor.modes.base import BaseSettings, Channels

if TYPE_CHECKING:
    from image_encryptor.modes.encrypt.controller import EncryptModeController


class EncryptionParametersData(BaseSettings):
    __slots__ = SETTING_NAMES = (
        'cutting_row', 'cutting_col', 'orig_width', 'orig_height', 'shuffle_chunks',
        'flip_chunks', 'mapping_channels', 'XOR_channels', 'XOR_encryption', 'noise_XOR', 'noise_factor',
        'has_password', 'password_base85', 'version', 'dynamic_auth', 'password'
        # 需保证dynamic_auth与password在最后，参考self.serialize_encryption_parameters
    )

    def __init__(self, parameters: Iterable[Any]):
        """
        Args:
            parameters: 加密参数字典或加密参数元组(一般由`self.properties_tuple`生成)
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
        return pickle_loads(b85decode(data))

    @property
    def properties(self):
        return (
            self.cutting_row, self.cutting_col,
            self.shuffle_chunks, self.flip_chunks,
            self.mapping_channels, self.XOR_encryption,
            self.XOR_channels, self.noise_XOR,
            self.noise_factor, 100 if self.password is None else self.password
        )


class EncryptionParameters(EncryptionParametersData):
    __slots__ = ()
    MODE_CONTROLLER: 'EncryptModeController'
    PASSWORD_PROPERTY_NAME = 'password'

    def __init__(self, parameters: dict[str, Any] | Iterable[Any]):
        super().__init__(parameters)
        super(EncryptionParametersData, self).__init__()
        self.set_enable_password(self.has_password)

    def get_password(self):
        if not self.has_password:
            return 100
        self.password = self.MAIN_CONTROLLER.frame.password_dict.get_password(self.password_base85)
        if self.password is None:
            return None
        return self.password

    def backtrack_interface(self):
        """将加密参数显示到界面"""
        self.MODE_CONTROLLER.cutting_row = self.cutting_row
        self.MODE_CONTROLLER.cutting_col = self.cutting_col
        self.MODE_CONTROLLER.shuffle_chunks = self.shuffle_chunks
        self.MODE_CONTROLLER.mapping_channels = self.mapping_channels
        self.MODE_CONTROLLER.flip_chunks = self.flip_chunks
        self.MODE_CONTROLLER.noise_XOR = self.noise_XOR
        self.MODE_CONTROLLER.noise_factor = self.noise_factor
        self.MODE_CONTROLLER.noise_factor_info = str(self.noise_factor)
        self.MODE_CONTROLLER.XOR_encryption = self.XOR_encryption
        self.MODE_CONTROLLER.XOR_channels = self.XOR_channels
        if self.has_password:
            while self.password is None:
                self.password = self.MAIN_CONTROLLER.frame.password_dict.get_password(self.password_base85)
                if self.password is not None:
                    break
                self.password = self.MAIN_CONTROLLER.frame.dialog.password_dialog(self.MAIN_CONTROLLER.frame.image_item.path_data.file_name, self.password_base85, True)
                if self.password is not None:
                    break
                self.MAIN_CONTROLLER.password = ''
                self.set_enable_password(True)
                return
            self.set_enable_password(False)
            self.MAIN_CONTROLLER.password = self.password
        else:
            self.MAIN_CONTROLLER.password = 'none'
