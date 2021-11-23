'''
Author       : noeru_desu
Date         : 2021-11-13 10:18:16
LastEditors  : noeru_desu
LastEditTime : 2021-11-23 21:11:17
Description  : 文件保存功能
'''
from os import listdir
from os.path import isdir
from typing import TYPE_CHECKING
from threading import Lock

from wx import ID_OK, ID_YES, ID_NO, DirDialog, DIRP_CHANGE_DIR, DIRP_DIR_MUST_EXIST, ID_CANCEL

import image_encryptor.gui.processor.qq_anti_harmony as qq_anti_harmony
import image_encryptor.gui.processor.decryptor as decryptor
import image_encryptor.gui.processor.encryptor as encryptor
from image_encryptor import EXTENSION_KEYS
from image_encryptor.gui.frame.utils import ProgressBar
from image_encryptor.gui.utils.thread import ThreadManager

if TYPE_CHECKING:
    from image_encryptor.gui.frame.main_frame import MainFrame
    from image_encryptor.gui.frame.tree_manager import ImageItem


class ImageSaver(object):
    """文件保存相关功能"""
    def __init__(self, frame: 'MainFrame'):
        self.frame = frame
        self.frame.process_pool.create_tag('bulk_save', False, False)   # 注册线程池标签
        self.saving_thread = ThreadManager('saving-thread')
        self.lock = Lock()
        self.progress_plane_displayed = False
        self.file_count = 0
        self.loading_progress = 0
        self.task_num = 0
        self.bar = None
        self.filter = None
        self.frame.program.logger.info('ImageSaver实例化完成')

    def save_selected_image(self):
        """保存选中的图片"""
        if self.frame.image_item is None:
            self.frame.error('没有选择图片')
            return
        if self._check():                       # 相关合法性检查
            return
        self.show_saving_progress_plane(False)
        if self.frame.update_password_dict():   # 检查密码栏内容是否合法
            self.frame.password.SetValue('none')
        if self.frame.mode.Selection == 0:
            self.saving_thread.start_new(encryptor.normal, self._save_selected_image_call_back, (self.frame, self.frame.saveProgressPrompt.SetLabelText, self.frame.saveProgress, self.frame.image_item.loaded_image, True))
        elif self.frame.mode.Selection == 1:
            self.saving_thread.start_new(decryptor.normal, self._save_selected_image_call_back, (self.frame, self.frame.saveProgressPrompt.SetLabelText, self.frame.saveProgress, self.frame.image_item.loaded_image, True))
        else:
            self.saving_thread.start_new(qq_anti_harmony.normal, self._save_selected_image_call_back, (self.frame, self.frame.saveProgressPrompt.SetLabelText, self.frame.saveProgress, self.frame.image_item.loaded_image, True))

    def _save_selected_image_call_back(self, error, image):
        """保存选中的图片完成后的回调函数"""
        self.hide_saving_progress_plane()
        if error is not None:
            self.frame.error(repr(error), '生成加密图片时出现意外错误')
            return
        self.frame.show_processing_preview(True, image)     # 顺便刷新一下预览图

    def bulk_save(self):
        """批量保存"""
        if not self.frame.tree_manager.file_dict:
            self.frame.error('没有载入图片')
            return
        if self._check():                               # 相关合法性检查
            return
        self.show_saving_progress_plane(True)
        if self.frame.imageTreeCtrl.Selection.IsOk():   # 检查是否选择了某一文件
            image_data = self.frame.imageTreeCtrl.GetItemData(self.frame.imageTreeCtrl.Selection)
            if image_data is not None:                  # 是否选择的是文件夹，如果不是，则同步gui内容至对应image_item实例
                image_data.settings = self.frame.settings
        else:
            self.frame.apply_settings_to_all(None)      # 如果没有选择任何文件，则将当前gui内容同步到所有image_item实例

        frame_id = self.frame.confirmation_frame('是否创建与文件树层级相同的文件夹进行文件保存', cancel='取消保存操作')
        if frame_id == ID_YES:
            use_folder = True
        elif frame_id == ID_NO:
            use_folder = False
        else:
            self.hide_saving_progress_plane()
            return

        self._generate_filter()
        self.bar = ProgressBar(self.frame.saveProgress)
        self.task_num = 0
        self.lock.acquire()                                 # 锁住线程锁，防止在任务添加期间执行回调函数，而导致进度识别错误

        for item_id in self.frame.tree_manager.file_dict.values():
            image_item: 'ImageItem' = self.frame.imageTreeCtrl.GetItemData(item_id)
            if image_item.encrypted_image and not image_item.manual_switch_mode:
                image_item.settings['mode'] = 1             # 检测是否为没有被手动更改过模式的可解密图片

            if self._filter_task(image_item.settings):      # 进行设置过滤
                continue
            uf = False                                      # use_folder的局部变量名
            if not use_folder:                              # 对未使用多级文件夹的情况的一些询问
                result = self._check_dir(image_item)
                if result == 2:
                    pass
                elif result == 3:
                    uf = True
                else:
                    continue
            else:
                uf = True

            image_data = ('RGBA', image_item.loaded_image.size, image_item.loaded_image.tobytes())  # 打包所需的可封存的对象
            saving_format = EXTENSION_KEYS[image_item.settings['saving_format']]

            if image_item.settings['mode'] == 0:
                self.frame.process_pool.add_task('bulk_save', self.frame.process_pool.submit(encryptor.batch, image_data, image_item.path_data, image_item.settings, saving_format, uf), self._bulk_save_callback)
            elif image_item.settings['mode'] == 1:
                image_item.encryption_data['password'] = self.frame.program.password_dict.get(image_item.encryption_data['password_base64'], None)
                if image_item.encryption_data['password'] is None:
                    self.frame.program.logger.warning(f'[{image_item.path_data[-1]}]未找到密码，跳过保存')
                    continue
                self.frame.process_pool.add_task('bulk_save', self.frame.process_pool.submit(decryptor.batch, image_data, image_item.path_data, image_item.settings, image_item.encryption_data, saving_format, uf), self._bulk_save_callback)
            else:
                self.frame.process_pool.add_task('bulk_save', self.frame.process_pool.submit(qq_anti_harmony.batch, image_data, image_item.settings, saving_format, uf), self._bulk_save_callback)

            self.task_num += 1

        self.lock.release()     # 任务分配完毕，释放线程锁
        if not self.task_num:   # 对是否分配了任务进行检查
            self.frame.warning('没有添加任何批量(多进程)任务')
            self.hide_saving_progress_plane()
        else:
            self.bar.next_step(self.task_num)
            self.frame.info(f'已添加{self.task_num}个批量(多进程)任务')
            self.frame.saveProgressPrompt.SetLabelText(f'0/{self.task_num} - 0%')

    def cancel(self):
        """取消所有未执行的批量保存任务"""
        self.frame.process_pool.cancel_task('bulk_save')

    def _check_dir(self, image_item: 'ImageItem'):
        """文件夹相关检查"""
        if not listdir(image_item.settings['saving_path']):     # 是否为空文件夹
            return 2
        if image_item.path_data[1]:                             # 是否有多级文件夹可使用
            frame_id = self.frame.confirmation_frame(f'{image_item.path_data[-1]}所选的保存文件夹{image_item.settings["saving_path"]}内有其他文件' + '\n' + '请选择处理方式', yes='仍然保存', no='选择新的文件夹进行保存', cancel='创建文件树同级文件夹保存', help='跳过保存该文件')
            if frame_id == ID_YES:
                return 2
            elif frame_id == ID_NO:
                path = self._select_dir(image_item.path_data[0])
                if path is None:
                    return
                else:
                    image_item.settings['saving_path'] = path
                    return 2
            elif frame_id == ID_CANCEL:
                return 3
            else:
                return
        else:
            frame_id = self.frame.confirmation_frame(f'{image_item.path_data[-1]}所选的保存文件夹{image_item.settings["saving_path"]}内有其他文件' + '\n' + '请选择处理方式', yes='仍然保存', no='选择新的文件夹进行保存', cancel='跳过保存该文件')
            if frame_id == ID_YES:
                return 2
            elif frame_id == ID_NO:
                path = self._select_dir(image_item.path_data[0])
                if path is None:
                    return
                else:
                    image_item.settings['saving_path'] = path
                    return 2
            else:
                return

    def _select_dir(self, defaultPath):
        """选择文件夹"""
        dialog = DirDialog(self, "选择文件夹", defaultPath, DIRP_CHANGE_DIR | DIRP_DIR_MUST_EXIST)
        if ID_OK == dialog.ShowModal():
            return dialog.GetPath()

    def _bulk_save_callback(self, future, tag_name):
        """批量保存回调函数"""
        with self.lock:     # 线程锁，防止进度累加错误
            self.bar.add()
            self.frame.saveProgressPrompt.SetLabelText(f"{self.bar.value}/{self.task_num} - {format(self.bar.value / self.task_num * 100, '.2f')}%")
            if self.bar.value == self.task_num:
                self.frame.program.logger.info('完成了所有任务')
                self.hide_saving_progress_plane()

    def _generate_filter(self):
        """生成过滤器"""
        password_filter = self.frame.passwordFilter.Selection
        shuffle_filter = self.frame.shuffleFilter.Selection
        flip_filter = self.frame.flipFilter.Selection
        mapping_filter = self.frame.mappingFilter.Selection
        self.filter = (
            (0 if self.frame.encryptionFilter.IsChecked() else None, 1 if self.frame.decryptionFilter.IsChecked() else None, 2 if self.frame.qqFilter.IsChecked() else None),
            None if password_filter == 2 else password_filter,
            None if shuffle_filter == 2 else shuffle_filter,
            None if flip_filter == 2 else flip_filter,
            None if mapping_filter == 2 else mapping_filter
        )

    def _check(self):
        """常规合法性检查"""
        if not isdir(self.frame.selectSavePath.Path):
            self.frame.error('没有选择保存文件夹或选择的文件夹不存在', '保存时出现错误')
            return True
        elif self.saving_thread.is_running or self.frame.process_pool.check_tag('bulk_save'):
            self.frame.error('请先等待当前已有的保存任务完成', '无法执行保存操作')
            return True
        return False

    def _filter_task(self, settings):
        """根据过滤器过滤image_item"""
        if not settings['saving_path']:
            return True
        if settings['mode'] not in self.filter[0]:
            return True
        if self.filter[1] is not None and (settings['password'] == 'none') is self.filter[1]:
            return True
        if self.filter[2] is not None and settings['shuffle'] is not self.filter[2]:
            return True
        if self.filter[3] is not None and settings['flip'] is not self.filter[3]:
            return True
        if self.filter[4] is not None and settings['mapping'] is not self.filter[4]:
            return True
        return False

    def show_saving_progress_plane(self, btn):
        if self.progress_plane_displayed:
            return
        self.progress_plane_displayed = True
        self.frame.saveProgress.SetValue(0)
        self.frame.saveProgressPrompt.SetLabelText('')
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
