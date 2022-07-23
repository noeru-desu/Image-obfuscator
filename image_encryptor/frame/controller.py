"""
Author       : noeru_desu
Date         : 2021-12-18 21:01:55
LastEditors  : noeru_desu
LastEditTime : 2022-07-23 19:37:49
Description  : 界面控制相关
"""
from os.path import splitext
from typing import TYPE_CHECKING, Callable, Iterable, Optional

from wx import Bitmap

from image_encryptor.constants import EXTENSION_KEYS
from image_encryptor.modes.base import BaseSettings, EmptySettings

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Gauge, Panel
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.tree_manager import ImageItem
    from image_encryptor.modules.image import WrappedImage
    from image_encryptor.types import ModeInterface, ItemSettings, ImageCacheHash

class ItemNotFoundError(Exception):
    pass


class Controller(object):
    "控件/控制器"
    __slots__ = (
        'frame', 'previous_saving_format', 'previous_proc_mode', 'imported_image_id', 'visible_proc_settings_panel',
        'password_ctrl_hash'
    )

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.previous_saving_format = 'png'
        self.previous_proc_mode: 'ModeInterface' = ...
        self.imported_image_id = 0
        self.visible_proc_settings_panel: Optional['Panel'] = None
        self.password_ctrl_hash = hash(self.frame.passwordCtrl)

    # ----------
    # properties
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
    def preview_plane_size(self) -> tuple[int, int]:
        if self.frame.displayedPreview.Selection != 2:
            return self.frame.imagePanel.GetSize()
        image_panel_width, image_panel_height = self.frame.imagePanel.GetSize()
        if self.preview_layout == 0:
            return image_panel_width, image_panel_height // 2
        else:
            return image_panel_width // 2, image_panel_height

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
    def saving_progress(self) -> int: return self.frame.savingProgress.GetValue()

    @saving_progress.setter
    def saving_progress(self, v): self.frame.savingProgress.SetValue(v)

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
    def saving_quality_info(self) -> str: return self.frame.qualityInfo.GetLabelText()

    @saving_quality_info.setter
    def saving_quality_info(self, v): self.frame.qualityInfo.SetLabelText(v)

    @property
    def saving_quality(self) -> int: return self.frame.savingQuality.GetValue()

    @saving_quality.setter
    def saving_quality(self, v: int): self.frame.savingQuality.SetValue(v)

    @property
    def saving_subsampling_info(self) -> str: return self.frame.subsamplingInfo.GetLabelText()

    @saving_subsampling_info.setter
    def saving_subsampling_info(self, v): self.frame.subsamplingInfo.SetLabelText(v)

    @property
    def saving_subsampling_level(self) -> int: return self.frame.subsamplingLevel.GetValue()

    @saving_subsampling_level.setter
    def saving_subsampling_level(self, v: int): self.frame.subsamplingLevel.SetValue(v)

    @property
    def saving_path(self) -> str: return self.frame.selectSavingPath.GetPath()

    @saving_path.setter
    def saving_path(self, v: str): self.frame.selectSavingPath.SetPath(v)

    @property
    def saving_format(self) -> str: return self.frame.savingFormat.GetValue()

    @saving_format.setter
    def saving_format(self, v: str): self.frame.savingFormat.SetValue(v)

    @property
    def saving_format_index(self) -> int: return EXTENSION_KEYS.index(self.frame.savingFormat.GetValue())

    @saving_format_index.setter
    def saving_format_index(self, v: int): self.frame.savingFormat.Select(v)

    @property
    def saving_progress_info(self) -> str: return self.frame.savingProgressInfo.GetLabelText()

    @saving_progress_info.setter
    def saving_progress_info(self, v: str): self.frame.savingProgressInfo.SetLabelText(v)

    @property
    def saving_progress(self) -> int: return self.frame.savingProgress.GetValue()

    @saving_progress.setter
    def saving_progress(self, v: int): self.frame.savingProgress.SetValue(v)

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
    def saving_settings(self) -> 'SavingSettings':
        """以当前的所有保存设置实例化SavingSettings类"""
        return SavingSettings(
            self.saving_path, self.saving_format_index, EXTENSION_KEYS[self.saving_format_index],
            self.saving_quality, self.saving_subsampling_level
        )

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
        self.frame.importedBitmap.Bitmap = self.frame.previewedBitmap.Bitmap = Bitmap()

    def standardized_password_ctrl(self):
        if not self.frame.update_password_dict():
            self.password = 'none'
            image_item = self.frame.image_item
            if image_item is not None and image_item.proc_mode.enable_password and image_item.proc_mode.settings_cls is not None:
                image_item.settings.sync_from_mapping(self.frame.passwordCtrl)

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

    def change_mode_plane(self, proc_mode: 'ModeInterface', settings_instance: 'ItemSettings'):
        self.proc_settings_panel = proc_mode.settings_panel
        if settings_instance is not EmptySettings:
            self.frame.procSettingsPanelContainer.Enable(settings_instance.enable_settings_panel)
            self.frame.passwordCtrl.Enable(settings_instance.enable_password)
        if not proc_mode.enable_password:
            self.password = 'none'

    def backtrack_interface(self, settings_instance: 'ItemSettings', proc_mode: 'ModeInterface' = ...):
        if proc_mode is Ellipsis:
            mode_interface = self.proc_mode_interface = self.frame.image_item.proc_mode
        else:
            mode_interface = self.proc_mode_interface = proc_mode
        self.change_mode_plane(mode_interface, settings_instance)
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
        return hash((self.controller.proc_mode_id, settings.properties_tuple, encryption_parameters.properties_tuple))

    def gen_encryption_settings_hash_with_size(self, settings: 'ItemSettings', encryption_parameters: 'ItemEncryptionParameters'):
        return hash((self.controller.proc_mode_id, settings.properties_tuple, encryption_parameters.properties_tuple, self.controller.resampling_filter_id, self.controller.preview_source, *self.controller.preview_size))
    '''

    @property
    def current_settings(self) -> 'ItemSettings':
        """以当前的所有加密设置实例化Settings类\n
        向图像实例同步设置时请使用`settings.sync_from_interface()`或`image_item.sync_options_from_interface()`
        """
        return self.proc_mode_interface.instantiate_settings_cls()

    @property
    def saving_settings(self) -> 'SavingSettings':
        """以当前的所有保存设置实例化SavingSettings类"""
        return SavingSettings(self.saving_path, self.saving_format_index, self.saving_format, self.saving_quality, self.saving_subsampling_level)


class SavingSettings(BaseSettings):
    __slots__ = SETTING_NAMES = ('path', 'format_index', 'format', 'quality', 'subsampling_level')

    def __init__(self, path: str, format_index: int, format: str, quality: int, subsampling_level: int):
        self.path = path
        self.format_index = format_index
        self.format = format
        self.quality = quality
        self.subsampling_level = subsampling_level


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
