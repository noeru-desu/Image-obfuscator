"""
Author       : noeru_desu
Date         : 2022-04-16 17:48:20
LastEditors  : noeru_desu
LastEditTime : 2023-03-25 22:26:15
"""
from traceback import format_exc
from typing import TYPE_CHECKING, Type

from wx import BoxSizer, VERTICAL, ALIGN_CENTER

from image_obfuscator.modes.base import ModeConstants
from image_obfuscator.modes import builtin_modes

if TYPE_CHECKING:
    from wx import Panel
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.types import ModeInterface, ItemSettings


class ModeManager(object):
    __slots__ = ('frame', 'mode_id_count', 'modes', 'default_mode', 'settings_panels', 'proc_settings_bsizer')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.mode_id_count = 0
        self.modes: dict[int, 'ModeInterface'] = {}
        self.default_mode: 'ModeInterface' = None
        self.settings_panels: dict[int, 'Panel'] = {}
        self.proc_settings_bsizer = BoxSizer(VERTICAL)
        self.frame.procSettingsPanelContainer.SetSizer(self.proc_settings_bsizer)
        self.proc_settings_bsizer.Fit(self.frame.procSettingsPanelContainer)

    def load_builtin_modes(self):
        for i in builtin_modes:
            self.add_mode(i)

        if self.default_mode is None:
            self.default_mode = self.modes[0]
        self.frame.controller.previous_proc_mode = self.default_mode
        self.frame.controller.proc_settings_panel = self.default_mode.settings_panel
        self.frame.procMode.Select(self.default_mode.mode_id)
        self.frame.controller.auto_show_additional_widget()

    def add_mode(self, mode_interface_cls: Type['ModeInterface']):
        mode_interface_cls.main_frame = self.frame
        mode_interface_cls.mode_id = self.mode_id_count
        mode_constants = mode_interface_cls.mode_constants = ModeConstants()
        try:
            interface = mode_interface_cls()
        except Exception:
            self.frame.dialog.async_warning(f'加载{mode_interface_cls.mode_qualname}时出现错误:\n{format_exc()}')
            return
        mode_constants.mode_interface = interface
        if __debug__ and not interface.check_metadata():
            return

        if not hasattr(interface, 'settings_panel'):
            if interface.settings_panel_cls is not None:
                interface.settings_panel = self.add_settings_panel(interface.settings_panel_cls)
            else:
                interface.settings_panel = None
        if not hasattr(interface, 'settings_controller'):
            if interface.settings_controller_cls is not None:
                interface.settings_controller = interface.settings_controller_cls()
            else:
                interface.settings_controller = None
        if interface.settings_cls is not None:
            interface.settings_cls._init_constants()
        if interface.encryption_parameters_cls is not None:
            interface.encryption_parameters_cls._init_constants()
        if not hasattr(interface, 'default_settings'):
            interface.default_settings = interface.instantiate_settings_cls(interface.default_settings_args)

        self.modes[self.mode_id_count] = self.modes[interface.mode_qualname] = interface
        self.frame.procMode.Append(interface.mode_name)

        if interface.default_mode:
            self.default_mode = interface
        self.mode_id_count += 1

    def add_settings_panel(self, panel_cls: Type['Panel']) -> 'Panel':
        cls_id = id(panel_cls)
        if cls_id in self.settings_panels:
            return self.settings_panels[cls_id]
        settings_panel = panel_cls(self.frame.procSettingsPanelContainer)
        self.proc_settings_bsizer.Add(settings_panel, 1, ALIGN_CENTER)
        self.settings_panels[cls_id] = settings_panel
        settings_panel.Hide()
        return settings_panel

    @property
    def default_mode_that_can_be_set_as_default(self):
        return self.default_mode if self.default_mode.can_be_set_as_default_mode else self.modes[0]

    @property
    def default_settings(self) -> 'ItemSettings':
        return self.default_mode.default_settings

    @default_settings.setter
    def default_settings(self, v: 'ItemSettings'):
        self.default_mode.default_settings = v
