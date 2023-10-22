"""
Author       : noeru_desu
Date         : 2022-06-07 06:20:01
LastEditors  : noeru_desu
LastEditTime : 2023-03-26 09:35:03
"""
from pickle import dumps as pickle_dumps, load as pickle_load, HIGHEST_PROTOCOL
from pickletools import optimize
from contextlib import suppress
from collections import namedtuple
from os import mkdir, startfile
from os.path import join, exists, isfile
from traceback import format_exc
from typing import TYPE_CHECKING

from image_obfuscator.constants import FRAME_SETTINGS_MAIN_VERSION, FRAME_SETTINGS_SUB_VERSION, LOCAL_APPDATA, LOCAL_APPDATA_TEMP

if TYPE_CHECKING:
    from image_obfuscator.frame.events import MainFrame


class ConfigManager(object):
    __slots__ = (
        'frame', 'frame_settings_path', 'password_dict_path', 'default_frame_settings',
        'FrameConfig', 'loaded_frame_settings_dict'
    )

    def __init__(self, frame: 'MainFrame') -> None:
        self.frame = frame
        self.loaded_frame_settings_dict = None
        self.frame_settings_path = join(LOCAL_APPDATA, 'frame_settings.pickle')
        self.password_dict_path = join(LOCAL_APPDATA, 'password_dict.pickle')
        if not exists(LOCAL_APPDATA):
            mkdir(LOCAL_APPDATA)

    def init(self):
        self.default_frame_settings = self.gen_frame_settings()
        self.FrameConfig = namedtuple('FrameConfig', (
            'config_version', 'default_proc_mode', 'default_mode_settings', 'program_options',
            'preview_mode', 'displayed_preview', 'preview_layout', 'preview_source',
            'resampling_filter', 'save_settings', 'max_image_pixels', 'window_size',
            'window_maximized'
        ), defaults=tuple(self.default_frame_settings.items()))

    def open_config_folder(self):
        startfile(LOCAL_APPDATA)

    def gen_frame_settings(self, init=False):
        if not (init or self.frame.controller.proc_mode_interface.can_be_set_as_default_mode):
            default_proc_mode = self.frame.mode_manager.default_mode_that_can_be_set_as_default
            default_mode_settings = default_proc_mode.default_settings
        else:
            default_proc_mode = self.frame.controller.proc_mode_interface
            default_mode_settings = self.frame.controller.current_settings
        return {
            'config_version': (FRAME_SETTINGS_MAIN_VERSION, FRAME_SETTINGS_SUB_VERSION),
            'window_maximized': self.frame.IsMaximized(),
            'window_size': self.frame.GetSize(),
            'default_proc_mode': default_proc_mode.mode_qualname,
            'default_mode_settings': default_mode_settings.settings_dict,
            'program_options': self.frame.program_options.parameters_dict,
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
            f.write(optimize(pickle_dumps(self.frame.password_dict.copy(), HIGHEST_PROTOCOL)))

    def load_password_dict(self):
        if not isfile(self.password_dict_path):
            return
        with open(self.password_dict_path, 'rb') as f:
            with suppress(Exception):
                self.frame.password_dict |= pickle_load(f)

    def save_frame_settings(self):
        with open(self.frame_settings_path, 'wb') as f:
            f.write(optimize(pickle_dumps(self.gen_frame_settings(), HIGHEST_PROTOCOL)))

    def restore_default_temp_dir(self):
        if 'program_options' in self.loaded_frame_settings_dict:
            self.loaded_frame_settings_dict['program_options']['temp_dir'] = LOCAL_APPDATA_TEMP
        with open(self.frame_settings_path, 'wb') as f:
            f.write(optimize(pickle_dumps(self.loaded_frame_settings_dict, HIGHEST_PROTOCOL)))

    def load_frame_settings(self):
        if not isfile(self.frame_settings_path):
            return False
        with open(self.frame_settings_path, 'rb') as f:
            try:
                self.loaded_frame_settings_dict = pickle_load(f)
                program_options = self.loaded_frame_settings_dict['program_options']
                if program_options.get('record_interface_settings', True):
                    self.frame.program_options.parameters_dict = program_options
            except Exception:
                self.loaded_frame_settings_dict = {}
                self.frame.logger.warning('载入配置文件时出现错误\n{}'.format(format_exc().rstrip('\r\n')))
                self.frame.logger.warning('出现此问题不影响程序使用, 可能是配置文件版本过高导致')
            finally:
                return True

    def apply_frame_settings(self):
        if self.loaded_frame_settings_dict is None:
            if not self.load_frame_settings():
                return
        data_dict = self.default_frame_settings.copy() | self.loaded_frame_settings_dict
        if not self.frame.program_options.record_interface_settings:
            return
        try:
            if data_dict['config_version'][0] != FRAME_SETTINGS_MAIN_VERSION:
                self.frame.logger.info('配置文件版本过高, 跳过加载')
                return
            elif data_dict['config_version'][1] != FRAME_SETTINGS_SUB_VERSION:
                frame_settings = self.FrameConfig(**{k: v for k, v in data_dict.items() if k in self.default_frame_settings.keys()})
            else:
                frame_settings = self.FrameConfig(**data_dict)
        except Exception:
            self.frame.logger.warning('转换配置文件时出现错误\n{}'.format(format_exc().rstrip('\r\n')))
            self.frame.logger.warning('出现此问题不影响程序使用, 可能是配置文件版本过高导致')
            return
        try:
            if frame_settings.window_maximized:
                self.frame.Maximize()
            else:
                self.frame.SetSize(frame_settings.window_size)
            self.frame.Layout()
            if frame_settings.default_proc_mode in self.frame.mode_manager.modes:
                default_mode = self.frame.mode_manager.default_mode = self.frame.mode_manager.modes[frame_settings.default_proc_mode]
                self.frame.controller.previous_proc_mode = default_mode
                default_settings = default_mode.instantiate_settings_cls()
                default_settings.settings_dict = frame_settings.default_mode_settings
                self.frame.mode_manager.default_settings = default_settings
                self.frame.controller.backtrack_interface(default_settings, default_mode)
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
