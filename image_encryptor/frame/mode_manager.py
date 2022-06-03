"""
Author       : noeru_desu
Date         : 2022-04-16 17:48:20
LastEditors  : noeru_desu
LastEditTime : 2022-06-03 15:48:06
Description  : 模式管理器
"""
from typing import TYPE_CHECKING, Type

from wx import BoxSizer, VERTICAL, ALIGN_CENTER

from image_encryptor.modes.antishield import ModeInterface as AntiShieldModeInterface
from image_encryptor.modes.encrypt import ModeInterface as EncryptModeInterface
from image_encryptor.modes.decrypt import ModeInterface as DecryptModeInterface

if TYPE_CHECKING:
    from wx import Panel
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.modes.base import BaseModeInterface


class ModeManager(object):
    __slots__ = ('frame', 'mode_id_count', 'modes', 'default_mode', 'settings_panels', 'proc_settings_bsizer')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.mode_id_count = 0
        self.modes: dict[int, 'BaseModeInterface'] = {}
        self.default_mode: 'BaseModeInterface' = None
        self.settings_panels: dict[int, 'Panel'] = {}
        self.proc_settings_bsizer = BoxSizer(VERTICAL)
        self.frame.procSettingsPanelContainer.SetSizer(self.proc_settings_bsizer)
        self.proc_settings_bsizer.Fit(self.frame.procSettingsPanelContainer)

    def load_builtin_modes(self):
        self.add_mode(EncryptModeInterface)
        self.add_mode(DecryptModeInterface)
        self.add_mode(AntiShieldModeInterface)

        if self.default_mode is None:
            self.default_mode = self.modes[0]
        self.frame.controller.previous_proc_mode = self.default_mode
        self.frame.controller.proc_settings_panel = self.default_mode.settings_panel
        self.frame.procMode.Select(self.default_mode.mode_id)

    def add_mode(self, mode_interface_cls: Type['BaseModeInterface']):
        interface = mode_interface_cls(self.frame, self.mode_id_count)
        if __debug__ and not interface.check_metadata():
            return

        interface.mode_id = self.mode_id_count
        if hasattr(interface, 'settings_panel'):
            pass
        elif interface.settings_panel_cls is not None:
            interface.settings_panel = self.add_settings_panel(interface.settings_panel_cls)
        else:
            interface.settings_panel = None

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
    def default_no_encryption_parameters_required_mode(self):
        return self.modes[0] if self.default_mode.requires_encryption_parameters else self.default_mode
