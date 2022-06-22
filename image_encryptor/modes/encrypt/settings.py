"""
Author       : noeru_desu
Date         : 2022-04-17 08:40:06
LastEditors  : noeru_desu
LastEditTime : 2022-06-22 11:29:56
Description  : 
"""
from base64 import b85encode
from pickle import dumps as pickle_dumps
from typing import TYPE_CHECKING, Iterable, Any

from image_encryptor.constants import EA_VERSION
from image_encryptor.modes.base import BaseSettings, Channels
from image_encryptor.modes.decrypt.settings import EncryptionParametersData
from image_encryptor.modules.password_verifier import PasswordDict

if TYPE_CHECKING:
    from image_encryptor.frame.controller import Controller as MainController
    from image_encryptor.modes.encrypt.controller import EncryptModeController


class SettingsData(BaseSettings):
    __slots__ = SETTING_NAMES = (
        'cutting_row', 'cutting_col', 'shuffle_chunks', 'flip_chunks',
        'mapping_channels', 'XOR_encryption', 'XOR_channels', 'noise_XOR', 'noise_factor',
        'password'
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
        return EncryptionParametersData((self.cutting_row, self.cutting_col, orig_width, orig_height, self.shuffle_chunks,
                                        self.flip_chunks, self.mapping_channels,
                                        self.XOR_channels if self.XOR_encryption else Channels((False, False, False, False)),
                                        self.XOR_encryption, self.noise_XOR, self.noise_factor, has_password,
                                        PasswordDict.get_validation_field_base85(password) if has_password else 0, EA_VERSION,
                                        True, self.password))

    @property
    def available_password(self):
        return 100 if self.password == 'none' else self.password

    def copy(self):
        return SettingsData(self.properties_tuple)

    def serialize_encryption_parameters(self, orig_width: int, orig_height: int):
        encryption_parameters_data = self.encryption_parameters_data(orig_width, orig_height)
        return b85encode(pickle_dumps(tuple(getattr(encryption_parameters_data, i) for i in EncryptionParametersData.SETTING_NAMES[:-2]))).decode('utf-8')


class Settings(SettingsData):
    __slots__ = ('main_controller', 'mode_controller')

    def __init__(self, main_controller: 'MainController', mode_controller: 'EncryptModeController', settings: Iterable[Any] = None):
        """
        Args:
            controller (Controller): Controller实例.\n
            settings (Iterable[Any], optional): settings (Iterable[Any]): 可迭代对象(一般是由`(self.properties_tuple)`生成的元组)
            默认为None, 为None时将从界面中获取加密设置
        """
        self.main_controller = main_controller
        self.mode_controller = mode_controller
        if settings is None:
            self._init()
        else:
            super().__init__(settings)

    def _init(self):
        self.cutting_row = self.mode_controller.cutting_row
        self.cutting_col = self.mode_controller.cutting_col
        self.shuffle_chunks = self.mode_controller.shuffle_chunks
        self.flip_chunks = self.mode_controller.flip_chunks
        self.mapping_channels = self.mode_controller.mapping_channels
        self.XOR_encryption = self.mode_controller.XOR_encryption
        self.XOR_channels = self.mode_controller.XOR_channels
        self.noise_XOR = self.mode_controller.noise_XOR
        self.noise_factor = self.mode_controller.noise_factor
        self.password = self.main_controller.password

    def backtrack_interface(self):
        """将加密设置显示到界面"""
        # if self.controller.proc_mode == ANTISHIELD_MODE:
        #     self.controller.frame.processingSettingsPanel.Disable()
        #     self.controller.frame.passwordCtrl.Disable()
        # else:
        #     self.controller.frame.processingSettingsPanel.Enable()
        #     self.controller.frame.passwordCtrl.Enable()
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
        self.mode_controller.settings_panel.xorPanel.Enable(self.XOR_encryption)

    def copy(self):
        return Settings(self.main_controller, self.mode_controller, self.properties_tuple)
