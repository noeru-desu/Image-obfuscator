"""
Author       : noeru_desu
Date         : 2021-11-13 10:18:16
LastEditors  : noeru_desu
LastEditTime : 2022-10-31 09:10:16
"""
from atexit import register as at_exit
from orjson import dumps
from os import listdir, makedirs
from os.path import isdir, splitext, join
from threading import Lock
from typing import TYPE_CHECKING

from wx import CURSOR_ARROW, CURSOR_WAIT, DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, DirDialog

from image_obfuscator.constants import DialogReturnCodes
from image_obfuscator.frame.controller import ProgressBar
from image_obfuscator.frame.file_item import ImageItem
from image_obfuscator.modules.image import PillowImage
from image_obfuscator.modules.version_adapter import gen_encryption_attributes
from image_obfuscator.utils.thread import SingleThreadExecutor

if TYPE_CHECKING:
    from PIL.Image import Image
    from image_obfuscator.frame.controller import SaveSettings
    from image_obfuscator.frame.events import MainFrame
    from image_obfuscator.frame.file_item import PathData
    from image_obfuscator.types import ModeInterface, ItemSettings, ItemEncryptionParameters

USE_FOLDER = 5
DO_NOT_USE_FOLDER = 6


class ImageSaver(object):
    """文件保存相关功能"""
    __slots__ = (
        'frame', 'lock', 'progress_plane_displayed', 'file_count', 'loading_progress',
        'task_num', 'bar', 'filter', 'save_thread'
    )

    def __init__(self, frame: 'MainFrame'):
        """
        Args:
            frame (MainFrame): `MainFrame`实例
        """
        self.frame = frame
        # self.frame.process_pool.create_tag('bulk_save', False, False)   # 注册线程池标签
        self.save_thread = SingleThreadExecutor('save-thread')
        self.lock = Lock()
        self.progress_plane_displayed = False
        self.file_count = 0
        self.loading_progress = 0
        self.task_num = 0
        self.bar = None
        self.filter = None
        at_exit(self.save_thread.shutdown, False)

    def save_selected_image(self):
        """保存选中的图像"""
        image_item = self.frame.image_item
        if self._check():
            return
        self.frame.set_cursor(CURSOR_WAIT)
        self.show_save_progress_plane(False)
        self.frame.controller.standardized_password_ctrl()
        mode_interface = image_item.proc_mode
        settings = image_item.available_settings_inst
        cache_hash = image_item.scalable_cache_hash
        cache = image_item.cache.preview_cache.get(cache_hash)
        if cache is None:
            self.save_thread.add_task(
                self._save_task,
                (mode_interface, image_item, *settings, self.frame.controller.save_settings),
                cb=self._save_selected_image_call_back, cb_args=(cache_hash,)
            )
        else:   # 如果存在原始图像处理结果缓存则直接保存缓存
            self.frame.saveProgress.SetValue(50)
            self.save_thread.add_task(
                self._save_cache_task,
                (cache, mode_interface, image_item, settings[0], self.frame.controller.save_settings),
                cb=self.hide_save_progress_plane
            )

    def save_selected_folder(self):
        """保存选中的文件夹"""
        folder_item = self.frame.folder_item
        if self._check():
            return
        self.show_save_progress_plane(True)
        self.frame.controller.standardized_password_ctrl()
        match self.frame.dialog.confirmation_frame('是否创建与文件树层级相同的文件夹进行文件保存', cancel='取消保存操作'):
            case DialogReturnCodes.yes:
                use_folder = True
            case DialogReturnCodes.no:
                use_folder = False
            case _:
                self.hide_save_progress_plane()
                return

        self.bar = ProgressBar(self.frame.saveProgress)
        self.task_num = 0
        save_settings = self.frame.controller.save_settings
        self.lock.acquire()                                 # 锁住线程锁，防止在任务添加期间执行回调函数，而导致进度识别错误

        for top, name, image_item in folder_item.walk() if use_folder else folder_item.all_included_items():
            # image_item.standardized_proc_mode()
            settings = image_item.available_settings_inst
            cache = image_item.cache.preview_cache.record(image_item.scalable_cache_hash)
            relative_save_path = top if use_folder else ''
            if cache is None:
                self.save_thread.add_task(
                    self._save_task,
                    (image_item.proc_mode, image_item, *settings, save_settings, relative_save_path, True),
                    cb=self._bulk_save_callback
                )
            else:   # 如果存在原始图像处理结果缓存则直接保存缓存
                self.save_thread.add_task(
                    self._save_cache_task,
                    (cache, image_item.proc_mode, image_item, settings[0], save_settings, relative_save_path, True),
                    cb=self._bulk_save_from_cache_callback
                )

            self.task_num += 1

        if not self.task_num:   # 对是否分配了任务进行检查
            self.frame.dialog.async_warning('没有添加任何批量保存任务')
            self.hide_save_progress_plane()
        else:
            self.frame.set_cursor(CURSOR_WAIT)
            self.bar.next_step(self.task_num)
            self.frame.dialog.async_info(f'已添加{self.task_num}个批量保存任务')
            self.frame.saveProgressInfo.SetLabelText(f'0/{self.task_num} - 0%')
        self.lock.release()     # 任务分配完毕，释放线程锁

    def bulk_save(self):
        """批量保存"""
        if self._check():                               # 相关检查
            return
        self.show_save_progress_plane(True)
        if not self.frame.imageTreeCtrl.Selection.IsOk():
            self.frame.apply_settings_to_all()      # 如果没有选择任何文件，则将当前gui内容同步到所有image_item实例

        match self.frame.dialog.confirmation_frame('是否创建与文件树层级相同的文件夹进行文件保存', cancel='取消保存操作'):
            case DialogReturnCodes.yes:
                use_folder = True
            case DialogReturnCodes.no:
                use_folder = False
            case _:
                self.hide_save_progress_plane()
                return

        # self._gen_filter()
        self.bar = ProgressBar(self.frame.saveProgress)
        self.task_num = 0
        save_settings = self.frame.controller.save_settings
        self.lock.acquire()                                 # 锁住线程锁，防止在任务添加期间执行回调函数，而导致进度识别错误

        for image_item in self.frame.tree_manager.all_image_item_data:
            settings = image_item.available_settings_inst
            cache = image_item.cache.preview_cache.record(image_item.scalable_cache_hash)
            relative_save_path = image_item.path_data.relative_save_dir if use_folder else ''
            if cache is None:
                self.save_thread.add_task(
                    self._save_task,
                    (image_item.proc_mode, image_item, *settings, save_settings, relative_save_path, True),
                    cb=self._bulk_save_callback
                )
            else:   # 如果存在原始图像处理结果缓存则直接保存缓存
                self.save_thread.add_task(
                    self._save_cache_task,
                    (cache, image_item.proc_mode, image_item, settings[0], save_settings, relative_save_path, True),
                    cb=self._bulk_save_from_cache_callback
                )

            self.task_num += 1

        if not self.task_num:   # 对是否分配了任务进行检查
            self.frame.dialog.async_warning('没有添加任何批量保存任务')
            self.hide_save_progress_plane()
        else:
            self.frame.set_cursor(CURSOR_WAIT)
            self.bar.next_step(self.task_num)
            self.frame.dialog.async_info(f'已添加{self.task_num}个批量保存任务')
            self.frame.saveProgressInfo.SetLabelText(f'0/{self.task_num} - 0%')
        self.lock.release()     # 任务分配完毕，释放线程锁

    def cancel(self):
        """取消所有保存任务"""
        self.save_thread.clear_task()
        self.save_thread.interrupt_task()
        # self.frame.process_pool.cancel_task('bulk_save')

    def _save_task(self, mode_interface: 'ModeInterface', image_item: 'ImageItem', settings: 'ItemSettings', encryption_parameters: 'ItemEncryptionParameters', save_settings: 'SaveSettings', relative_save_path: str = '', quiet=False):
        loaded_image = image_item.cache.loaded_image
        result = (mode_interface.proc_image_quietly(
            loaded_image, True, PillowImage, settings, encryption_parameters
        ) if quiet else mode_interface.proc_image(
            loaded_image, True, PillowImage, settings, encryption_parameters,
            self.frame.saveProgressInfo.SetLabelText, self.frame.saveProgress
        ))
        if __debug__:
            image, error = result
            if error is not None:
                return result
        else:
            image = result
        if image is None:
            self.frame.dialog.async_warning('根据当前模式设置无法生成结果', '无图像可供保存')
            return result
        self._post_save_processing(
                    mode_interface,
                    settings.serialize_encryption_parameters(*loaded_image.size) if mode_interface.add_encryption_parameters_in_file else None,
                    self._save_image(image, mode_interface, image_item.path_data, save_settings, relative_save_path, quiet)
                )
        return result

    def _save_cache_task(self, image: 'Image', mode_interface: 'ModeInterface', image_item: 'ImageItem', settings: 'ItemSettings', save_settings: 'SaveSettings', relative_save_path: str = '', quiet=False):
        self._post_save_processing(
            mode_interface,
            settings.serialize_encryption_parameters(*image_item.cache.loaded_image.size) if mode_interface.add_encryption_parameters_in_file else None,
            self._save_image(image, mode_interface, image_item.path_data, save_settings, relative_save_path, quiet)
        )

    def _save_image(self, image: 'Image', mode_interface: 'ModeInterface', image_path_data: 'PathData', save_settings: 'SaveSettings', relative_save_path: str = '', quiet=False):
        name, _ = splitext(image_path_data.file_name)
        if mode_interface.file_name_suffix is not None:
            name = f"{name.removesuffix(mode_interface.file_name_suffix[0])}{mode_interface.file_name_suffix[1]}.{save_settings.format}"
        else:
            name = f"{name}.{save_settings.format}"
        save_path = join(save_settings.path, relative_save_path)
        output_path = join(save_path, name)
        if relative_save_path and not isdir(save_path):
            makedirs(save_path)
        if save_settings.format in ('jpg', 'jpeg'):
            image.convert('RGB')
        if not quiet:
            self.frame.saveProgressInfo.SetLabelText('正在保存文件')  # ! 未测试批量时的效果
        image.save(output_path, **save_settings.kwds)
        return output_path

    def _post_save_processing(self, mode_interface: 'ModeInterface', data, output_path: str):
        if mode_interface.add_encryption_parameters_in_file:
            serialized_encryption_parameters = gen_encryption_attributes(mode_interface.corresponding_decryption_mode, data)
            with open(output_path, "a") as f:
                f.write(f'\n{dumps(serialized_encryption_parameters).decode()}')

    def _check_dir(self, image_item: 'ImageItem'):
        """文件夹相关检查"""
        if not listdir(self.frame.controller.save_path):     # 是否为空文件夹
            return DO_NOT_USE_FOLDER
        if image_item.path_data.relative_path:               # 是否有多级文件夹可使用
            match self.frame.dialog.confirmation_frame(
                '{}所选的保存文件夹{}内有其他文件\n请选择处理方式'.format(image_item.path_data.file_name, self.frame.controller.save_path),
                yes='仍然保存', no='选择新的文件夹进行保存', cancel='创建文件树同级文件夹保存', help='跳过保存该文件'
            ):
                case DialogReturnCodes.yes:
                    return DO_NOT_USE_FOLDER
                case DialogReturnCodes.no:
                    return self._select_dir(image_item.path_data.root_path)
                case DialogReturnCodes.cancel:
                    return USE_FOLDER
            return
        else:
            match self.frame.dialog.confirmation_frame(
                '{}所选的保存文件夹{}内有其他文件\n请选择处理方式'.format(image_item.path_data.file_name, self.frame.controller.save_path),
                yes='仍然保存', no='选择新的文件夹进行保存', cancel='跳过保存该文件'
            ):
                case DialogReturnCodes.yes:
                    return DO_NOT_USE_FOLDER
                case DialogReturnCodes.no:
                    return self._select_dir(image_item.path_data.root_path)
            return

    def _select_dir(self, default_path):
        """选择文件夹"""
        dialog = DirDialog(self, "选择文件夹", default_path, DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST)
        if DialogReturnCodes.ok == dialog.ShowModal():
            self.frame.controller.save_path = dialog.GetPath()
            return DO_NOT_USE_FOLDER

    def _save_selected_image_call_back(self, result, cache_hash):
        """保存选中的图像完成后的回调函数"""
        self.hide_save_progress_plane()
        if __debug__:
            result, error = result
            if error is not None:
                self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')
                return
        if result is not None:
            self.frame.controller.display_and_cache_processed_preview(result, cache_hash)     # 顺便刷新一下预览图

    def _bulk_save_from_cache_callback(self, result):
        """批量保存回调函数"""
        with self.lock:     # 线程锁，防止进度累加错误
            self.bar.add()
            self.frame.controller.save_progress_info = f"{self.bar.value}/{self.task_num} - {format(self.bar.value / self.task_num * 100, '.2f')}%"
            if self.bar.value == self.task_num:
                self.frame.logger.info('完成了所有任务')
                self.hide_save_progress_plane()

    def _bulk_save_callback(self, result):
        """批量保存回调函数"""
        with self.lock:     # 线程锁，防止进度累加错误
            if __debug__:
                data, error = result
                if error is not None:
                    self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')
            self.bar.add()
            self.frame.controller.save_progress_info = f"{self.bar.value}/{self.task_num} - {format(self.bar.value / self.task_num * 100, '.2f')}%"
            if self.bar.value == self.task_num:
                self.frame.logger.info('完成了所有任务')
                self.hide_save_progress_plane()

    def __bulk_save_callback(self, future, tag_name=None, result=(None, None)):
        """批量保存回调函数"""
        # TODO result疑似无法获取(疑似ProcessTaskManager.callback出现问题)
        with self.lock:     # 线程锁，防止进度累加错误
            data, error = result
            if error is not None:
                self.frame.dialog.async_error(data, '生成加密图像时出现意外错误')
            self.bar.add()
            self.frame.controller.save_progress_info = f"{self.bar.value}/{self.task_num} - {format(self.bar.value / self.task_num * 100, '.2f')}%"
            if self.bar.value == self.task_num:
                self.frame.logger.info('完成了所有任务')
                self.hide_save_progress_plane()

    '''
    def _gen_filter(self):
        """生成过滤器"""
        self.filter = Filter(
            (0 if self.frame.encryptionFilter.Value else None, 1 if self.frame.decryptionFilter.Value else None, 2 if self.frame.qqFilter.Value else None),
            id_dict[self.frame.passwordFilter.Get3StateValue()], id_dict[self.frame.shuffleFilter.Get3StateValue()],
            id_dict[self.frame.flipFilter.Get3StateValue()], id_dict[self.frame.mappingFilter.Get3StateValue()],
            id_dict[self.frame.XorFilter.Get3StateValue()]
        )
    '''

    def _check(self):
        """常规检查(是否选择保存位置/保存位置是否存在/是否已有保存任务), 可以进行保存着返回False"""
        if not isdir(self.frame.controller.save_path):
            path = self.frame.dialog.select_dir('选择保存位置')
            if path is None:
                self.frame.dialog.error('没有选择保存文件夹或选择的文件夹不存在', '保存时出现错误')
                return True
            else:
                self.frame.controller.save_path = path
        if self.progress_plane_displayed: # or self.frame.process_pool.check_tag('bulk_save'):
            self.frame.dialog.error('请等待当前的保存任务完成', '无法执行保存操作')
            return True
        return False

    def show_save_progress_plane(self, btn):
        if self.progress_plane_displayed:
            return
        self.progress_plane_displayed = True
        self.frame.controller.save_progress = 0
        self.frame.controller.save_progress_info = ''
        if btn:
            self.frame.stopSaveBtn.Enable()
            self.frame.stopSaveBtn.Show()
        else:
            self.frame.stopSaveBtn.Hide()
        self.frame.saveBtnPanel.Hide()
        self.frame.saveProgressPanel.Show()
        self.frame.imageTreeCtrl.Disable()
        self.frame.processingOptions.Disable()
        self.frame.saveOptions.Layout()

    def hide_save_progress_plane(self, _=None):
        if not self.progress_plane_displayed:
            return
        self.progress_plane_displayed = False
        self.frame.saveProgressPanel.Hide()
        self.frame.saveBtnPanel.Show()
        self.frame.imageTreeCtrl.Enable()
        self.frame.processingOptions.Enable()
        self.frame.saveOptions.Layout()
        self.frame.set_cursor(CURSOR_ARROW)


'''
class Filter(NamedTuple):
    mode: Iterable = (0, 1, 2)
    password: int = IGNORE
    shuffle: int = IGNORE
    flip_filter: int = IGNORE
    mapping_filter: int = IGNORE
    xor_filter: int = IGNORE

    def check(self, settings: 'Settings') -> bool:
        """满足过滤要求则返回True"""
        if settings.proc_mode not in self.mode:
            return False
        if self.password is not IGNORE and convert_settings[settings.password == 'none'] is self.password:
            return False
        if self.shuffle is not IGNORE and convert_settings[settings.shuffle_chunks] is not self.shuffle:
            return False
        if self.flip_filter is not IGNORE and convert_settings[settings.flip_chunks] is not self.flip_filter:
            return False
        if self.mapping_filter is not IGNORE and convert_settings[bool(settings.mapping_channels)] is not self.mapping_filter:
            return False
        if self.xor_filter is not IGNORE and convert_settings[bool(settings.XOR_channels)] is not self.xor_filter:
            return False
        return True
'''
