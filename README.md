# Image-encryptor

## 运行源代码

Python版本：`3.10`

`requirements.txt`包含所有依赖库名称

CLI版本为`Image_encryptor_cli.py`

GUI版本为`Image_encryptor_gui.py`

## 自动构建

Actions页面的CI中可下载自动构建的可执行文件包

>目前CI仅测试程序能否正常启动，没有测试各项功能是否可使用或是否存在Bug

packaged代表被打包为单文件版本

unpackaged代表没有被打包的版本

启动速度上，没有被打包的版本启动更快，Nuitka编译的版本比PyInstaller打包的版本更快

性能上，Nuitka编译的版本比PyInstaller打包的版本更好

但Nuitka编译的版本可能出现一些bug

## CLI版本的启动参数

Image_encryptor_cli.exe <文件/文件夹 路径> <保存路径> [附加参数]

<文件/文件夹 路径>必填，其余选填

<保存路径>仅可使用文件夹，默认为被加密文件的同级目录

附加参数如下：

`-e` 加密模式。

`-d` 解密模式。

`-t` 在批量加解密时不仅遍历表层文件夹，同时遍历所有文件夹内的文件夹，并在保存时自动创建不存在的子文件夹。

`--nne` 或 `--no-normal-encryption` 禁用所有常规加密，即禁用打乱翻转加密与RGB映射加密，该禁用选项优先于下方的`启用RGB随机映射`。

`--rm` 或 `--rgb-mapping` 启用RGB随机映射。

`-x <rgb/rgba>` 或 `--xor <rgb/rgba>` 异或加密rgb/rgba通道。

`--pw <password>`或`--password <password>` 设置密码。

`-r <row>`或`--row <row>` 设置分割行数，默认为25。提供`{width}` `{height}`，表示图片的宽高。

`-c <column>`或`--col <column>` 或`--column <column>` 设置分割列数，默认为25。提供`{width}` `{height}`，表示图片的宽高。

`-f <file format>`或`--format <file format>` 指定保存的文件格式，默认为png。

`--pc <process count>` 或 `--process-count <process count>` 指定用于异或加解密/批量加解密的进程池大小。提供`{cpu_count}`，表示cpu数量(每个cpu的核数之和)，默认为`{cpu_count}-2`，对于`{cpu_count}-2 < 1`的电脑，默认为1。

所有变量均为此格式：`{var}`，所有提供变量的参数均可使用Python运算符来使程序运算出结果。

***注意：指定文件保存格式为有损压缩格式(如jpg)时，RGB通道映射与异或加密会导致图片无法完全复原***

无需更改参数时，直接将文件拖放到exe上即可

如参数中不指明使用加密或解密模式，将在启动后进行选择

解密模式将忽略一部分启动参数，且保存格式默认为被解密图片的格式
