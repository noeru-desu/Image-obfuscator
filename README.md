# Image Obfuscator (由于时间原因，不再进行功能更新)

__`2.1.0`版本前称为*Image Encryptor*__

__这个工具是初中时期自学Python时的练习项目，当时也用来在群里开车(?)。现在由于空闲时间较少，所以不再对此工具进行功能更新__

<details>
<summary><h2>部分已实现的处理效果展示[点击展开/收起]</h2></summary>

> 所引用图像的画师: `かにビーム`

### 加密模式

__[保存为无损图像后解密保存的原图时，可无损还原出原图像]__

__[保存为有损图像或解密时使用非原图时，会出现较细的切割线]__

↓默认设置↓

<img style="max-width:100%;overflow:hidden;height:500px" src="https://github.com/noeru-desu/noeru-desu/blob/main/assets/Image-obfuscator/normal_encrypt.jpg?raw=true">

↓最高强度噪音异或RGB↓

<img style="max-width:100%;overflow:hidden;height:500px" src="https://github.com/noeru-desu/noeru-desu/blob/main/assets/Image-obfuscator/noise_xor_encrypt.jpg?raw=true">

---

### QQ反屏蔽模式(用于群聊中发送图像)

__[仅修改4个角的各1个像素点，使图像不会被特征匹配机制拦截]__

注意: 此模式完全**无法防举报**

<img style="max-width:100%;overflow:hidden;height:500px" src="https://github.com/noeru-desu/noeru-desu/blob/main/assets/Image-obfuscator/qq_antishield.jpg?raw=true">

---

### 幻影坦克模式 (使同一张图像显示在黑底与白底中时展现出不同的内容)

__[彩色模式就看个乐子，效果不好]__

<img style="max-width:100%;overflow:hidden;height:500px" src="https://github.com/noeru-desu/noeru-desu/blob/main/assets/Image-obfuscator/mirage_tank.jpg?raw=true">

---

### LSB(Least Significant Bit, 最低有效位)隐写模式

__[使用小于等于2个最低有效位时，可在肉眼无法辨别的情况下隐写任意文件到图像中]__

~(因为处理结果看起来完全没区别所以就不放图片了)~

---

</details>

## 下载

[Release版本](../../../releases)

[自动构建版本](../../../actions)

## 对旧版本加密的图像的兼容性

最多可解密 _0.1.0.rc_ 版加密的图像

## 已计划新增的模式

暂无

## 启动参数

请使用`-h`参数查看帮助

大部分启动参数都可以在程序内修改

## 运行源代码

Python版本：`3.11`

`requirements.txt`包含所有依赖库名称

CLI版本已停止更新

GUI版本入口为`ImageObfuscator.py`

向Python传入`-O`或`-OO`参数启动GUI版本时，将在参数本身的优化操作之外，禁用部分用于Debug的装饰器

## 从源代码构建可执行文件

可使用`Pyinstaller`或`Nuitka`将程序构建为可执行文件

## Github Actions 自动构建

Actions页面的CI中可下载自动构建的可执行文件压缩包

压缩包命名格式为：`适用系统`-`Python编译器`-`C编译器`-`MSVC版本`-build.`Github Actions运行ID`

# Thanks
### references:
* https://github.com/Aloxaf/MirageTankGo
* https://zhuanlan.zhihu.com/p/31164700
* https://github.com/ragibson/Steganography
