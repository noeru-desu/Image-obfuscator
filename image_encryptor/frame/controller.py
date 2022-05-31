"""
Author       : noeru_desu
Date         : 2021-12-18 21:01:55
LastEditors  : noeru_desu
LastEditTime : 2022-05-30 21:03:35
Description  : 界面控制相关
"""
from os.path import splitext
from typing import TYPE_CHECKING, Callable, Iterable, Optional

from wx import Bitmap

from image_encryptor.constants import EXTENSION_KEYS
from image_encryptor.modes.base import BaseSettings

if TYPE_CHECKING:
    from PIL.Image import Image
    from wx import Gauge, Panel
    from image_encryptor.frame.events import MainFrame
    from image_encryptor.frame.tree_manager import ImageItem
    from image_encryptor.modules.image import WrappedImage
    from image_encryptor.modes.base import BaseModeInterface


class ItemNotFoundError(Exception):
    pass


class Controller(object):
    "控件/控制器"
    __slots__ = ('frame', 'previous_saving_format', 'previous_proc_mode', 'imported_image_id', 'visible_proc_settings_panel')

    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.previous_saving_format = 'png'
        self.previous_proc_mode: 'BaseModeInterface' = ...
        self.imported_image_id = 0
        self.visible_proc_settings_panel: Optional['Panel'] = None

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
    def loading_progress_info(self) -> str: return self.frame.loadingProgressInfo.Label

    @loading_progress_info.setter
    def loading_progress_info(self, v: str): self.frame.loadingProgressInfo.Label = v

    @property
    def loading_progress(self) -> int: return self.frame.loadingProgress.Value

    @loading_progress.setter
    def loading_progress(self, v: int): self.frame.loadingProgress.Value = v

    @property
    def image_info(self) -> str: return self.frame.imageInfo.Label

    @image_info.setter
    def image_info(self, v: str):
        try:
            self.frame.imageInfo.Label = v
        except RuntimeError:
            return

    @property
    def imported_bitmap(self) -> 'Bitmap': return self.frame.importedBitmap.Bitmap

    @imported_bitmap.setter
    def imported_bitmap(self, v: 'Bitmap'):
        self.frame.importedBitmap.Bitmap = v
        self.frame.importedBitmapPanel.Layout()

    @property
    def imported_image(self) -> 'Image': raise NotImplementedError()

    @imported_image.setter
    def imported_image(self, v: 'Image'):
        addr = id(v)
        if addr == self.imported_image_id:  # 防止重复的Image->Bitmap转换
            return
        self.imported_image_id = addr
        self.frame.importedBitmap.Bitmap = Bitmap.FromBufferRGBA(*v.size, v.tobytes())
        self.frame.importedBitmapPanel.Layout()

    @property
    def previewed_bitmap(self) -> 'Bitmap': return self.frame.previewedBitmap.Bitmap

    @previewed_bitmap.setter
    def previewed_bitmap(self, v: 'Bitmap'):
        self.frame.previewedBitmap.Bitmap = v
        self.frame.previewedBitmapPanel.Layout()

    @property
    def previewed_image(self) -> 'Image': raise NotImplementedError()

    @previewed_image.setter
    def previewed_image(self, v: 'WrappedImage'):
        self.frame.previewedBitmap.Bitmap = v.wxBitmap
        self.frame.previewedBitmapPanel.Layout()

    @property
    def proc_mode(self) -> int: raise NotImplementedError()

    @proc_mode.setter
    def proc_mode(self, v): raise NotImplementedError()

    @property
    def proc_mode_id(self) -> int: return self.frame.procMode.Selection

    @proc_mode_id.setter
    def proc_mode_id(self, v: int): self.frame.procMode.Selection = v

    @property
    def proc_mode_interface(self) -> 'BaseModeInterface': return self.frame.mode_manager.modes[self.frame.procMode.Selection]

    @proc_mode_interface.setter
    def proc_mode_interface(self, v: 'BaseModeInterface'): self.frame.procMode.Selection = v.mode_id

    @property
    def proc_mode_qualname(self) -> 'str': return self.frame.mode_manager.modes[self.frame.procMode.Selection].mode_qualname

    @proc_mode_qualname.setter
    def proc_mode_qualname(self, v: 'str'): self.frame.procMode.Selection = self.frame.mode_manager.modes[v].mode_id

    @property
    def password(self) -> str: return self.frame.passwordCtrl.Value

    @password.setter
    def password(self, v: str): self.frame.passwordCtrl.Value = v

    @property
    def preview_mode(self) -> int: return self.frame.previewMode.Selection

    @preview_mode.setter
    def preview_mode(self, v: int): self.frame.previewMode.Selection = v

    @property
    def preview_source(self) -> int: return self.frame.previewSource.Selection

    @preview_source.setter
    def preview_source(self, v: int): self.frame.previewSource.Selection = v

    @property
    def saving_progress(self) -> int: return self.frame.savingProgress.Value

    @saving_progress.setter
    def saving_progress(self, v): self.frame.savingProgress.Value = v

    @property
    def preview_progress_info(self) -> str: return self.frame.previewProgressInfo.Label

    @preview_progress_info.setter
    def preview_progress_info(self, v): self.frame.previewProgressInfo.Label = v

    @property
    def preview_progress(self) -> int: return self.frame.previewProgress.Value

    @preview_progress.setter
    def preview_progress(self, v): self.frame.previewProgress.Value = v

    @property
    def resampling_filter_id(self) -> int: return self.frame.resamplingFilter.Selection

    @resampling_filter_id.setter
    def resampling_filter_id(self, v: int): self.frame.resamplingFilter.Selection = v

    @property
    def resampling_filter_name(self) -> str: return self.frame.resamplingFilter.StringSelection

    @resampling_filter_name.setter
    def resampling_filter_name(self, v: str): self.frame.resamplingFilter.StringSelection = v

    @property
    def max_image_pixels(self) -> int: return self.frame.maxImagePixels.Value

    @max_image_pixels.setter
    def max_image_pixels(self, v): self.frame.maxImagePixels.Value = v

    @property
    def stop_loading_btn_text(self) -> str: return self.frame.stopLoadingBtn.Label

    @stop_loading_btn_text.setter
    def stop_loading_btn_text(self, v): self.frame.stopLoadingBtn.Label = v

    @property
    def reloading_btn_text(self) -> str: return self.frame.reloadingBtn.Label

    @reloading_btn_text.setter
    def reloading_btn_text(self, v): self.frame.reloadingBtn.Label = v

    @property
    def saving_quality_info(self) -> str: return self.frame.qualityInfo.Label

    @saving_quality_info.setter
    def saving_quality_info(self, v): self.frame.qualityInfo.Label = v

    @property
    def saving_quality(self) -> int: return self.frame.savingQuality.Value

    @saving_quality.setter
    def saving_quality(self, v: int): self.frame.savingQuality.Value = v

    @property
    def saving_subsampling_info(self) -> str: return self.frame.subsamplingInfo.Label

    @saving_subsampling_info.setter
    def saving_subsampling_info(self, v): self.frame.subsamplingInfo.Label = v

    @property
    def saving_subsampling_level(self) -> int: return self.frame.subsamplingLevel.Value

    @saving_subsampling_level.setter
    def saving_subsampling_level(self, v: int): self.frame.subsamplingLevel.Value = v

    @property
    def saving_path(self) -> str: return self.frame.selectSavingPath.Path

    @saving_path.setter
    def saving_path(self, v: str): self.frame.selectSavingPath.Path = v

    @property
    def saving_format(self) -> str: return self.frame.savingFormat.Value

    @saving_format.setter
    def saving_format(self, v: str): self.frame.savingFormat.Value = v

    @property
    def saving_format_index(self) -> int: return EXTENSION_KEYS.index(self.frame.savingFormat.Value)

    @saving_format_index.setter
    def saving_format_index(self, v: int): self.frame.savingFormat.Selection = v

    @property
    def preview_size(self) -> tuple[int, int]: return self.frame.importedBitmapPanel.Size

    @property
    def saving_progress_info(self) -> str: return self.frame.savingProgressInfo.Label

    @saving_progress_info.setter
    def saving_progress_info(self, v: str): self.frame.savingProgressInfo.Label = v

    @property
    def saving_progress(self) -> int: return self.frame.savingProgress.Value

    @saving_progress.setter
    def saving_progress(self, v: int): self.frame.savingProgress.Value = v

    @property
    def redundant_cache_length(self) -> int:
        """启动参数: 冗余缓存最大长度

        处理结果缓存中会同时缓存多个不同加密设置生成的图像数据
        (处理结果缓存类似于LRU缓存)
        除最新缓存外的其他缓存都将在取消选择图像项目时删除

        Returns:
            int: 冗余缓存最大长度
        """
        return self.frame.redundantCacheLength.Value

    @redundant_cache_length.setter
    def redundant_cache_length(self, v: int): self.frame.redundantCacheLength.Value = v

    @property
    def low_memory_mode(self) -> bool:
        """启动参数: 低内存占用模式

        开启后，将在取消选中图像项目时删除相关的图像数据(包括原始数据与缓存，图像和文件信息除外)

        Returns:
            bool: 是否开启
        """
        return self.frame.lowMemoryMode.Value

    @low_memory_mode.setter
    def low_memory_mode(self, v: bool): self.frame.lowMemoryMode.Value = v

    @property
    def disable_cache(self) -> bool:
        """启动参数: 禁用处理结果缓存

        Returns:
            bool: 是否禁用
        """
        return self.frame.disableCache.Value

    @disable_cache.setter
    def disable_cache(self, v: bool): self.frame.disableCache.Value = v

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
        """取消显示所有缓存"""
        self.frame.importedBitmap.Bitmap = self.frame.previewedBitmap.Bitmap = Bitmap()

    def standardized_password_ctrl(self):
        if not self.frame.update_password_dict():
            self.password = 'none'

    def display_and_cache_processed_preview(self, image: 'WrappedImage'):
        """显示并缓存处理结果

        如果`image`参数传入的实例支持缩放操作，则添加到可缩放缓存，反之则添加到普通缓存

        Args:
            image (WrappedImage): 需要显示并缓存的WrappedImage的子类实例
        """
        if image.scalable:
            self.frame.image_item.cache.previews.add_scalable_cache(self.frame.settings.encryption_settings_hash, image)
            self.previewed_bitmap = image.gen_wxBitmap(self.preview_size, self.resampling_filter_id)
        else:
            bitmap = image.wxBitmap
            self.frame.image_item.cache.previews.add_normal_cache(self.frame.settings.encryption_settings_hash_with_size, bitmap)
            self.previewed_bitmap = bitmap

    def backtrack_interface(self, settings_instance: 'BaseSettings', proc_mode: 'BaseModeInterface' = ...):
        if proc_mode is Ellipsis:
            mode_interface = self.proc_mode_interface = self.frame.image_item.proc_mode
        else:
            mode_interface = self.proc_mode_interface = proc_mode
        self.proc_settings_panel = mode_interface.settings_panel
        self.frame.procSettingsPanelContainer.Enable(mode_interface.enable_settings_panel)
        self.frame.passwordCtrl.Enable(mode_interface.enable_password)
        settings_instance.backtrack_interface()


class SettingsManager(object):
    __slots__ = ('controller', 'default')

    def __init__(self, controller: 'Controller'):
        self.controller = controller
        self.default = controller.default_proc_mode.default_settings

    @property
    def encryption_settings(self):
        """当前所有加密设置的元组, 一般为生成encryption_settings_hash时使用"""
        return self.controller.proc_mode_interface.encryption_settings_tuple

    @property
    def encryption_settings_hash(self):
        """当前加密设置的hash"""
        return hash((self.controller.proc_mode_id, self.encryption_settings))

    @property
    def encryption_settings_hash_with_size(self):
        """在encryption_settings_hash的基础上添加resampling_filter_id/preview_source/preview_size"""
        return hash((self.controller.proc_mode_id, self.encryption_settings, self.controller.resampling_filter_id, self.controller.preview_source, *self.controller.preview_size))

    def gen_encryption_settings_hash(self, settings: 'BaseSettings'):
        return hash((self.controller.proc_mode_id, settings.properties_tuple))

    def gen_encryption_settings_hash_with_size(self, settings: 'BaseSettings'):
        return hash((self.controller.proc_mode_id, settings.properties_tuple, self.controller.resampling_filter_id, self.controller.preview_source, *self.controller.preview_size))

    @property
    def all(self) -> 'BaseSettings':
        """以当前的所有加密设置实例化Settings类"""
        return self.controller.proc_mode_interface.instantiate_settings_cls(self.controller)

    @property
    def saving_settings(self) -> 'SavingSettings':
        """以当前的所有保存设置实例化SavingSettings类"""
        return self.controller.saving_settings


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
        gauge.Value = 0
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
        self.gauge.Value = int(value * self._coefficient) + self.basic_progress

    def add(self):
        self.update(self.value + 1)

    def finish(self):
        self.gauge.Value = self.basic_progress = self.step_size * self.step
        self.finished_step = True

    def over(self):
        self.gauge.Value = self.gauge_range


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
