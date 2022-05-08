"""
Author       : noeru_desu
Date         : 2021-11-13 10:18:16
LastEditors  : noeru_desu
LastEditTime : 2022-05-08 13:52:06
Description  : 文件保存功能
"""
from atexit import register as at_exit
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from os.path import isdir
from threading import Lock
from typing import TYPE_CHECKING, Iterable, NamedTuple

from wx import (CHK_CHECKED, CHK_UNCHECKED, CHK_UNDETERMINED, DIRP_CHANGE_DIR,
                DIRP_DIR_MUST_EXIST, DirDialog)

import image_encryptor.modes.anti_shielded as anti_shielded
import image_encryptor.modes.decrypt as decrypt
import image_encryptor.modes.encrypt as encrypt
from image_encryptor.constants import DialogReturnCodes, ProcModes
from image_encryptor.frame.controls import ProgressBar
from image_encryptor.frame.file_item import ImageItem

if TYPE_CHECKING:
    from concurrent.futures import Future
    from image_encryptor.frame.controls import Settings
    from image_encryptor.frame.events import MainFrame

ENABLE = 2
DISABLE = 3
IGNORE = 4
USE_FOLDER = 5
DO_NOT_USE_FOLDER = 6

id_dict = {CHK_UNDETERMINED: IGNORE, CHK_CHECKED: ENABLE, CHK_UNCHECKED: DISABLE}
convert_settings = {True: ENABLE, False: DISABLE}


class ImageSaver(object):
    """文件保存相关功能"""
    __slots__ = (
        'frame', 'lock', 'progress_plane_displayed', 'file_count', 'loading_progress',
        'task_num', 'bar', 'filter', 'saving_thread_pool'
    )

    def __init__(self, frame: 'MainFrame'):
        """
        Args:
            frame (MainFrame): `MainFrame`实例
        """
        self.frame = frame
        self.frame.process_pool.create_tag('bulk_save', False, False)   # 注册线程池标签
        self.saving_thread_pool = ThreadPoolExecutor(self.frame.process_pool._max_workers, 'saving_thread_pool')
        self.lock = Lock()
        self.progress_plane_displayed = False
        self.file_count = 0
        self.loading_progress = 0
        self.task_num = 0
        self.bar = None
        self.filter = None
        at_exit(self.saving_thread_pool.shutdown, wait=False, cancel_futures=True)

    def save_selected_image(self):
        """保存选中的图像"""
        if self.frame.image_item is None:
            self.frame.dialog.async_error('没有选择图像')
            return
        if self._check():   # 相关合法性检查
            return
        self.show_saving_progress_plane(False)
        if not self.frame.update_password_dict():   # 检查密码栏内容是否合法
            self.frame.controls.password = 'none'
        cache = self.frame.image_item.cache.previews.get_scalable_cache(self.frame.settings.encryption_settings_hash)
        if cache is None:
            match self.frame.controls.proc_mode:
                case ProcModes.encryption_mode:
                    self.saving_thread_pool.submit(
                        encrypt.normal,
                        self.frame, self.frame.savingProgressInfo.SetLabelText, self.frame.savingProgress,
                        self.frame.image_item.cache.loaded_image, True
                    ).add_done_callback(self._save_selected_image_call_back)
                case ProcModes.decryption_mode:
                    self.saving_thread_pool.submit(
                        decrypt.normal,
                        self.frame, self.frame.savingProgressInfo.SetLabelText, self.frame.savingProgress,
                        self.frame.image_item.cache.loaded_image, True
                    ).add_done_callback(self._save_selected_image_call_back)
                case ProcModes.anti_shielded_mode:
                    self.saving_thread_pool.submit(
                        anti_shielded.normal,
                        self.frame, self.frame.savingProgressInfo.SetLabelText, self.frame.savingProgress,
                        self.frame.image_item.cache.loaded_image, True, True
                    ).add_done_callback(self._save_selected_image_call_back)
        else:   # 如果存在原始图像处理结果缓存则直接保存缓存
            settings = self.frame.settings.all
            self.frame.savingProgress.SetValue(50)
            self.frame.savingProgressInfo.SetLabelText('正在保存文件')
            match self.frame.controls.proc_mode:
                case ProcModes.encryption_mode:
                    self.saving_thread_pool.submit(
                        encrypt.save_image,
                        cache, self.frame.image_item.path_data, settings.saving_path, settings.saving_format, settings.saving_quality,
                        settings.saving_subsampling_level,
                        settings.encryption_parameters_data(*self.frame.image_item.cache.loaded_image.size).encryption_parameters_dict
                    ).add_done_callback(self._save_selected_image_from_cache_call_back)
                case ProcModes.decryption_mode:
                    self.saving_thread_pool.submit(
                        decrypt.save_image,
                        cache, self.frame.image_item.path_data, settings.saving_path, settings.saving_format, settings.saving_quality,
                        settings.saving_subsampling_level
                    ).add_done_callback(self._save_selected_image_from_cache_call_back)
                case ProcModes.anti_shielded_mode:
                    self.saving_thread_pool.submit(
                        anti_shielded.save_image,
                        cache, self.frame.image_item.path_data, settings.saving_path, settings.saving_format, settings.saving_quality,
                        settings.saving_subsampling_level
                    ).add_done_callback(self._save_selected_image_from_cache_call_back)
            self.frame.savingProgress.SetValue(100)
            self.frame.savingProgressInfo.SetLabelText('完成')

    def _save_selected_image_call_back(self, future: 'Future'):
        """保存选中的图像完成后的回调函数"""
        self.hide_saving_progress_plane()
        data, error = future.result()
        if error is not None:
            self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')
        else:
            self.frame.controls.display_and_cache_processed_preview(data)     # 顺便刷新一下预览图

    def _save_selected_image_from_cache_call_back(self, future: 'Future'):
        """保存选中的图像完成后的回调函数"""
        self.hide_saving_progress_plane()
        data, error = future.result()
        if error is not None:
            self.frame.dialog.async_error(error, '生成加密图像时出现意外错误')

    def bulk_save(self):
        """批量保存"""
        if not self.frame.tree_manager.file_dict:
            self.frame.dialog.async_error('没有载入图像')
            return
        if self._check():                               # 相关合法性检查
            return
        self.show_saving_progress_plane(True)
        if self.frame.imageTreeCtrl.Selection.IsOk():   # 检查是否选择了某一文件
            image_data = self.frame.tree_manager.selected_item_data
            if isinstance(image_data, ImageItem):                  # 是否选择的是文件夹，如果不是，则同步gui内容至对应image_item实例
                image_data.settings = self.frame.settings.all
        else:
            self.frame.apply_settings_to_all()      # 如果没有选择任何文件，则将当前gui内容同步到所有image_item实例

        match self.frame.dialog.confirmation_frame('是否创建与文件树层级相同的文件夹进行文件保存', cancel='取消保存操作'):
            case DialogReturnCodes.yes:
                use_folder = True
            case DialogReturnCodes.no:
                use_folder = False
            case _:
                self.hide_saving_progress_plane()
                return

        self._gen_filter()
        self.bar = ProgressBar(self.frame.savingProgress)
        self.task_num = 0
        self.lock.acquire()                                 # 锁住线程锁，防止在任务添加期间执行回调函数，而导致进度识别错误

        for image_item in self.frame.tree_manager.all_image_item_data:
            if not self.filter.check(image_item.settings):      # 进行设置过滤
                continue
            uf = False                                      # use_folder的局部变量名
            if not use_folder:                              # 对未使用多级文件夹的情况的一些询问
                result = self._check_dir(image_item)
                if result == DO_NOT_USE_FOLDER:
                    pass
                elif result == USE_FOLDER:
                    uf = True
                else:
                    continue
            else:
                uf = True

            cache = image_item.cache.previews.get_scalable_cache(image_item.settings.encryption_settings_hash)
            if cache is None:
                loaded_image = image_item.cache.loaded_image
                image_data = ('RGBA', loaded_image.size, loaded_image.tobytes())  # 打包所需的可序列化对象(图像数据方面)
                match image_item.settings.proc_mode:
                    case ProcModes.encryption_mode:
                        self.frame.process_pool.add_task('bulk_save', self.frame.process_pool.submit(
                            encrypt.batch, image_data, image_item.path_data, image_item.settings.properties_tuple,
                            self.frame.settings.saving_settings.properties_tuple, uf
                        ), self._bulk_save_callback)
                    case ProcModes.decryption_mode:
                        image_item.cache.encryption_parameters.password = self.frame.password_dict.get_password(
                            image_item.cache.encryption_parameters.password_base64
                        )
                        if image_item.cache.encryption_parameters.password is None:
                            self.frame.logger.warning(f'[{image_item.path_data.file_name}]未找到密码，跳过保存')
                            continue
                        self.frame.process_pool.add_task('bulk_save', self.frame.process_pool.submit(
                            decrypt.batch, image_data, image_item.path_data, image_item.cache.encryption_parameters.properties_tuple,
                            self.frame.settings.saving_settings.properties_tuple, uf
                        ), self._bulk_save_callback)
                    case ProcModes.anti_shielded_mode:
                        self.frame.process_pool.add_task('bulk_save', self.frame.process_pool.submit(
                            anti_shielded.batch, image_data, self.frame.settings.saving_settings.properties_tuple, uf
                        ), self._bulk_save_callback)
            else:   # 如果存在原始图像处理结果缓存则直接保存缓存
                match self.frame.controls.proc_mode:
                    case ProcModes.encryption_mode:
                        self.saving_thread_pool.submit(encrypt.save_image,
                            cache, image_item.path_data, self.frame.controls.saving_path, self.frame.controls.saving_format, self.frame.controls.saving_quality,
                            self.frame.controls.saving_subsampling_level,
                            image_item.settings.encryption_parameters_data(*image_item.cache.loaded_image.size).encryption_parameters_dict,
                            uf
                        ).add_done_callback(self._bulk_save_callback)
                    case ProcModes.decryption_mode:
                        self.saving_thread_pool.submit(decrypt.save_image,
                            cache, image_item.path_data, self.frame.controls.saving_path, self.frame.controls.saving_format, self.frame.controls.saving_quality,
                            self.frame.controls.saving_subsampling_level, uf
                        ).add_done_callback(self._bulk_save_callback)
                    case ProcModes.anti_shielded_mode:
                        self.saving_thread_pool.submit(anti_shielded.save_image,
                            cache, image_item.path_data, self.frame.controls.saving_path, self.frame.controls.saving_format, self.frame.controls.saving_quality,
                            self.frame.controls.saving_subsampling_level, uf
                        ).add_done_callback(self._bulk_save_callback)

            self.task_num += 1

        if not self.task_num:   # 对是否分配了任务进行检查
            self.frame.dialog.async_warning('没有添加任何批量(多进程)任务')
            self.hide_saving_progress_plane()
        else:
            self.bar.next_step(self.task_num)
            self.frame.dialog.async_info(f'已添加{self.task_num}个批量(多进程)任务')
            self.frame.savingProgressInfo.SetLabelText(f'0/{self.task_num} - 0%')
        self.lock.release()     # 任务分配完毕，释放线程锁

    def cancel(self):
        """取消所有未执行的批量保存任务"""
        self.frame.process_pool.cancel_task('bulk_save')

    def _check_dir(self, image_item: 'ImageItem'):
        """文件夹相关检查"""
        if not listdir(self.frame.controls.saving_path):     # 是否为空文件夹
            return DO_NOT_USE_FOLDER
        if image_item.path_data.relative_path:               # 是否有多级文件夹可使用
            match self.frame.dialog.confirmation_frame(
                    '{}所选的保存文件夹{}内有其他文件\n请选择处理方式'.format(image_item.path_data.file_name, self.frame.controls.saving_path),
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
                    '{}所选的保存文件夹{}内有其他文件\n请选择处理方式'.format(image_item.path_data.file_name, self.frame.controls.saving_path),
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
            self.frame.controls.saving_path = dialog.GetPath()
            return DO_NOT_USE_FOLDER

    def _bulk_save_callback(self, future, tag_name=None, result=(None, None)):
        """批量保存回调函数"""
        # TODO result疑似无法获取(疑似ProcessTaskManager.callback出现问题)
        with self.lock:     # 线程锁，防止进度累加错误
            data, error = result
            if error is not None:
                self.frame.dialog.async_error(data, '生成加密图像时出现意外错误')
            self.bar.add()
            self.frame.controls.saving_progress_info = f"{self.bar.value}/{self.task_num} - {format(self.bar.value / self.task_num * 100, '.2f')}%"
            if self.bar.value == self.task_num:
                self.frame.logger.info('完成了所有任务')
                self.hide_saving_progress_plane()

    def _gen_filter(self):
        """生成过滤器"""
        self.filter = Filter(
            (0 if self.frame.encryptionFilter.Value else None, 1 if self.frame.decryptionFilter.Value else None, 2 if self.frame.qqFilter.Value else None),
            id_dict[self.frame.passwordFilter.Get3StateValue()], id_dict[self.frame.shuffleFilter.Get3StateValue()],
            id_dict[self.frame.flipFilter.Get3StateValue()], id_dict[self.frame.mappingFilter.Get3StateValue()],
            id_dict[self.frame.XorFilter.Get3StateValue()]
        )

    def _check(self):
        """常规合法性检查"""
        if not isdir(self.frame.controls.saving_path):
            path = self.frame.dialog.select_dir('选择保存位置')
            if path is not None:
                self.frame.controls.saving_path = path
                return False
            self.frame.dialog.error('没有选择保存文件夹或选择的文件夹不存在', '保存时出现错误')
            return True
        elif self.progress_plane_displayed or self.frame.process_pool.check_tag('bulk_save'):
            self.frame.dialog.error('请先等待当前已有的保存任务完成', '无法执行保存操作')
            return True
        return False

    def show_saving_progress_plane(self, btn):
        if self.progress_plane_displayed:
            return
        self.progress_plane_displayed = True
        self.frame.controls.saving_progress = 0
        self.frame.controls.saving_progress_info = ''
        if btn:
            self.frame.stopSavingBtn.Enable()
            self.frame.stopSavingBtn.Show()
        else:
            self.frame.stopSavingBtn.Hide()
        self.frame.savingBtnPanel.Hide()
        self.frame.savingPrograssPanel.Show()
        self.frame.imageTreeCtrl.Disable()
        self.frame.savingFilters.Disable()
        self.frame.processingOptions.Disable()
        self.frame.savingOptions.Layout()

    def hide_saving_progress_plane(self):
        if not self.progress_plane_displayed:
            return
        self.progress_plane_displayed = False
        self.frame.savingPrograssPanel.Hide()
        self.frame.savingBtnPanel.Show()
        self.frame.imageTreeCtrl.Enable()
        self.frame.savingFilters.Enable()
        self.frame.processingOptions.Enable()
        self.frame.savingOptions.Layout()


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
