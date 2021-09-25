# Image-encryptor
对图片进行分块打乱

***已经可以使用，但仍在开发阶段。0.1.0-beta.4版本后的解密器向下兼容至0.1.0-rc.1版本加密的图片***

加密器(encryptor)的启动参数：

Image_encryptor.exe <文件路径> [附加参数]

<文件路径>必填，其余选填

附加参数如下：

`--rm` 或 `--rgb-mapping` 启用RGB随机映射

`-x <rgb/rgba>` 或 `--xor <rgb/rgba>` 异或加密rgb/rgba通道

`--pw <password>`或`--password <password>` 设置密码

`-r <row>`或`--row <row>` 设置分割行数，默认为25

`-c <column>`或`--col <column>` 或`--column <column>` 设置分割列数，默认为25

`-f <file format>`或`--format <file format>` 指定保存的文件格式，默认为png

`--pc <process count>` 或 `--process-count <process count>` 指定用于异或加密的进程池大小，可使用运算符。提供{cpu_count}，表示cpu数量(每个cpu的核数之和)。默认为{cpu_count}-2。对于{cpu_count}-2 < 1的电脑，默认为1。

***注意：指定文件格式为有损压缩格式(如jpg)时，禁用RGB通道映射与异或加密***

无需更改参数时，直接将文件拖放到exe上即可

解密器仅支持`-f`或`--format`，且默认为被解密图片的格式

开发版的exe文件可在Actions页面的CI中下载(Pyinstaller构建的版本)
