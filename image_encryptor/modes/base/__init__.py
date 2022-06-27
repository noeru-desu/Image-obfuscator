"""
Author       : noeru_desu
Date         : 2022-04-16 18:08:19
LastEditors  : noeru_desu
LastEditTime : 2022-06-27 08:43:38
Description  : 基类
"""
from abc import ABC
from warnings import warn
from itertools import compress

from image_encryptor.modules.decorator import catch_exc_and_return

from typing import TYPE_CHECKING, Callable, Optional, Iterable, Any, Union, Type, Iterator, final

if TYPE_CHECKING:
    from typing import Iterator
    from PIL.Image import Image
    from wx import Panel, Gauge, Event, Object
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


class LengthMismatchWarning(UserWarning):
    pass


class SettingsMapping(dict):
    __slots__ = ('settings',)

    def __init__(self, settings: 'BaseSettings', kwargs: dict[int, tuple[str, Callable]], password_property_name: Optional[str] = None):
        super().__init__(kwargs)
        self.settings = settings
        if password_property_name is not None:
            MAIN_CONTROLLER = self.settings.MAIN_CONTROLLER
            self[MAIN_CONTROLLER.password_ctrl_hash] = (password_property_name, lambda event: MAIN_CONTROLLER.password)
        if __debug__:
            self.check_mapping()

    def check_mapping(self):
        for k, v in self.items():
            assert isinstance(k, int), f'The keys of SettingsMapping must be int, currently {type(k)}'
            attr = v[0]
            assert hasattr(self.settings, attr), f"'{type(self.settings)}' object has no attribute '{attr}'"

    def sync_from_object_to_settings(self, _object: 'Object'):
        _hash = hash(_object)
        if _hash in self:
            attr, setter = self[_hash]
            setattr(self.settings, attr, setter(_object))

    def sync_from_event_to_settings(self, event: 'Event'):
        _hash = hash(event.GetEventObject())
        if _hash in self:
            attr, setter = self[_hash]
            setattr(self.settings, attr, setter(event))


class BaseSettings(ABC):
    __slots__ = ('SETTINGS_MAPPING', 'enable_password', 'enable_settings_panel')
    SETTING_NAMES: tuple[str]
    SETTINGS_MAPPING_DICT: 'dict[int, tuple[str, Callable[[Union[Event, Object]], None]]]'
    PASSWORD_PROPERTY_NAME: Optional[str] = None
    MAIN_CONTROLLER: 'MainController'
    MODE_CONTROLLER: Optional['ModeController']
    MODE_INTERFACE: 'BaseModeInterface'
    SETTINGS_MAPPING: 'SettingsMapping'     # 每次实例化时都将生成新的SettingsMapping

    def __init__(self, settings: Optional[Iterable[Any]] = None) -> None:
        self.SETTINGS_MAPPING = SettingsMapping(self, self.SETTINGS_MAPPING_DICT, self.PASSWORD_PROPERTY_NAME)
        self.enable_password = self.MODE_INTERFACE.enable_password
        self.enable_settings_panel = self.MODE_INTERFACE.enable_settings_panel

    def __repr__(self) -> str:
        return ', '.join(f'{i}: {getattr(self, i)}' for i in self.SETTING_NAMES)

    def __getitem__(self, i: Any):
        if isinstance(i, str):
            return getattr(self, i)

    @classmethod
    def set_constants(cls, main_controller: 'MainController', mode_interface: 'BaseModeInterface'):
        cls.MODE_INTERFACE = mode_interface
        cls.MAIN_CONTROLLER = main_controller
        cls.MODE_CONTROLLER = mode_interface.settings_controller
        cls.SETTINGS_MAPPING_DICT = cls.gen_settings_mapping_kwargs()

    @classmethod
    def gen_settings_mapping_kwargs(cls):
        return {}

    def set_enable_password(self, v: bool):
        self.enable_password = v
        self.MAIN_CONTROLLER.frame.passwordCtrl.Enable(v)

    def set_enable_settings_panel(self, v: bool):
        self.enable_settings_panel = v
        self.MAIN_CONTROLLER.frame.passwordCtrl.Enable(v)

    def sync_from_event(self, event: 'Event'):
        self.SETTINGS_MAPPING.sync_from_event_to_settings(event)

    def sync_from_mapping(self, _object: 'Object'):
        self.SETTINGS_MAPPING.sync_from_object_to_settings(_object)

    def sync_from_tuple(self, settings: Iterable[Any], check_length=True):
        """将可迭代对象(一般是由`self.properties_tuple`生成的元组)中的数据同步到自身

        Args:
            settings (Iterable[Any]): 可迭代对象(一般是由`(self.properties_tuple)`生成的元组)
            check_length (bool): 是否检查`settings`参数与`SETTING_NAMES`属性的长度是否对应. 默认为`True`. 当检查出长度不一致时触发`LengthMismatchWarning`警告
        """
        if __debug__ and check_length and len(self.SETTING_NAMES) != len(settings):
            warn(f'Wrong settings arguments length, currently {len(settings)} (expected {len(self.SETTING_NAMES)})', LengthMismatchWarning)
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

    @property
    def properties_dict(self) -> Optional[dict]:
        """返回`self.SETTING_NAMES`中每个属性名与其值的字典.

        Returns:
            dict: {属性名: 属性值, ...}
        """
        return {k: getattr(self, k) for k in self.SETTING_NAMES}

    @properties_dict.setter
    def properties_dict(self, v: dict):
        for k, _v in v.items():
            if k in self.SETTING_NAMES:
                setattr(self, k, _v)

    def copy(self) -> 'BaseSettings':
        """返回当前实例的浅拷贝

        Returns:
            Type[Self]: 当前实例的浅拷贝
        """
        return self.__class__(self.properties_tuple)

    def backtrack_interface(self):
        pass

    def sync_from_interface(self):
        raise NotImplementedError()

    def serialize_encryption_parameters(self, orig_width: int, orig_height: int) -> str:
        raise NotImplementedError()

    @classmethod
    def deserialize_encrypted_parameters(cls, data: str) -> Any:
        raise NotImplementedError()


class EmptySettingsType(BaseSettings):
    """空的设置实例, 用于占位, 实例为单例"""
    __slots__ = SETTING_NAMES = ('_',)
    _instance: Optional['EmptySettingsType'] = None

    def __new__(cls: type['EmptySettingsType'], main_controller):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, main_controller) -> None:
        self._ = None

    def set_constants(self, main_controller: 'MainController'):
        cls = self.__class__
        cls.MAIN_CONTROLLER = main_controller
        cls.SETTINGS_MAPPING = SettingsMapping(self, {}, '_')

    def on_init(self): ...

    def sync_from_tuple(self, v): pass

    def sync_from_interface(self): pass

    @property
    def properties(self): return ()

    @property
    def properties_tuple(self): return ()

    @property
    def properties_dict(self) -> None: return None

    @properties_dict.setter
    def properties_dict(self, v: Any): pass

    def copy(self): return self


EmptySettings = EmptySettingsType(...)


class ModeController(object):
    __slots__ = ()
    """用于单一模式的控制器"""


class BaseModeInterface(ABC):
    __slots__ = ('mode_id', 'settings_panel')

    frame: 'MainFrame'

    default_mode: bool = False           # 是否为默认模式
    decryption_mode: bool = False   # 是否属于解密模式
    mode_id: int        # 模式ID, 将被自动设置
    mode_name: str = NotImplemented      # 模式的显示名称
    mode_qualname: str = NotImplemented  # 模式唯一名称 (如`builtin.mode_a`)

    settings_cls: Optional[Type['BaseSettings']] = None  # 该模式需使用的设置类
    default_settings: 'BaseSettings' = EmptySettings

    requires_encryption_parameters: bool = False        # 是否需要读取文件末尾的加密参数
    encryption_parameters_cls: Optional[Type['BaseSettings']] = None  # 读取加密参数后实例化的参数类
    corresponding_decryption_mode: Optional[str] = None # 对应的解密模式的唯一名称
    add_encryption_parameters_in_file: bool = False     # 是否需要添加加密参数到文件结尾

    settings_controller: Optional['ModeController'] = None     # 面板控制器类
    enable_settings_panel: bool = True  # 是否启用设置面板
    enable_password: bool = False       # 是否使用密码输入框
    settings_panel: Optional['Panel']                       # 该模式的设置面板实例, 如需手动实例化,
                                                            # 请在ModeInterface.__init__中使用frame.mode_manager.add_settings_panel()进行实例化
    settings_panel_cls: Optional[Type['Panel']] = None      # 该模式的设置面板(`wx.Panel`子类)

    file_name_suffix: Optional[tuple[str, str]] = None      # 添加到文件名末尾的后缀信息(非格式后缀)

    supports_multiprocessing = False

    def __new__(cls, frame: 'MainFrame', mode_id: int):
        if __debug__:
            cls.proc_image = catch_exc_and_return(cls.proc_image)
            cls.proc_image_quietly = catch_exc_and_return(cls.proc_image_quietly)
        # TODO [需要SharedMemory支持] cls.proc_image_independently = catch_exc_and_return(lambda image_data, original)
        return super().__new__(cls)

    def __init__(self, frame: 'MainFrame', mode_id: int):
        if self.settings_controller is not None:
            if self.settings_cls is not None:
                self.settings_cls.set_constants(frame.controller, self)
            if self.encryption_parameters_cls is not None:
                self.encryption_parameters_cls.set_constants(frame.controller, self)

    @property
    def encryption_settings_tuple(self):
        return None

    def proc_image(self, frame: 'MainFrame', source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'BaseSettings', encryption_parameters: 'BaseSettings', label_text_setter: Callable, gauge: 'Gauge') -> tuple[Optional['WrappedImage'], Optional[str]]:
        raise NotImplementedError()

    def proc_image_quietly(self, frame: 'MainFrame', source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'BaseSettings', encryption_parameters: 'BaseSettings'):
        raise NotImplementedError()

    def proc_image_multiprocessing(self, source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'BaseSettings') -> tuple[Optional['WrappedImage'], Optional[str]]:
        raise NotImplementedError()

    def instantiate_settings_cls(self, data: Optional[Any] = None):
        return EmptySettings if self.settings_cls is None else self.settings_cls(data)

    def instantiate_encryption_parameters_cls(self, data):
        return EmptySettings if self.encryption_parameters_cls is None else self.encryption_parameters_cls(data)

    @final
    def check_metadata(self):
        if self.mode_qualname is NotImplemented:
            name = self.__class__.__qualname__
        else:
            name = self.mode_qualname
        ok = True
        self.frame.logger.info(f'正在检查{name}的元数据')
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
        if self.supports_multiprocessing:
            self.frame.logger.warning('多进程处理将不会被使用')
        if not ok:
            self.frame.dialog.error('模式元数据错误, 请查看控制台')
        return ok
