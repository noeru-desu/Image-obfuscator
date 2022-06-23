"""
Author       : noeru_desu
Date         : 2022-04-17 08:39:57
LastEditors  : noeru_desu
LastEditTime : 2022-06-22 11:24:31
Description  : 设置选项
"""
from base64 import b85decode
from pickle import loads as pickle_loads
from typing import TYPE_CHECKING, Iterable, Any, Union

from image_encryptor.modes.base import BaseSettings, Channels

if TYPE_CHECKING:
    from image_encryptor.frame.controller import Controller as MainController
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
            self._inherit_dict_settings(parameters)
        self.dynamic_auth: bool = self.version >= 6
        self.password: str = None

    def _inherit_dict_settings(self, parameters_dict: dict[str, Any]):
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
    __slots__ = ('main_controller', 'mode_controller')

    def __init__(self, main_controller: 'MainController', mode_controller: 'EncryptModeController', parameters: dict[str, Any] | Iterable[Any]):
        self.main_controller = main_controller
        self.mode_controller = mode_controller
        super().__init__(parameters)

    def get_password(self):
        if not self.has_password:
            return 100
        if self.password is not None:
            return self.password
        self.password = self.main_controller.frame.password_dict.get_password(self.password_base85)
        return None if self.password is None else self.password

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
        if self.has_password:
            while self.password is None:
                self.password = self.main_controller.frame.password_dict.get_password(self.password_base85)
                if self.password is not None:
                    break
                self.password = self.main_controller.frame.dialog.password_dialog(self.main_controller.frame.image_item.path_data.file_name, self.password_base85, True)
                if self.password is not None:
                    break
                self.main_controller.password = ''
                self.main_controller.frame.passwordCtrl.Enable()
                return
            self.main_controller.frame.passwordCtrl.Disable()
            self.main_controller.password = self.password
        else:
            self.main_controller.frame.passwordCtrl.Disable()
            self.main_controller.password = 'none'
