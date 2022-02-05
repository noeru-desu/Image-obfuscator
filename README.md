<!--
 * @Author       : noeru_desu
 * @Date         : 2021-11-21 19:21:41
 * @LastEditors  : noeru_desu
 * @LastEditTime : 2022-02-05 15:06:09
 * @Description  : 
-->
# Image-encryptor

## 运行源代码

Python版本：`3.10`

`requirements.txt`包含所有依赖库名称

CLI版本已停止支持

GUI版本为`ImageEncryptor.py`

## 从源代码构建可执行文件

使用Pyinstaller构建时没有注意事项。可参考的命令行：`pyinstaller -F ImageEncryptor.py`

使用Nuitka构建时请添加`--include-package=PIL`参数，否则Pillow库只能进行常见图片格式的编解码(当然如果不介意的话也不要紧)。可参考的命令行：`nuitka --python-flag=-OO --onefile --plugin-enable=anti-bloat,pkg-resources,numpy,multiprocessing,upx --noinclude-pytest-mode=nofollow --noinclude-setuptools-mode=nofollow --include-module=wx._xml --include-package=PIL ImageEncryptor.py`

## 自动构建

Actions页面的CI中可下载自动构建的可执行文件包

>目前CI仅测试程序能否正常启动，没有测试各项功能是否可使用或是否存在Bug

packaged代表被打包为单文件版本

unpackaged代表没有被打包的版本