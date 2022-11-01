"""
Author       : noeru_desu
Date         : 2022-07-14 18:58:24
LastEditors  : noeru_desu
LastEditTime : 2022-11-01 10:57:22
"""
from typing import Any, Generator, Iterable, Callable, Union

from wx import Panel, Event, Object
from image_obfuscator.modes.base import BaseModeSettingsPanel, BaseSettings, BaseModeInterface, EmptySettingsType, BaseModeController

if __debug__:
    print('类型提示模块被加载')

ChannelsTuple = tuple[bool, bool, bool, bool]
ChannelsHash = int
ChannelsNum = tuple[int, int, int, int]
EmptySettings = EmptySettingsType
Settings = Iterable[Any]
SettingsGenerator = Generator[Any, None, None]
SettingsTuple = tuple[Any, ...]
SettingsTupleHash = int
DataGenerator = Generator[Any, None, None]
DataTuple = tuple[Any, ...]
ModeInterface = BaseModeInterface
ModeController = BaseModeController
ItemSettings = ItemEncryptionParameters = BaseSettings
ScalableImageCacheHash = int
NormalImageCacheHash = int
ImageCacheHash = Union[ScalableImageCacheHash, NormalImageCacheHash]
SettingsDict = dict[str, Any]
class ModeSettingsPanel(Panel, BaseModeSettingsPanel): pass
ItemSettingsMappingDict = dict[int, tuple[str, Callable[[Union[Event, Object]], None]]]
