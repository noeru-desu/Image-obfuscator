"""
Author       : noeru_desu
Date         : 2022-07-14 18:58:24
LastEditors  : noeru_desu
LastEditTime : 2022-07-15 18:32:53
Description  : 用于类型提示
"""
from typing import Any, Generator, Iterable, Callable, Union

from wx import Panel, Event, Object
from image_encryptor.modes.base import BaseModeSettingsPanel, BaseSettings, BaseModeInterface


ChannelsTuple = tuple[bool, bool, bool, bool]
ChannelsHash = int
ChannelsNum = tuple[int, int, int, int]
Properties = Iterable[Any]
PropertiesGenerator = Generator[Any, None, None]
PropertiesTuple = tuple[Any, ...]
PropertiesTupleHash = int
ModeInterface = BaseModeInterface
ItemSettings = ItemEncryptionParameters = BaseSettings
ScalableImageCacheHash = int
NormalImageCacheHash = int
ImageCacheHash = Union[ScalableImageCacheHash, NormalImageCacheHash]
PropertiesDict = dict[str, Any]
class ModeSettingsPanel(Panel, BaseModeSettingsPanel): pass
ItemSettingsMappingDict = dict[int, tuple[str, Callable[[Union[Event, Object]], None]]]
