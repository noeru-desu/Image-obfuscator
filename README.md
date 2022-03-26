<!--
 * @Author       : noeru_desu
 * @Date         : 2021-11-21 19:21:41
 * @LastEditors  : noeru_desu
 * @LastEditTime : 2022-03-20 12:57:55
 * @Description  : README
-->
# Image-encryptor

## 下载

[Release版本](../../../releases)

[自动构建版本](../../../actions)

## 启动参数

低内存占用模式：`--low-memory`。开启后将不缓存未选中图像的缓存信息(如原图、预览图、已处理预览图等)，代价为更高的磁盘读取频率与CPU占用

目前没有对启动参数进行解析，不会对错误的启动参数进行提示

## 运行源代码

Python版本：`3.10`

`requirements.txt`包含所有依赖库名称

CLI版本已停止支持

GUI版本为`ImageEncryptor.py`

## 从源代码构建可执行文件

使用Pyinstaller构建时没有注意事项。

使用Nuitka构建时请添加`--include-package=PIL`参数，否则Pillow库只能进行常见图像格式的编解码(当然如果不介意的话也不要紧)。

## 自动构建

Actions页面的CI中可下载自动构建的可执行文件包

>目前CI仅测试程序能否正常启动，没有测试各项功能是否可使用或是否存在Bug

压缩包命名格式为：适用系统-Python编译器-C++编译器(-C++编译器版本)-build.Github Actions运行ID
