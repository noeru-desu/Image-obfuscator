"""
Author       : noeru_desu
Date         : 2022-04-16 18:08:19
LastEditors  : noeru_desu
LastEditTime : 2022-08-17 15:58:08
Description  : 基类
"""
from abc import ABC
from itertools import compress
from typing import (TYPE_CHECKING, Any, Callable, Iterable, Iterator, Optional,
                    Type, Union, final)
from warnings import warn

from wx import WHITE

from image_obfuscator.modules.decorator import catch_exc_and_return

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Colour, Event, Gauge, Object
    from image_obfuscator.frame.controller import Controller as MainController
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.modules.image import (ImageData, PillowImage,
                                               WrappedImage)
    from image_obfuscator.types import (ItemSettings, ItemSettingsMappingDict,
                                       ModeInterface, Settings,
                                       SettingsDict, SettingsGenerator,
                                       DataGenerator, DataTuple,
                                       SettingsTuple, SettingsTupleHash,
                                       ChannelsHash, ChannelsNum, ChannelsTuple,
                                       ModeSettingsPanel, ItemEncryptionParameters,
                                       ModeController)


class Channels(object):
    __slots__ = ('tuple', '_hash', 'len', 'bool', '_channels_num')

    def __hash__(self) -> 'ChannelsHash':
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

    def __init__(self, __tuple: 'ChannelsTuple') -> None:
        self.tuple = __tuple
        self._hash: 'ChannelsHash' = ...
        self.len: int = ...
        self.bool: bool = ...
        self._channels_num: 'ChannelsNum' = ...

    @property
    def hash(self) -> 'ChannelsHash':
        if self._hash is Ellipsis:
            self._hash = hash(self.tuple)
        return self._hash

    @property
    def channels_num(self) -> 'ChannelsNum':
        if self._channels_num is Ellipsis:
            self._channels_num = tuple(compress((0, 1, 2, 3), self.tuple))
        return self._channels_num


class ModeConstants(object):
    __slots__ = ('settings_panel', 'mode_controller', 'mode_interface')
    main_frame: 'MainFrame' = ...
    main_controller: 'MainController' = ...
    mode_interface: 'ModeInterface'

    def __init__(self):
        self.settings_panel: Optional['ModeSettingsPanel'] = None
        self.mode_controller: Optional['ModeController'] = None



class SupportConstantProperty(object):
    __slots__ = ()
    mode_constants: 'ModeConstants'

    @property
    def main_frame(self) -> 'MainFrame':
        return self.mode_constants.main_frame

    @property
    def main_controller(self) -> 'MainController':
        return self.mode_constants.main_controller

    @property
    def mode_interface(self) -> 'ModeInterface':
        return self.mode_constants.mode_interface

    @property
    def settings_panel(self) -> Optional['ModeSettingsPanel']:
        return self.mode_constants.settings_panel

    @property
    def mode_controller(self) -> Optional['ModeController']:
        return self.mode_constants.mode_controller


class LengthMismatchWarning(UserWarning):
    pass


class SettingsMapping(dict):
    __slots__ = ('settings',)

    def __init__(self, settings: 'ItemSettings', kwargs: dict[int, tuple[str, Callable]], password_property_name: Optional[str] = None):
        super().__init__(kwargs)
        self.settings = settings
        if password_property_name is not None:
            main_controller = self.settings.main_controller
            self[main_controller.password_ctrl_hash] = (password_property_name, lambda event: main_controller.password)
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


class BaseSettings(SupportConstantProperty):
    __slots__ = ('SETTINGS_MAPPING', 'enable_password', 'preview_bg')
    DATA_NAMES = ()
    SETTING_NAMES: tuple[str]
    SETTINGS_MAPPING_DICT: 'ItemSettingsMappingDict'
    PASSWORD_PROPERTY_NAME: Optional[str] = None
    SETTINGS_MAPPING: 'SettingsMapping'     # 每次实例化时都将生成新的SettingsMapping

    def __init__(self, settings: Optional[Iterable[Any]] = None, data: Optional[Iterable[Any]] = None) -> None:
        if not hasattr(self, 'enable_password'):
            self.enable_password = self.mode_interface.enable_password
        if not hasattr(self, 'preview_bg'):
            self.preview_bg = WHITE
        self.SETTINGS_MAPPING = SettingsMapping(self, self.SETTINGS_MAPPING_DICT, self.PASSWORD_PROPERTY_NAME)

    def __repr__(self) -> str:
        return ', '.join(f'{i}: {getattr(self, i)}' for i in self.SETTING_NAMES)

    def __getitem__(self, i: Any):
        if isinstance(i, str):
            return getattr(self, i)

    @classmethod
    def _init_constants(cls):
        cls.SETTINGS_MAPPING_DICT = cls.gen_settings_mapping_kwargs()

    @classmethod
    def gen_settings_mapping_kwargs(cls):
        return {}

    def set_enable_password(self, v: bool):
        self.enable_password = v
        self.main_frame.passwordCtrl.Enable(v)

    def set_preview_bg(self, color: 'Colour'):
        self.main_controller.set_preview_panel_bg(color)
        self.preview_bg = color

    def sync_from_event(self, event: 'Event'):
        self.SETTINGS_MAPPING.sync_from_event_to_settings(event)

    def sync_from_object(self, obj: 'Object'):
        self.SETTINGS_MAPPING.sync_from_object_to_settings(obj)

    def sync_from_tuple(self, settings: 'Settings', check_length=True):
        """将可迭代对象(一般是由`self.settings_tuple`生成的元组)中的数据同步到自身

        Args:
            settings (Iterable[Any]): 可迭代对象(一般是由`(self.settings_tuple)`生成的元组)
            check_length (bool): 是否检查`settings`参数与`SETTING_NAMES`属性的长度是否对应. 默认为`True`. 当检查出长度不一致时触发`LengthMismatchWarning`警告
        """
        if __debug__ and check_length and len(self.SETTING_NAMES) != len(settings):
            warn(f'Wrong settings arguments length, currently {len(settings)} (expected {len(self.SETTING_NAMES)})', LengthMismatchWarning)
        for n, v in zip(self.SETTING_NAMES, settings):
            self.__setattr__(n, v)

    def sync_data_from_tuple(self, data, check_length=True):
        """将可迭代对象(一般是由`self.data_tuple`生成的元组)中的数据同步到自身

        Args:
            settings (Iterable[Any]): 可迭代对象(一般是由`(self.settings_tuple)`生成的元组)
            check_length (bool): 是否检查`settings`参数与`SETTING_NAMES`属性的长度是否对应. 默认为`True`. 当检查出长度不一致时触发`LengthMismatchWarning`警告
        """
        if __debug__ and check_length and len(self.DATA_NAMES) != len(data):
            warn(f'Wrong settings arguments length, currently {len(data)} (expected {len(self.DATA_NAMES)})', LengthMismatchWarning)
        for n, v in zip(self.DATA_NAMES, data):
            self.__setattr__(n, v)

    @property
    def settings(self) -> 'SettingsGenerator':
        """返回`self.SETTING_NAMES`中每个属性名的值的生成器.\n
        此方法返回值必须与`ModeInterface.encryption_settings_tuple`相同,
        即`SETTING_NAMES`对应内容的类型/顺序与`encryption_settings_tuple`相同

        Returns:
            Generator: `self.SETTING_NAMES`中每个属性名的值
        """
        return (getattr(self, i) for i in self.SETTING_NAMES)

    @property
    def settings_tuple(self) -> 'SettingsTuple':
        """将`self.settings`转换为元组

        Returns:
            tuple: `self.SETTING_NAMES`中每个属性名的值的元组
        """
        return tuple(self.settings)

    @property
    def settings_hash(self) -> 'SettingsTupleHash':
        """`self.settings_tuple`的hash值\n
        注意: 此hash不包含`proc_mode_id`, 用于预览图缓存的hash请使用`Item`中的方法生成

        Returns:
            int: hash结果
        """
        return hash(self.settings_tuple)

    @property
    def settings_dict(self) -> Optional['SettingsDict']:
        """返回`self.SETTING_NAMES`中每个属性名与其值的字典.

        Returns:
            dict: {属性名: 属性值, ...}
        """
        return {k: getattr(self, k) for k in self.SETTING_NAMES}

    @settings_dict.setter
    def settings_dict(self, v: 'SettingsDict'):
        for k, _v in v.items():
            if k in self.SETTING_NAMES:
                setattr(self, k, _v)

    @property
    def data(self) -> 'DataGenerator':
        """返回`self.DATA_NAMES`中每个属性名的值的生成器.

        Returns:
            Generator: `self.DATA_NAMES`中每个属性名的值
        """
        return (getattr(self, i) for i in self.DATA_NAMES)

    @property
    def data_tuple(self) -> 'DataTuple':
        """将`self.data`转换为元组

        Returns:
            tuple: `self.DATA_NAMES`中每个属性名的值的元组
        """
        return tuple(self.data)

    def copy(self) -> 'ItemSettings':
        """返回当前实例的浅拷贝

        Returns:
            Type[Self]: 当前实例的浅拷贝
        """
        return self.__class__(self.settings_tuple, self.data_tuple)

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
    __slots__ = SETTING_NAMES = ('_', 'SETTINGS_MAPPING')
    _instance: Optional['EmptySettingsType'] = None

    def __new__(cls: type['EmptySettingsType']):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._ = None

    def create_settings_mapping(self):
        self.SETTINGS_MAPPING = SettingsMapping(self, {}, '_')

    def sync_from_tuple(self, v): pass

    def sync_from_interface(self): pass

    @property
    def settings(self): return ()

    @property
    def settings_tuple(self): return ()

    @property
    def settings_dict(self) -> None: return None

    @settings_dict.setter
    def settings_dict(self, v: Any): pass

    def copy(self): return self


EmptySettingsType.mode_constants = ModeConstants()
EmptySettings: EmptySettingsType = EmptySettingsType()


class BaseModeSettingsPanel(SupportConstantProperty):
    __slots__ = ()

    def __new__(cls, *args):
        inst = super().__new__(cls, *args)
        cls.mode_constants.settings_panel = inst
        return inst


class BaseModeController(SupportConstantProperty):
    __slots__ = ()

    def __new__(cls):
        inst = super().__new__(cls)
        cls.mode_constants.mode_controller = inst
        return inst


class BaseModeInterface(ABC):
    __slots__ = ('settings_panel', 'default_settings', 'settings_controller')

    mode_constants: 'ModeConstants'
    mode_id: int
    main_frame: 'MainFrame'
    #以上属性值均为只可自动设置

    default_mode: bool = False           # 是否为默认模式
    decryption_mode: bool = False   # 是否属于解密模式, 为True在生成预览图时，将始终提供原图进行处理
    mode_name: str = NotImplemented      # 模式的显示名称
    mode_qualname: str = NotImplemented  # 模式唯一名称 (如`builtin.mode_a`)
    can_be_set_as_default_mode: Optional[bool] = None    # 是否可被设置为默认模式(包括在没有选择图像时是否可被选择), 为None时与decryption_mode值相反

    settings_cls: Optional[Type['ItemSettings']] = None  # 该模式需使用的设置类
    default_settings_args: Optional[tuple[Any]] = None   # 实例化默认设置时使用的参数
    default_settings: 'ItemSettings'                     # 使用上方属性实例化默认设置, 一般为自动, 手动时请注意顺序

    requires_encryption_parameters: bool = False        # 是否需要读取文件末尾的加密参数
    encryption_parameters_must_be_used: bool = False      # 是否必须使用加密参数, 为True且图像加密参数不存在或不对应时将阻止用户使用此模式
    encryption_parameters_cls: Optional[Type['ItemEncryptionParameters']] = None  # 读取加密参数后实例化的参数类
    corresponding_decryption_mode: Optional[str] = None # 对应的解密模式的唯一名称
    add_encryption_parameters_in_file: bool = False     # 是否需要添加加密参数到文件结尾

    settings_controller_cls: Optional[Type['ModeController']] = None    # 面板控制器类(基类为BaseModeController)
    settings_controller: Optional['ModeController']                     # 面板控制器实例(一般为自动创建, 手动实例化时请注意顺序)
    enable_password: bool = False       # 是否使用密码输入框
    settings_panel: Optional['ModeSettingsPanel']           # 该模式的设置面板实例, 如需手动实例化,
                                                            # 请在ModeInterface.__init__中使用frame.mode_manager.add_settings_panel()进行实例化
    settings_panel_cls: Optional[Type['ModeSettingsPanel']] = None      # 该模式的设置面板(BaseModeSettingsPanel和wx.Panel的子类(务必使MRO中BaseModeSettingsPanel优先))

    file_name_suffix: Optional[tuple[str, str]] = None      # 添加到文件名末尾的后缀信息(非格式后缀)

    supports_multiprocessing = False

    def __new__(cls):
        if __debug__:
            cls.proc_image = catch_exc_and_return(cls.proc_image)
            cls.proc_image_quietly = catch_exc_and_return(cls.proc_image_quietly)
        # TODO [需要SharedMemory支持] cls.proc_image_independently = catch_exc_and_return(lambda image_data, original)
        if cls.can_be_set_as_default_mode is None:
            cls.can_be_set_as_default_mode = not cls.decryption_mode
        return super().__new__(cls)

    def __init__(self):
        """继承时请始终在最开始执行`super().__init__`"""
        if self.settings_panel_cls is not None:
            self.settings_panel_cls.mode_constants = self.mode_constants
        if self.settings_controller_cls is not None:
            self.settings_controller_cls.mode_constants = self.mode_constants
            if self.settings_cls is not None:
                self.settings_cls.mode_constants = self.mode_constants
            if self.encryption_parameters_cls is not None:
                self.encryption_parameters_cls.mode_constants = self.mode_constants

    def proc_image(self, source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'ItemSettings', encryption_parameters: 'ItemEncryptionParameters', label_text_setter: Callable, gauge: 'Gauge') -> tuple[Optional['WrappedImage'], Optional[str]]:
        raise NotImplementedError()

    def proc_image_quietly(self, source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'ItemSettings', encryption_parameters: 'ItemEncryptionParameters'):
        raise NotImplementedError()

    def proc_image_multiprocessing(self, source: 'Image', original: bool, return_type: Type[Union['PillowImage', 'ImageData']], settings: 'ItemSettings') -> tuple[Optional['WrappedImage'], Optional[str]]:
        raise NotImplementedError()

    def instantiate_settings_cls(self, data: Optional[Any] = None) -> Union[EmptySettingsType, 'ItemSettings']:
        return EmptySettings if self.settings_cls is None else self.settings_cls(data, None)

    def instantiate_encryption_parameters_cls(self, data) -> Union[EmptySettingsType, 'ItemEncryptionParameters']:
        return EmptySettings if self.encryption_parameters_cls is None else self.encryption_parameters_cls(data, None)

    @final
    def check_metadata(self):
        if self.mode_qualname is NotImplemented:
            name = self.__class__.__qualname__
        else:
            name = self.mode_qualname
        ok = True
        self.main_frame.logger.info(f'正在检查{name}的元数据')
        if self.mode_qualname is NotImplemented:
            ok = False
            self.main_frame.logger.error('请设置mode_qualname属性作为唯一名称')
        if self.mode_name is NotImplemented:
            self.main_frame.logger.warning('请设置mode_name属性作为显示名称')
            self.mode_name = self.mode_qualname
        if self.add_encryption_parameters_in_file and self.corresponding_decryption_mode is None:
            ok = False
            self.main_frame.logger.error('add_encryption_parameters_in_file为True时请设置corresponding_decryption_mode属性')
        if self.supports_multiprocessing:
            self.main_frame.logger.warning('多进程处理将不会被使用')
        if not self.can_be_set_as_default_mode and self.default_mode:
            ok = False
            self.main_frame.logger.error('can_be_set_as_default_mode与default_mode的值相冲突')
        if not ok:
            self.main_frame.dialog.error('模式元数据错误, 请查看控制台', f'加载{name}模式失败')
        return ok


class PropertyAliasMapping(dict):
    def add_alias(self, property_name, alias: Union[Iterable[str], str]):
        if isinstance(alias, str):
            self[alias] = property_name
        else:
            for i in alias:
                self[i] = property_name

    def get_property_name(self, alias) -> str:
        try:
            return self[alias]
        except KeyError as e:
            raise KeyError(f'{alias} is not an alias for any property') from e
