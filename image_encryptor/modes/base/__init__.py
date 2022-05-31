"""
Author       : noeru_desu
Date         : 2022-04-16 18:08:19
LastEditors  : noeru_desu
LastEditTime : 2022-05-31 06:01:51
Description  : 基类
"""
from abc import ABC
from itertools import compress

from typing import TYPE_CHECKING, Callable, Optional, Iterable, Any, Union, Type, Iterator

if TYPE_CHECKING:
    from typing import Iterator
    from PIL.Image import Image
    from wx import Panel, Gauge
    from image_encryptor.frame.controller import Controller as MainController
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.modules.image import PillowImage, ImageData, WrappedImage


class Channels(object):
    __slots__ = ('tuple', '_hash', 'len', 'bool', '_channels_id')

    def __hash__(self) -> int:
        return self.hash

    def __iter__(self) -> Iterator:
        return self.tuple.__iter__()

    def __len__(self) -> int:
        if self.len is Ellipsis:
            self.len = self.tuple.count(True)
        return self.len

    def __bool__(self) -> bool:
        if self.bool is Ellipsis:
            self.bool = any(self.tuple)
        return self.bool

    def __init__(self, __tuple: tuple) -> None:
        self.tuple = __tuple
        self._hash: int = ...
        self.len: int = ...
        self.bool: bool = ...
        self._channels_id: tuple[int, int, int ,int] = ...

    @property
    def hash(self):
        if self._hash is Ellipsis:
            self._hash = hash(self.tuple)
        return self._hash

    @property
    def channels_id(self):
        if self._channels_id is Ellipsis:
            self._channels_id = tuple(compress((0, 1, 2, 3), self.tuple))
        return self._channels_id


class BaseSettings(ABC):
    __slots__ = ()
    SETTING_NAMES: Iterable[str]

    def __init__(self, main_controller: 'MainController', mode_controller: 'ModeController', settings: Optional[Iterable[Any]] = None) -> None: ...

    def __repr__(self) -> str:
        return ', '.join(f'{i}: {getattr(self, i)}' for i in self.SETTING_NAMES)

    def __getitem__(self, i: Any):
        if isinstance(i, str):
            return getattr(self, i)

    def inherit_tuple(self, settings: Iterable[Any]):
        """将可迭代对象(一般是由`self.properties_tuple`生成的元组)中的数据同步到自身

        Args:
            settings (Iterable[Any]): 可迭代对象(一般是由`(self.properties_tuple)`生成的元组)
        """
        assert len(self.SETTING_NAMES) == len(settings), f'Wrong settings arguments length, currently {len(settings)} (expected {len(self.SETTING_NAMES)})'
        for n, v in zip(self.SETTING_NAMES, settings):
            self.__setattr__(n, v)

    @property
    def properties(self):
        """返回`self.SETTING_NAMES`中每个属性名的值的生成器.\n
        此方法返回值必须与`ModeInterface.encryption_settings_tuple`相同,
        即`SETTING_NAMES`对应内容的类型/顺序与`encryption_settings_tuple`相同

        Returns:
            Generator: `self.SETTING_NAMES`中每个属性名的值
        """
        return (getattr(self, i) for i in self.SETTING_NAMES)

    @property
    def properties_tuple(self):
        """将`self.properties`转换为元组

        Returns:
            tuple: `self.SETTING_NAMES`中每个属性名的值的元组
        """
        return tuple(self.properties)

    @property
    def properties_hash(self):
        """`self.properties_tuple`的hash值\n
        注意: 此hash不包含`proc_mode_id`, 用于预览图缓存的hash请使用`SettingsManager`中的方法生成

        Returns:
            int: hash结果
        """
        return hash(self.properties_tuple)

    def copy(self) -> 'BaseSettings':
        """返回当前实例的浅拷贝

        Returns:
            Type[Self]: 当前实例的浅拷贝
        """
        raise NotImplementedError()

    def backtrack_interface(self):
        pass

    def encryption_parameters_dict(self, orig_width: int, orig_height: int):
        raise NotImplementedError()


class EmptySettings(BaseSettings):
    SETTING_NAMES = ()
    _instance: Optional['EmptySettings'] = None

    def __new__(cls: type['EmptySettings']):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None: pass

    def inherit_tuple(self, v): pass

    @property
    def properties(self): return ()

    @property
    def properties_tuple(self): return ()

    def copy(self): return self


class ModeController(object):
    __slots__ = ()
    """用于单一模式的控制器"""


class BaseModeInterface(ABC):
    __slots__ = ('mode_id', 'settings_panel')

    frame: 'MainFrame'

    default_mode: bool = False           # 是否为默认模式
    decryption_mode: bool = False   # 是否属于解密模式
    mode_id: int        # 模式ID
    mode_name: str = NotImplemented      # 模式的显示名称
    mode_qualname: str = NotImplemented  # 模式唯一名称 (如`builtin.mode_a`)

    settings_cls: Optional[Type['BaseSettings']] = None  # 该模式需使用的设置类
    default_settings: 'BaseSettings' = EmptySettings()

    requires_encryption_parameters: bool = False        # 是否需要读取文件末尾的加密参数
    encryption_parameters_cls: Optional[Type['BaseSettings']] = None  # 读取加密参数后实例化的参数类
    corresponding_decryption_mode: Optional[str] = None # 对应的解密模式的唯一名称
    add_encryption_parameters_in_file: bool = False     # 是否需要添加加密参数到文件结尾

    settings_controller: Optional['ModeController'] = None     # 面板控制器类
    enable_settings_panel: bool = True  # 是否启用设置面板
    enable_password: bool = True        # 是否使用密码输入框
    settings_panel: Optional['Panel']
    settings_panel_cls: Optional[Type['Panel']] = None    # 该模式的设置面板(`wx.Panel`子类)

    file_name_suffix: Optional[tuple[str, str]] = None    # 添加到文件名末尾的后缀信息(非格式后缀)

    def __init__(self, frame: 'MainFrame'):
        raise NotImplementedError()

    @property
    def encryption_settings_tuple(self):
        return None

    def proc_image(self, frame: 'MainFrame', source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'BaseSettings', label_text_setter: Callable, gauge: 'Gauge') -> tuple[Optional['WrappedImage'], Optional[str]]:
        raise NotImplementedError()

    def proc_image_independently(self, frame: 'MainFrame', source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'BaseSettings', label_text_setter: Callable, gauge: 'Gauge') -> tuple[Optional['WrappedImage'], Optional[str]]:
        raise NotImplementedError()

    def instantiate_settings_cls(self, main_controller, data: Optional[Any] = None):
        return EmptySettings() if self.settings_cls is None else self.settings_cls(main_controller, self.settings_controller, data)

    def instantiate_encryption_parameters_cls(self, main_controller, data):
        return EmptySettings() if self.encryption_parameters_cls is None else self.encryption_parameters_cls(main_controller, self.settings_controller, data)

    def check_metadata(self):
        ok = True
        if hasattr(self, 'mode_id'):
            self.frame.logger.warning('mode_id属性将会被自动设置, 手动设置值无效')
        if self.mode_qualname is NotImplemented:
            ok = False
            self.frame.logger.error('请设置mode_qualname属性作为唯一名称')
        if self.mode_name is NotImplemented:
            self.frame.logger.warning('请设置mode_name属性作为显示名称')
            self.mode_name = self.mode_qualname
        if self.add_encryption_parameters_in_file and self.corresponding_decryption_mode is None:
            ok = False
            self.frame.logger.error('add_encryption_parameters_in_file为True时请设置corresponding_decryption_mode属性')
        if not ok:
            self.frame.dialog.error('模式元数据错误, 请查看控制台')
        return ok
