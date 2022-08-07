"""
Author       : noeru_desu
Date         : 2022-07-02 10:44:58
LastEditors  : noeru_desu
LastEditTime : 2022-07-02 10:55:58
Description  : 
"""
from atexit import register
from zipfile import ZipFile


class ZipFileManager(object):
    def __init__(self, file: str) -> None:
        self.file_path = file
        self.closed = False
        self.zip_file = ZipFile(file)
        register(self.close_zip_file)

    def load_zip_info(self):
        self.zip_file.infolist()

    def close_zip_file(self):
        if self.closed:
            return
        self.closed = True
        self.zip_file.close()
