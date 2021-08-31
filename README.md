# Image-encryptor
对图片进行分块打乱

***已经可以使用，但仍在开发阶段。新Beta版本的解密器不会兼容旧Beta版本加密的图片***

加密器(encryptor)的启动参数：

Image_encryptor.exe <文件路径> [附加参数]

<文件路径>必填，其余选填

附加参数如下：

`--nm`或`--not_mapping` 关闭RGB通道映射

`--pw <password>`或`--password <password>` 设置密码

`-r <row>`或`--row <row>` 设置分割行数

`-c <column>`或`--col <column>` 或`--column <column>` 设置分割列数默认为25

`-f <file_format>`或`--format <file_format>` 指定保存的文件格式，默认为png

***注意：指定文件格式为有损压缩格式(如jpg)时，自动禁用RGB通道映射***

无需更改参数时，直接将文件拖放到exe上即可

BETA版与开发版的exe文件可在Actions页面的CI中下载
