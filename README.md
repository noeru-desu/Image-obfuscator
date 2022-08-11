<!--
 * @Author       : noeru_desu
 * @Date         : 2021-11-21 19:21:41
 * @LastEditors  : noeru_desu
 * @LastEditTime : 2022-08-11 13:31:33
 * @Description  : README
-->
# Image Obfuscator

__`2.1.0`版本前称为*Image Encryptor*__

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

GUI版本为`ImageObfuscator.py`

向Python传入`-O`或`-OO`参数启动GUI版本时，将在参数本身的优化操作之外，禁用部分装饰器

## 从源代码构建可执行文件

可使用`Pyinstaller`或`Nuitka`将程序构建为可执行文件

## Github Actions 自动构建

Actions页面的CI中可下载自动构建的可执行文件压缩包

__只有发布时的构建才会禁用控制台并使用`-OO`参数来进行性能优化__

__目前CI仅测试程序能否正常启动，没有测试各项功能是否存在问题__

压缩包命名格式为：`适用系统`-`Python编译器`-`C编译器`-`MSVC版本`-build.`Github Actions运行ID`
