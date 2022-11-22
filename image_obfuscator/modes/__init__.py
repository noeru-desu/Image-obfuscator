"""
Author       : noeru_desu
Date         : 2022-11-12 14:35:48
LastEditors  : noeru_desu
LastEditTime : 2022-11-20 21:24:29
"""
from image_obfuscator.modes.antishield import ModeInterface as AntiShieldModeInterface
from image_obfuscator.modes.encrypt import ModeInterface as EncryptModeInterface
from image_obfuscator.modes.decrypt import ModeInterface as DecryptModeInterface
from image_obfuscator.modes.mirage_tank import ModeInterface as MirageTankModeInterface
from image_obfuscator.modes.lsb_steganography import ModeInterface as LsbSteganographyModeInterface
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from image_obfuscator.types import ModeInterface

builtin_modes: tuple['ModeInterface'] = (
    EncryptModeInterface, DecryptModeInterface,
    AntiShieldModeInterface, MirageTankModeInterface,
    LsbSteganographyModeInterface
)
