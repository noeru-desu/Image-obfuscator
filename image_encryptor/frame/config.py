"""
Author       : noeru_desu
Date         : 2022-06-07 06:20:01
LastEditors  : noeru_desu
LastEditTime : 2022-08-06 18:25:31
Description  : 
"""
from pickle import dump as pickle_dump, load as pickle_load
from contextlib import suppress
from collections import namedtuple
from os import getenv, mkdir, startfile
from os.path import join, exists, isfile
from traceback import format_exc
from typing import TYPE_CHECKING

from image_encryptor.constants import FRAME_SETTINGS_MAIN_VERSION, FRAME_SETTINGS_SUB_VERSION

if TYPE_CHECKING:
    from image_encryptor.frame.events import MainFrame


class ConfigManager(object):
    __slots__ = (
        'frame', 'data_path', 'frame_settings_path', 'password_dict_path', 'default_frame_settings',
        'FrameConfig', 'image_items_path'
    )

    def __init__(self, frame: 'MainFrame') -> None:
        self.frame = frame
        self.data_path = join(getenv('LOCALAPPDATA', 'pickles'), 'ImageEncryptor')
        self.frame_settings_path = join(self.data_path, 'frame_settings.pickle')
        self.password_dict_path = join(self.data_path, 'password_dict.pickle')
        self.image_items_path = join(self.data_path, 'image_items.pickle')
        if not exists(self.data_path):
            mkdir(self.data_path)
        self.default_frame_settings = self.gen_frame_settings()
        self.FrameConfig = namedtuple('FrameConfig', (
            'config_version', 'default_proc_mode', 'default_mode_settings', 'startup_parameters',
            'preview_mode', 'displayed_preview', 'preview_layout', 'preview_source',
            'resampling_filter', 'save_settings', 'max_image_pixels'
        ), defaults=tuple(self.default_frame_settings.items()))

    def open_config_folder(self):
        startfile(self.data_path)

    def gen_frame_settings(self):
        if self.frame.controller.proc_mode_interface.requires_encryption_parameters:
            default_proc_mode = self.frame.mode_manager.default_no_encryption_parameters_required_mode
            if self.frame.mode_manager.default_mode.requires_encryption_parameters:
                default_mode_settings = default_proc_mode.default_settings
            else:
                default_mode_settings = self.frame.mode_manager.default_settings
        else:
            default_proc_mode = self.frame.controller.proc_mode_interface
            default_mode_settings = self.frame.controller.current_settings
        return {
            'config_version': (FRAME_SETTINGS_MAIN_VERSION, FRAME_SETTINGS_SUB_VERSION),
            'default_proc_mode': default_proc_mode.mode_qualname,
            'default_mode_settings': default_mode_settings.properties_dict,
            'startup_parameters': self.frame.startup_parameters.parameters_dict,
            'preview_mode': self.frame.controller.preview_mode,
            'displayed_preview': self.frame.controller.displayed_preview,
            'preview_layout': self.frame.controller.preview_layout,
            'preview_source': self.frame.controller.preview_source,
            'resampling_filter': self.frame.controller.resampling_filter_id,
            'save_settings': self.frame.controller.save_settings,
            'max_image_pixels': self.frame.controller.max_image_pixels
            }

    def save_password_dict(self):
        with open(self.password_dict_path, 'wb') as f:
            pickle_dump(self.frame.password_dict.copy(), f)

    def load_password_dict(self):
        if not isfile(self.password_dict_path):
            return
        with open(self.password_dict_path, 'rb') as f:
            with suppress(Exception):
                self.frame.password_dict |= pickle_load(f)

    def save_frame_settings(self):
        with open(self.frame_settings_path, 'wb') as f:
            pickle_dump(self.gen_frame_settings(), f)

    def load_frame_settings(self):
        if not isfile(self.frame_settings_path):
            return
        with open(self.frame_settings_path, 'rb') as f:
            try:
                data_dict = self.default_frame_settings.copy() | pickle_load(f)
                if data_dict['config_version'][0] != FRAME_SETTINGS_MAIN_VERSION:
                    self.frame.logger.info('配置文件版本过高, 跳过加载')
                    return
                elif data_dict['config_version'][1] != FRAME_SETTINGS_SUB_VERSION:
                    frame_settings = self.FrameConfig(**{k: v for k, v in data_dict.items() if k in self.default_frame_settings.keys()})
                else:
                    frame_settings = self.FrameConfig(**data_dict)
            except Exception:
                self.frame.logger.warning('读取配置文件时出现错误\n{}'.format(format_exc().rstrip('\r\n')))
                self.frame.logger.warning('出现此问题不影响程序使用, 可能是配置文件版本过高导致')
                return
        if not frame_settings.startup_parameters.get('record_interface_settings', True):
            return
        try:
            if frame_settings.default_proc_mode in self.frame.mode_manager.modes:
                default_mode = self.frame.mode_manager.default_mode = self.frame.mode_manager.modes[frame_settings.default_proc_mode]
                default_settings = default_mode.instantiate_settings_cls()
                default_settings.properties_dict = frame_settings.default_mode_settings
                self.frame.mode_manager.default_settings = default_settings
                self.frame.controller.backtrack_interface(default_settings, default_mode)
            self.frame.startup_parameters.parameters_dict = frame_settings.startup_parameters
            self.frame.controller.preview_mode = frame_settings.preview_mode
            self.frame.controller.displayed_preview = frame_settings.displayed_preview
            self.frame.controller.preview_layout = frame_settings.preview_layout
            self.frame.controller.preview_source = frame_settings.preview_source
            self.frame.controller.resampling_filter_id = frame_settings.resampling_filter
            self.frame.controller.sync_save_settings(frame_settings.save_settings)
            self.frame.controller.max_image_pixels = frame_settings.max_image_pixels
        except Exception:
            self.frame.logger.warning('应用配置文件时出现错误\n{}'.format(format_exc().rstrip('\r\n')))
            self.frame.logger.warning('出现此问题不影响程序使用, 可能是配置文件版本过高导致')

    def save_loaded_image_items(self):
        image_items = (
            [() for path, mode, settings in self.frame.tree_manager.all_folder_item_data],
            [() for path, mode, settings in self.frame.tree_manager.all_image_item_data]
        )
        with open(self.image_items_path, 'wb') as f:
            pickle_dump(self.gen_frame_settings(), f)
