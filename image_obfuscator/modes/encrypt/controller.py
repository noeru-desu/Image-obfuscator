"""
Author       : noeru_desu
Date         : 2022-04-17 13:38:35
LastEditors  : noeru_desu
LastEditTime : 2022-08-13 15:08:16
Description  : 
"""
from typing import TYPE_CHECKING, Optional

from image_obfuscator.modes.base import BaseModeController, Channels

if TYPE_CHECKING:
    from image_obfuscator.modes.encrypt.panel import ProcSettingsPanel


class EncryptModeController(BaseModeController):
    "控制器"
    __slots__ = ('mapping_checkboxes', 'XOR_checkboxes')
    _instance: Optional['EncryptModeController'] = None
    settings_panel: 'ProcSettingsPanel'

    def __new__(cls: type['EncryptModeController'], *_):
        return super().__new__(cls) if cls._instance is None else cls._instance

    def __init__(self):
        if self.__class__._instance is not None:
            return
        self.__class__._instance = self
        settings_panel = self.settings_panel
        settings_panel.xorPanel.Disable()
        self.mapping_checkboxes = (settings_panel.mappingR, settings_panel.mappingG, settings_panel.mappingB, settings_panel.mappingA)
        self.XOR_checkboxes = (settings_panel.XORR, settings_panel.XORG, settings_panel.XORB, settings_panel.XORA)

    @property
    def cutting_row(self) -> int: return self.settings_panel.cuttingRow.GetValue()

    @cutting_row.setter
    def cutting_row(self, v: int): self.settings_panel.cuttingRow.SetValue(v)

    @property
    def cutting_col(self) -> int: return self.settings_panel.cuttingCol.GetValue()

    @cutting_col.setter
    def cutting_col(self, v: int): self.settings_panel.cuttingCol.SetValue(v)

    @property
    def shuffle_chunks(self) -> bool: return self.settings_panel.shuffleChunks.GetValue()

    @shuffle_chunks.setter
    def shuffle_chunks(self, v: bool): self.settings_panel.shuffleChunks.SetValue(v)

    @property
    def flip_chunks(self) -> bool: return self.settings_panel.flipChunks.GetValue()

    @flip_chunks.setter
    def flip_chunks(self, v: bool): self.settings_panel.flipChunks.SetValue(v)

    @property
    def mapping_R(self) -> bool: return self.settings_panel.mappingR.GetValue()

    @mapping_R.setter
    def mapping_R(self, v: bool): self.settings_panel.mappingR.SetValue(v)

    @property
    def mapping_G(self) -> bool: return self.settings_panel.mappingG.GetValue()

    @mapping_G.setter
    def mapping_G(self, v: bool): self.settings_panel.mappingG.SetValue(v)

    @property
    def mapping_B(self) -> bool: return self.settings_panel.mappingB.GetValue()

    @mapping_B.setter
    def mapping_B(self, v: bool): self.settings_panel.mappingB.SetValue(v)

    @property
    def mapping_A(self) -> bool: return self.settings_panel.mappingA.GetValue()

    @mapping_A.setter
    def mapping_A(self, v: bool): self.settings_panel.mappingA.SetValue(v)

    @property
    def XOR_encryption(self) -> bool: return self.settings_panel.XOREncryption.GetValue()

    @XOR_encryption.setter
    def XOR_encryption(self, v: bool): self.settings_panel.XOREncryption.SetValue(v)

    @property
    def XOR_R(self) -> bool: return self.settings_panel.XORR.GetValue()

    @XOR_R.setter
    def XOR_R(self, v: bool): self.settings_panel.XORR.SetValue(v)

    @property
    def XOR_G(self) -> bool: return self.settings_panel.XORG.GetValue()

    @XOR_G.setter
    def XOR_G(self, v: bool): self.settings_panel.XORG.SetValue(v)

    @property
    def XOR_B(self) -> bool: return self.settings_panel.XORB.GetValue()

    @XOR_B.setter
    def XOR_B(self, v: bool): self.settings_panel.XORB.SetValue(v)

    @property
    def XOR_A(self) -> bool: return self.settings_panel.XORA.GetValue()

    @XOR_A.setter
    def XOR_A(self, v: bool): self.settings_panel.XORA.SetValue(v)

    @property
    def noise_XOR(self) -> bool: return self.settings_panel.noiseXor.GetValue()

    @noise_XOR.setter
    def noise_XOR(self, v: bool): self.settings_panel.noiseXor.SetValue(v)

    @property
    def noise_factor(self) -> int: return self.settings_panel.noiseFactor.GetValue()

    @noise_factor.setter
    def noise_factor(self, v: int): self.settings_panel.noiseFactor.SetValue(v)

    @property
    def noise_factor_info(self) -> str: return self.settings_panel.noiseFactorNum.GetLabelText()

    @noise_factor_info.setter
    def noise_factor_info(self, v): self.settings_panel.noiseFactorNum.SetLabelText(v)

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
