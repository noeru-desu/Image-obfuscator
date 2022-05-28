"""
Author       : noeru_desu
Date         : 2022-04-17 13:38:35
LastEditors  : noeru_desu
LastEditTime : 2022-05-28 19:56:52
Description  : 
"""
from typing import TYPE_CHECKING, Optional

from image_encryptor.modes.base import ModeController, Channels

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.modes.encrypt.panel import ProcSettingsPanel


class EncryptModeController(ModeController):
    "控制器"
    __slots__ = ('frame', 'settings_panel', 'mapping_checkboxes', 'XOR_checkboxes')
    _instance: Optional['EncryptModeController'] = None

    def __new__(cls: type['EncryptModeController'], *_):
        return super().__new__(cls) if cls._instance is None else cls._instance

    def __init__(self, frame: 'MainFrame', settings_panel: 'ProcSettingsPanel'):
        if self.__class__._instance is not None:
            return
        self.__class__._instance = self
        self.frame = frame
        self.settings_panel = settings_panel
        settings_panel.xorPanel.Disable()
        self.mapping_checkboxes = (settings_panel.mappingR, settings_panel.mappingG, settings_panel.mappingB, settings_panel.mappingA)
        self.XOR_checkboxes = (settings_panel.XORR, settings_panel.XORG, settings_panel.XORB, settings_panel.XORA)

    @property
    def cutting_row(self) -> int: return self.settings_panel.cuttingRow.Value

    @cutting_row.setter
    def cutting_row(self, v: int): self.settings_panel.cuttingRow.Value = v

    @property
    def cutting_col(self) -> int: return self.settings_panel.cuttingCol.Value

    @cutting_col.setter
    def cutting_col(self, v: int): self.settings_panel.cuttingCol.Value = v

    @property
    def shuffle_chunks(self) -> bool: return self.settings_panel.shuffleChunks.Value

    @shuffle_chunks.setter
    def shuffle_chunks(self, v: bool): self.settings_panel.shuffleChunks.Value = v

    @property
    def flip_chunks(self) -> bool: return self.settings_panel.flipChunks.Value

    @flip_chunks.setter
    def flip_chunks(self, v: bool): self.settings_panel.flipChunks.Value = v

    @property
    def mapping_R(self) -> bool: return self.settings_panel.mappingR.Value

    @mapping_R.setter
    def mapping_R(self, v: bool): self.settings_panel.mappingR.Value = v

    @property
    def mapping_G(self) -> bool: return self.settings_panel.mappingG.Value

    @mapping_G.setter
    def mapping_G(self, v: bool): self.settings_panel.mappingG.Value = v

    @property
    def mapping_B(self) -> bool: return self.settings_panel.mappingB.Value

    @mapping_B.setter
    def mapping_B(self, v: bool): self.settings_panel.mappingB.Value = v

    @property
    def mapping_A(self) -> bool: return self.settings_panel.mappingA.Value

    @mapping_A.setter
    def mapping_A(self, v: bool): self.settings_panel.mappingA.Value = v

    @property
    def XOR_encryption(self) -> bool: return self.settings_panel.XOREncryption.Value

    @XOR_encryption.setter
    def XOR_encryption(self, v: bool): self.settings_panel.XOREncryption.Value = v

    @property
    def XOR_R(self) -> bool: return self.settings_panel.XORR.Value

    @XOR_R.setter
    def XOR_R(self, v: bool): self.settings_panel.XORR.Value = v

    @property
    def XOR_G(self) -> bool: return self.settings_panel.XORG.Value

    @XOR_G.setter
    def XOR_G(self, v: bool): self.settings_panel.XORG.Value = v

    @property
    def XOR_B(self) -> bool: return self.settings_panel.XORB.Value

    @XOR_B.setter
    def XOR_B(self, v: bool): self.settings_panel.XORB.Value = v

    @property
    def XOR_A(self) -> bool: return self.settings_panel.XORA.Value

    @XOR_A.setter
    def XOR_A(self, v: bool): self.settings_panel.XORA.Value = v

    @property
    def noise_XOR(self) -> bool: return self.settings_panel.noiseXor.Value

    @noise_XOR.setter
    def noise_XOR(self, v: bool): self.settings_panel.noiseXor.Value = v

    @property
    def noise_factor(self) -> int: return self.settings_panel.noiseFactor.Value

    @noise_factor.setter
    def noise_factor(self, v: int): self.settings_panel.noiseFactor.Value = v

    @property
    def noise_factor_info(self) -> str: return self.settings_panel.noiseFactorNum.Label

    @noise_factor_info.setter
    def noise_factor_info(self, v): self.settings_panel.noiseFactorNum.Label = v

    @property
    def mapping_channels(self) -> 'Channels':
        """选择的需要随机映射的各通道字符串

        Returns:
            tuple: 以RGBA顺序对应的bool
        """
        return Channels((self.mapping_R, self.mapping_G, self.mapping_B, self.mapping_A))

    @mapping_channels.setter
    def mapping_channels(self, v: 'Channels'):
        for i, j in zip(self.mapping_checkboxes, v.tuple):
            i.SetValue(j)

    @property
    def XOR_channels(self) -> 'Channels':
        """选择的需要异或加密的各通道字符串

        Returns:
            tuple: 以RGBA顺序对应的bool
        """
        return Channels((self.XOR_R, self.XOR_G, self.XOR_B, self.XOR_A))

    @XOR_channels.setter
    def XOR_channels(self, v: 'Channels'):
        for i, j in zip(self.XOR_checkboxes, v.tuple):
            i.SetValue(j)
