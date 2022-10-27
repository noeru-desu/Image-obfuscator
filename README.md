# Image Obfuscator

__`2.1.0`版本前称为*Image Encryptor*__

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

> 核心实现参考:
[Aloxaf/MirageTankGo的核心实现](https://github.com/Aloxaf/MirageTankGo/blob/master/MTCore/MTCore.py)、
[幻影坦克架构指南(一)](https://zhuanlan.zhihu.com/p/31164700)、
[幻影坦克架构指南(三)](https://zhuanlan.zhihu.com/p/32532733)、
[棋盘格与幻影坦克](https://zhuanlan.zhihu.com/p/33148445)

<img style="max-width:100%;overflow:hidden;height:500px" src="https://github.com/noeru-desu/noeru-desu/blob/main/assets/Image-obfuscator/mirage_tank.jpg?raw=true">

---

__*未来将添加更多模式*__

</details>


## 网页版

已有计划...

## 下载

[Release版本](../../../releases)

[自动构建版本](../../../actions)

## 对旧版本加密的图像的兼容性

最多可解密 _0.1.0.rc_ 版加密的图像

## 已计划新增的模式

1. LSB(最低有效位)隐写模式 (俗称无影坦克)

*类似于 一个**非图像文件**中隐藏一张图像 的模式暂时没有计划添加*

## 启动参数

请使用`-h`参数查看帮助

大部分启动参数都可以在程序内修改

## 运行源代码

Python版本：`3.11`

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
