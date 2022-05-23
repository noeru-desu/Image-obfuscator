<!--
 * @Author       : noeru_desu
 * @Date         : 2021-11-21 19:21:41
 * @LastEditors  : noeru_desu
 * @LastEditTime : 2022-05-23 21:41:02
 * @Description  : README
-->
# Image Encryptor

## 新版本

此分支([dev/1.x](../../../tree/dev/1.x))不再添加新功能，仅进行必要的Bug修复

当前正在`v2.x`分支([dev/2.x](../../../tree/dev/2.x))进行一些重构工作，完成后将添加更多功能

## 下载

[Release版本](../../../releases)

[自动构建版本](../../../actions)

## 启动参数

请使用`-h`参数查看帮助

大部分启动参数都可以在程序内修改

## 运行源代码

Python版本：`3.10`

`requirements.txt`包含所有依赖库名称

CLI版本已停止支持 (2.x版本中可能被重新添加)

GUI版本为`ImageEncryptor.py`

向Python传入`-O`或`-OO`参数启动GUI版本时，将在参数本身的优化操作之外，禁用部分装饰器

## 从源代码构建可执行文件

使用Pyinstaller构建时没有注意事项。

使用Nuitka构建时请添加`--include-package=PIL`参数，否则Pillow库只能进行常见图像格式的编解码(当然如果不介意的话也不要紧)。

## Github Actions 自动构建

Actions页面的CI中可下载自动构建的可执行文件包

只有发布时的构建才会使用`-OO`参数来优化字节码和禁用部分装饰器

>目前CI仅测试程序能否正常启动，没有测试各项功能是否存在问题

压缩包命名格式为：`适用系统`-`Python编译器`-`C编译器`-`MSVC版本`-build.`Github Actions运行ID`
