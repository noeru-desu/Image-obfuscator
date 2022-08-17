"""
Author       : noeru_desu
Date         : 2021-12-18 21:01:55
LastEditors  : noeru_desu
LastEditTime : 2022-08-17 19:39:49
Description  : 界面控制相关
"""
from json import dumps
from os.path import splitext
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Sequence, Union

from wx import VERTICAL, HORIZONTAL, Bitmap

from image_obfuscator.constants import EXTENSION_KEYS, Orientations
from image_obfuscator.modes.base import BaseSettings, EmptySettings

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Gauge, Panel, Colour, StaticBox
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.frame.tree_manager import ImageItem
    from image_obfuscator.modules.image import WrappedImage
    from image_obfuscator.types import ModeInterface, ItemSettings, ImageCacheHash

orientations = (VERTICAL, HORIZONTAL, None)


class ItemNotFoundError(Exception):
    pass


class Controller(object):
    "控件/控制器"
    __slots__ = (
        'frame', 'previous_save_format', 'previous_proc_mode', 'imported_image_id', 'visible_proc_settings_panel',
        'password_ctrl_hash', '_save_kwds_dict', 'save_kwds_json', 'proc_panel_state_association', 'preview_static_box',
        'empty_bitmap'
    )

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.empty_bitmap = Bitmap()    # 必须在wx.App实例化后创建
        self.previous_save_format = 'png'
        self.previous_proc_mode: 'ModeInterface' = ...
        self.imported_image_id = 0
        self.visible_proc_settings_panel: Optional['Panel'] = None
        self.password_ctrl_hash = hash(self.frame.passwordCtrl)
        self._save_kwds_dict: dict[str, Any] = {}
        self.save_kwds_json: str = '{\n\t\n}'
        self.preview_static_box: 'StaticBox' = frame.previewedBitmapPanel.GetSizer().GetStaticBox()
        self.proc_panel_state_association = (frame.procSettingsPanelContainer.Enable, frame.procSettingsPanelContainer.Disable, frame.procSettingsPanelContainer.Disable)

    # ----------
    # settings
    # ----------

    @property
    def proc_settings_panel(self) -> 'Panel': return self.visible_proc_settings_panel

    @proc_settings_panel.setter
    def proc_settings_panel(self, v: 'Panel'):
        if id(v) == id(self.visible_proc_settings_panel):
            return
        if self.visible_proc_settings_panel is not None:
            self.visible_proc_settings_panel.Hide()
        if v is None:
            self.visible_proc_settings_panel = None
        else:
            v.Show()
            self.frame.processingOptions.Layout()
            self.visible_proc_settings_panel = v

    @property
    def loading_progress_info(self) -> str: return self.frame.loadingProgressInfo.GetLabelText()

    @loading_progress_info.setter
    def loading_progress_info(self, v: str): self.frame.loadingProgressInfo.SetLabelText(v)

    @property
    def loading_progress(self) -> int: return self.frame.loadingProgress.GetValue()

    @loading_progress.setter
    def loading_progress(self, v: int): self.frame.loadingProgress.SetValue(v)

    @property
    def preview_panel_title(self) -> str: return self.preview_static_box.GetLabelText()

    @preview_panel_title.setter
    def preview_panel_title(self, v: str): self.preview_static_box.SetLabelText(v)

    @property
    def image_info(self) -> str: return self.frame.imageInfo.GetLabelText()

    @image_info.setter
    def image_info(self, v: str):
        try:
            self.frame.imageInfo.SetLabelText(v)
        except RuntimeError:
            return

    @property
    def imported_bitmap(self) -> 'Bitmap': return self.frame.importedBitmap.GetBitmap()

    @imported_bitmap.setter
    def imported_bitmap(self, v: 'Bitmap'):
        self.frame.importedBitmap.SetBitmap(v)
        self.frame.importedBitmapPanel.Layout()

    @property
    def preview_size(self) -> tuple[int, int]:
        return self.frame.importedBitmapSizerPanel.GetSize()

    @property
    def image_panel_size(self) -> tuple[int, int]:
        return self.frame.imagePanel.GetSize()

    @property
    def preview_plane_size(self) -> tuple[int, int]:
        if self.displayed_preview != 2:
            return self.frame.imagePanel.GetSize()
        image_panel_width, image_panel_height = self.frame.imagePanel.GetSize()
        preview_layout = self.preview_layout
        if preview_layout == 2:
            if self.frame.image_item is None:
                return image_panel_width, image_panel_height // 2
            preview_layout = self.frame.image_item.best_layout
        else:
            preview_layout = orientations[preview_layout]
        match preview_layout:
            case Orientations.vertical:
                return image_panel_width, image_panel_height // 2
            case Orientations.horizontal:
                return image_panel_width // 2, image_panel_height
        raise ValueError()

    @property
    def imported_image(self) -> 'Image': raise NotImplementedError()

    @imported_image.setter
    def imported_image(self, v: 'Image'):
        addr = id(v)
        if addr == self.imported_image_id:  # 防止重复的Image->Bitmap转换
            return
        self.imported_image_id = addr
        self.frame.importedBitmap.SetBitmap(Bitmap.FromBufferRGBA(*v.size, v.tobytes()))
        self.frame.importedBitmapPanel.Layout()

    @property
    def previewed_bitmap(self) -> 'Bitmap': return self.frame.previewedBitmap.GetBitmap()

    @previewed_bitmap.setter
    def previewed_bitmap(self, v: 'Bitmap'):
        self.frame.previewedBitmap.SetBitmap(v)
        self.frame.previewedBitmapPanel.Layout()

    @property
    def previewed_image(self) -> 'Image': raise NotImplementedError()

    @previewed_image.setter
    def previewed_image(self, v: 'WrappedImage'):
        self.frame.previewedBitmap.SetBitmap(v.wxBitmap)
        self.frame.previewedBitmapPanel.Layout()

    def set_preview_panel_bg(self, color: 'Colour'):
        self.frame.previewedBitmapSizerPanel.SetBackgroundColour(color)
        self.frame.previewedBitmapSizerPanel.Refresh()

    @property
    def displayed_preview(self) -> int:
        return self.frame.displayedPreview.GetSelection()

    @displayed_preview.setter
    def displayed_preview(self, v: int):
        self.frame.displayedPreview.Select(v)
        self.frame.change_displayed_preview(self.frame.displayedPreview)

    @property
    def preview_layout(self) -> int:
        return self.frame.previewLayout.GetSelection()

    @preview_layout.setter
    def preview_layout(self, v: int):
        self.frame.previewLayout.Select(v)
        self.frame.change_preview_layout(...)

    @property
    def preview_layout_flag(self) -> Optional[Union['VERTICAL', 'HORIZONTAL']]:
        return orientations[self.frame.previewLayout.GetSelection()]

    @preview_layout_flag.setter
    def preview_layout_flag(self, v):
        raise NotImplementedError()

    @property
    def proc_mode(self) -> int: raise NotImplementedError()

    @proc_mode.setter
    def proc_mode(self, v): raise NotImplementedError()

    @property
    def proc_mode_id(self) -> int: return self.frame.procMode.GetSelection()

    @proc_mode_id.setter
    def proc_mode_id(self, v: int): self.frame.procMode.Select(v)

    @property
    def proc_mode_interface(self) -> 'ModeInterface': return self.frame.mode_manager.modes[self.frame.procMode.GetSelection()]

    @proc_mode_interface.setter
    def proc_mode_interface(self, v: 'ModeInterface'): self.frame.procMode.Select(v.mode_id)

    @property
    def proc_mode_qualname(self) -> 'str': return self.frame.mode_manager.modes[self.frame.procMode.GetSelection()].mode_qualname

    @proc_mode_qualname.setter
    def proc_mode_qualname(self, v: 'str'): self.frame.procMode.Select(self.frame.mode_manager.modes[v].mode_id)

    def settings_source_selected(self, btn: int, sync_to_item: bool = True):
        self.proc_panel_state_association[btn]()
        if sync_to_item and self.frame.image_item is not None:
            self.frame.image_item.settings_source = btn

    @property
    def settings_source_used(self) -> int: return self.frame.SettingsSourceUsed.GetSelection()

    def set_settings_source_used(self, item_id: int, sync_to_item: bool = True):
        if self.frame.SettingsSourceUsed.GetSelection() == item_id:
            return
        if __debug__ and not self.frame.SettingsSourceUsed.IsItemEnabled(item_id):
            self.frame.dialog.warning('settings_source_used请求选中的目标已被禁用')
            self.enable_settings_source_btn(item_id, sync_to_item=sync_to_item)
        self.frame.SettingsSourceUsed.Select(item_id)
        self.settings_source_selected(item_id, sync_to_item)

    def enable_settings_source_btn(self, item_id: Union[int, Sequence[int]], select: int = ..., sync_to_item: bool = True):
        all_item_id = tuple(range(self.frame.SettingsSourceUsed.GetCount()))
        if isinstance(item_id, int):
            if self.frame.SettingsSourceUsed.GetSelection() != item_id:
                self.frame.SettingsSourceUsed.Select(item_id)
                self.settings_source_selected(item_id, sync_to_item)
                if sync_to_item and self.frame.image_item is not None:
                    self.frame.image_item.settings_source = item_id
            for i in all_item_id:
                if i == item_id:
                    self.frame.SettingsSourceUsed.EnableItem(i)
                else:
                    self.frame.SettingsSourceUsed.EnableItem(i, False)
        elif isinstance(item_id, Sequence):
            if __debug__:
                if select is not Ellipsis and select not in item_id:
                    raise ValueError('select does not exist in item_id')
            if select is Ellipsis:
                select = item_id[0]
            if self.frame.SettingsSourceUsed.GetSelection() != select:
                self.frame.SettingsSourceUsed.Select(select)
                self.settings_source_selected(select, sync_to_item)
                if sync_to_item and self.frame.image_item is not None:
                    self.frame.image_item.settings_source = select
            for i in all_item_id:
                if i in item_id:
                    self.frame.SettingsSourceUsed.EnableItem(i)
                else:
                    self.frame.SettingsSourceUsed.EnableItem(i, False)

    @property
    def password(self) -> str: return self.frame.passwordCtrl.GetValue()

    @password.setter
    def password(self, v: str): self.frame.passwordCtrl.SetValue(v)

    @property
    def preview_mode(self) -> int: return self.frame.previewMode.GetSelection()

    @preview_mode.setter
    def preview_mode(self, v: int):
        self.frame.previewMode.Select(v)
        self.frame.preview_mode_change(...)

    @property
    def preview_source(self) -> int: return self.frame.previewSource.GetSelection()

    @preview_source.setter
    def preview_source(self, v: int): self.frame.previewSource.Select(v)

    @property
    def save_progress(self) -> int: return self.frame.saveProgress.GetValue()

    @save_progress.setter
    def save_progress(self, v): self.frame.saveProgress.SetValue(v)

    @property
    def preview_progress_info(self) -> str: return self.frame.previewProgressInfo.GetLabelText()

    @preview_progress_info.setter
    def preview_progress_info(self, v): self.frame.previewProgressInfo.SetLabelText(v)

    @property
    def preview_progress(self) -> int: return self.frame.previewProgress.GetValue()

    @preview_progress.setter
    def preview_progress(self, v): self.frame.previewProgress.SetValue(v)

    @property
    def resampling_filter_id(self) -> int: return self.frame.resamplingFilter.GetSelection()

    @resampling_filter_id.setter
    def resampling_filter_id(self, v: int): self.frame.resamplingFilter.Select(v)

    @property
    def resampling_filter_name(self) -> str: return self.frame.resamplingFilter.GetStringSelection()

    @resampling_filter_name.setter
    def resampling_filter_name(self, v: str): self.frame.resamplingFilter.SetStringSelection(v)

    @property
    def max_image_pixels(self) -> int: return self.frame.maxImagePixels.GetValue()

    @max_image_pixels.setter
    def max_image_pixels(self, v): self.frame.maxImagePixels.SetValue(v)

    @property
    def stop_loading_btn_text(self) -> str: return self.frame.stopLoadingBtn.GetLabelText()

    @stop_loading_btn_text.setter
    def stop_loading_btn_text(self, v): self.frame.stopLoadingBtn.SetLabelText(v)

    @property
    def reloading_btn_text(self) -> str: return self.frame.reloadingBtn.GetLabelText()

    @reloading_btn_text.setter
    def reloading_btn_text(self, v): self.frame.reloadingBtn.SetLabelText(v)

    @property
    def save_quality_info(self) -> str: return self.frame.qualityInfo.GetLabelText()

    @save_quality_info.setter
    def save_quality_info(self, v): self.frame.qualityInfo.SetLabelText(v)

    @property
    def save_quality(self) -> int: return self.frame.saveQuality.GetValue()

    @save_quality.setter
    def save_quality(self, v: int): self.frame.saveQuality.SetValue(v)

    @property
    def save_optimize(self) -> bool: return self.frame.saveOptimize.GetValue()

    @save_optimize.setter
    def save_optimize(self, v: bool): self.frame.saveOptimize.SetValue(v)

    @property
    def save_exif(self) -> bool: return self.frame.saveExif.GetValue()

    @save_exif.setter
    def save_exif(self, v: bool): self.frame.saveExif.SetValue(v)

    @property
    def save_lossless(self) -> bool: return self.frame.saveLossless.GetValue()

    @save_lossless.setter
    def save_lossless(self, v: bool): self.frame.saveLossless.SetValue(v)

    @property
    def save_compression(self) -> str: return self.frame.saveCompression.GetStringSelection()

    @save_compression.setter
    def save_compression(self, v: str): self.frame.saveCompression.SetStringSelection(v)

    @property
    def save_subsampling_info(self) -> str: return self.frame.subsamplingInfo.GetLabelText()

    @save_subsampling_info.setter
    def save_subsampling_info(self, v): self.frame.subsamplingInfo.SetLabelText(v)

    @property
    def save_subsampling_level(self) -> int: return self.frame.subsamplingLevel.GetValue()

    @save_subsampling_level.setter
    def save_subsampling_level(self, v: int): self.frame.subsamplingLevel.SetValue(v)

    @property
    def save_path(self) -> str: return self.frame.selectSavePath.GetPath()

    @save_path.setter
    def save_path(self, v: str): self.frame.selectSavePath.SetPath(v)

    @property
    def save_format(self) -> str: return self.frame.saveFormat.GetValue()

    @save_format.setter
    def save_format(self, v: str): self.frame.saveFormat.SetValue(v)

    @property
    def save_format_index(self) -> int: return EXTENSION_KEYS.index(self.frame.saveFormat.GetValue())

    @save_format_index.setter
    def save_format_index(self, v: int): self.frame.saveFormat.Select(v)

    @property
    def save_kwds_dict(self) -> dict: return self._save_kwds_dict

    @save_kwds_dict.setter
    def save_kwds_dict(self, v: dict):
        self._save_kwds_dict = v
        self.frame.saveKwdsJson.SetValue(dumps(v))

    @property
    def save_progress_info(self) -> str: return self.frame.saveProgressInfo.GetLabelText()

    @save_progress_info.setter
    def save_progress_info(self, v: str): self.frame.saveProgressInfo.SetLabelText(v)

    @property
    def save_progress(self) -> int: return self.frame.saveProgress.GetValue()

    @save_progress.setter
    def save_progress(self, v: int): self.frame.saveProgress.SetValue(v)

    @property
    def redundant_cache_length(self) -> int:
        """启动参数: 冗余缓存最大长度

        处理结果缓存中会同时缓存多个不同加密设置生成的图像数据
        (处理结果缓存类似于LRU缓存)
        除最新缓存外的其他缓存都将在取消选择图像项目时删除

        Returns:
            int: 冗余缓存最大长度
        """
        return self.frame.redundantCacheLength.GetValue()

    @redundant_cache_length.setter
    def redundant_cache_length(self, v: int): self.frame.redundantCacheLength.SetValue(v)

    @property
    def low_memory_mode(self) -> bool:
        """启动参数: 低内存占用模式

        开启后，将在取消选中图像项目时删除相关的图像数据(包括原始数据与缓存，图像和文件信息除外)

        Returns:
            bool: 是否开启
        """
        return self.frame.lowMemoryMode.GetValue()

    @low_memory_mode.setter
    def low_memory_mode(self, v: bool): self.frame.lowMemoryMode.SetValue(v)

    @property
    def disable_cache(self) -> bool:
        """启动参数: 禁用处理结果缓存

        Returns:
            bool: 是否禁用
        """
        return self.frame.disableCache.GetValue()

    @disable_cache.setter
    def disable_cache(self, v: bool): self.frame.disableCache.SetValue(v)

    @property
    def record_interface_settings(self) -> bool:
        """启动参数: 记录界面设置

        Returns:
            bool: 是否记录
        """
        return self.frame.recordInterfaceSettings.GetValue()

    @record_interface_settings.setter
    def record_interface_settings(self, v: bool): self.frame.recordInterfaceSettings.SetValue(v)

    @property
    def record_password_dict(self) -> bool:
        """启动参数: 记录密码字典

        Returns:
            bool: 是否记录
        """
        return self.frame.recordPasswordDict.GetValue()

    @record_password_dict.setter
    def record_password_dict(self, v: bool): self.frame.recordPasswordDict.SetValue(v)

    @property
    def final_layout_widgets(self) -> bool:
        """启动参数: 记录密码字典

        Returns:
            bool: 是否记录
        """
        return self.frame.finalLayoutWidgets.GetValue()

    @final_layout_widgets.setter
    def final_layout_widgets(self, v: bool): self.frame.finalLayoutWidgets.SetValue(v)

    @property
    def default_proc_mode(self): return self.frame.mode_manager.default_mode

    def gen_image_info(self, item: 'ImageItem' = None):
        """输出图像信息至界面

        Args:
            item (ImageItem, optional): ImageItem实例. 默认为None, 输出为`未选择图像`
        """
        if item is None:
            self.image_info = '未选择图像'
        else:
            self.image_info = '大小: {}x{} 格式: {}'.format(*item.cache.loaded_image.size,
                                                        '未知' if item.no_file else splitext(item.loaded_image_path)[1].lstrip('.')
                                                        )

    def clear_preview(self):
        """取消显示所有预览图"""
        self.frame.importedBitmap.Bitmap = self.frame.previewedBitmap.Bitmap = self.empty_bitmap

    def clear_proc_preview(self):
        """取消显示处理结果预览图"""
        self.frame.previewedBitmap.Bitmap = self.empty_bitmap

    def standardized_password_ctrl(self):
        if not self.frame.update_password_dict():
            self.password = 'none'
            image_item = self.frame.image_item
            if image_item is not None and image_item.proc_mode.settings_cls is not None:
                image_item.settings.sync_from_object(self.frame.passwordCtrl)

    def display_and_cache_processed_preview(self, image: 'WrappedImage', cache_hash: 'ImageCacheHash' = ...):
        """显示并缓存处理结果

        如果`image`参数传入的实例支持缩放操作，则添加到可缩放缓存，反之则添加到普通缓存

        Args:
            image (WrappedImage): 需要显示并缓存的WrappedImage的子类实例
            cache_hash (int): 指定该预览图的`cache_hash`. 默认由`self.frame.image_item`中的信息生成
        """
        if image.scalable:
            if cache_hash is Ellipsis:
                cache_hash = self.frame.image_item.scalable_cache_hash
            self.frame.image_item.cache.previews.add_scalable_cache(cache_hash, image)
            self.previewed_bitmap = image.gen_wxBitmap(self.preview_size, self.resampling_filter_id)
        else:
            if cache_hash is Ellipsis:
                cache_hash = self.frame.image_item.normal_cache_hash
            bitmap = image.wxBitmap
            self.frame.image_item.cache.previews.add_normal_cache(cache_hash, bitmap)
            self.previewed_bitmap = bitmap

    def change_mode_plane(self, proc_mode: 'ModeInterface', image_item: 'ImageItem', settings_instance: 'ItemSettings'):
        self.proc_settings_panel = proc_mode.settings_panel
        if settings_instance is not EmptySettings:
            self.frame.passwordCtrl.Enable(settings_instance.enable_password)
            self.set_preview_panel_bg(settings_instance.preview_bg)
        if not proc_mode.enable_password:
            self.password = 'none'

    def backtrack_interface(self, settings_instance: 'ItemSettings', proc_mode: 'ModeInterface' = ..., image_item: 'ImageItem' = ...):
        if image_item is Ellipsis:
            image_item = self.frame.image_item
        if proc_mode is Ellipsis:
            mode_interface = self.proc_mode_interface = image_item.proc_mode
        else:
            mode_interface = self.proc_mode_interface = proc_mode
        self.change_mode_plane(mode_interface, image_item, settings_instance)
        settings_instance.backtrack_interface()

    '''
    @property
    def encryption_settings_hash(self):
        """当前加密设置的hash"""
        return hash((
            self.controller.proc_mode_id,
            self.controller.proc_mode_interface.encryption_settings_tuple
        ))

    @property
    def encryption_settings_hash_with_size(self):
        """在encryption_settings_hash的基础上添加resampling_filter_id/preview_source/preview_size"""
        return hash((self.controller.proc_mode_id, self.controller.proc_mode_interface.encryption_settings_tuple, self.controller.resampling_filter_id, self.controller.preview_source, *self.controller.preview_size))

    def gen_encryption_settings_hash(self, settings: 'ItemSettings', encryption_parameters: 'ItemEncryptionParameters'):
        return hash((self.controller.proc_mode_id, settings.settings_tuple, encryption_parameters.settings_tuple))

    def gen_encryption_settings_hash_with_size(self, settings: 'ItemSettings', encryption_parameters: 'ItemEncryptionParameters'):
        return hash((self.controller.proc_mode_id, settings.settings_tuple, encryption_parameters.settings_tuple, self.controller.resampling_filter_id, self.controller.preview_source, *self.controller.preview_size))
    '''

    @property
    def current_settings(self) -> 'ItemSettings':
        """以当前的所有加密设置实例化Settings类\n
        向图像实例同步设置时请使用`settings.sync_from_interface()`或`image_item.sync_options_from_interface()`
        """
        return self.proc_mode_interface.instantiate_settings_cls()

    @property
    def save_settings(self) -> 'SaveSettings':
        """以当前的所有保存设置实例化SaveSettings类"""
        return SaveSettings(
            self.save_path, self.save_format_index, self.save_format,
            self.save_quality, self.save_subsampling_level, self.save_optimize,
            self.save_exif, self.save_lossless, self.save_compression,
            self.save_kwds_dict
        )

    def sync_save_settings(self, save_settings: 'SaveSettings'):
        self.save_path = save_settings.path
        self.save_format_index = save_settings.format_index
        self.save_quality = save_settings.quality
        self.save_subsampling_level = save_settings.subsampling
        self.save_optimize = save_settings.optimize
        self.save_exif = save_settings.exif
        self.save_lossless = save_settings.lossless
        self.save_compression = save_settings.compression
        self.save_kwds_dict = save_settings.user_kwds
        self.save_kwds_json = dumps(save_settings.user_kwds, indent=2)


class SaveSettings(BaseSettings):
    __slots__ = SETTING_NAMES = (
        'path', 'format_index', 'format', 'quality', 'subsampling', 'optimize',
        'exif', 'lossless', 'compression', 'user_kwds'
    )
    kwd_names = (
        'quality', 'subsampling', 'optimize', 'exif', 'lossless', 'compression'
    )

    def __init__(
            self, path: str, format_index: int, format: str, quality: int, subsampling: int,
            optimize: bool, exif: bool, lossless: bool, compression: str, user_kwds: dict[str, Any]
        ):
        self.path = path
        self.format_index = format_index
        self.format = format
        self.quality = quality
        self.subsampling = subsampling
        self.optimize = optimize
        self.exif = exif
        self.lossless = lossless
        self.compression = compression
        self.user_kwds = user_kwds

    @property
    def kwds(self) -> dict[str, Any]:
        kwds = {k: getattr(self, k) for k in self.kwd_names}
        if kwds['compression'] == 'none':
            kwds['compression'] = None
        return kwds | self.user_kwds


class ProgressBar(object):
    __slots__ = (
        'gauge', 'gauge_range', 'total_steps', 'step_size', 'finished_step',
        'step', 'basic_progress', 'value', 'max_value', '_coefficient'
    )

    def __init__(self, gauge: 'Gauge', total_steps: int = 1):
        assert total_steps > 0, f'total_steps must be greater than 0 (currently {total_steps})'
        gauge.SetValue(0)
        self.gauge = gauge
        self.gauge_range: int = gauge.Range
        self.total_steps = total_steps
        self.step_size = self.gauge_range // total_steps
        self.finished_step = True
        self.step = 0
        self.basic_progress = 0
        self.value = 0
        self.max_value = 0
        self._coefficient = 0

    def next_step(self, max_value: int):
        if not self.finished_step:
            self.finish()
        self.finished_step = False
        self.step += 1
        self.max_value = max_value
        self.value = 0
        self._coefficient = self.step_size / max_value

    def update(self, value: int):
        assert not self.finished_step, 'Step information is not initialized, please call next_step first.'
        if value > self.max_value:
            return
        self.value = value
        self.gauge.SetValue(int(value * self._coefficient) + self.basic_progress)

    def add(self):
        self.update(self.value + 1)

    def finish(self):
        self.basic_progress = self.step_size * self.step
        self.gauge.SetValue(self.basic_progress)
        self.finished_step = True

    def over(self):
        self.gauge.SetValue(self.gauge_range)


class SegmentTrigger(object):
    __slots__ = ('_callbacks', '_initcall', '_args', '_kwargs', '_max_num', '_num')

    def __init__(self, callbacks: Iterable[Callable], initcall: Optional[Callable] = None, *init_args, **init_kwargs):
        self._callbacks = callbacks
        self._initcall = initcall
        self._args = init_args
        self._kwargs = init_kwargs
        self._max_num = len(callbacks)
        self._num = -1

    @property
    def call(self) -> Callable:
        self._num += 1
        if self._num >= self._max_num:
            self.init()
        return self._callbacks[self._num]

    def init(self):
        self._num = -1
        if self._initcall is not None:
            self._initcall(*self._args, **self._kwargs)
