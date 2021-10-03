# Image-encryptor
对图片进行分块打乱、加密

***0.1.0-beta.4版本后的解密器向下兼容至0.1.0-rc.1版本加密的图片***

---

## 对于0.1.1版本

加密模式的启动参数：

Image_encryptor.exe <文件/文件夹 路径> <保存路径> [附加参数]

<文件/文件夹 路径>必填，其余选填

<保存路径>仅可使用文件夹，默认为被加密文件的同级目录

附加参数如下：

`-e` 加密模式

`-d` 解密模式

`-t` 在批量加解密时不仅遍历表层文件夹，同时遍历所有文件夹内的文件夹，并在保存时自动创建不存在的子文件夹

`--rm` 或 `--rgb-mapping` 启用RGB随机映射

`-x <rgb/rgba>` 或 `--xor <rgb/rgba>` 异或加密rgb/rgba通道

`--pw <password>`或`--password <password>` 设置密码

`-r <row>`或`--row <row>` 设置分割行数，默认为25

`-c <column>`或`--col <column>` 或`--column <column>` 设置分割列数，默认为25

`-f <file format>`或`--format <file format>` 指定保存的文件格式，默认为png

`--pc <process count>` 或 `--process-count <process count>` 指定用于异或加解密/批量加解密的进程池大小，可使用运算符。提供{cpu_count}，表示cpu数量(每个cpu的核数之和)。默认为{cpu_count}-2。对于{cpu_count}-2 < 1的电脑，默认为1。

***注意：指定文件保存格式为有损压缩格式(如jpg)时，警告RGB通道映射与异或加密***

无需更改参数时，直接将文件拖放到exe上即可

如参数中不指明使用加密或解密模式，将在启动后进行选择

解密模式将忽略一部分启动参数，且保存格式默认为被解密图片的格式

开发版的exe文件可在Actions页面的CI中下载(Pyinstaller构建的版本)
