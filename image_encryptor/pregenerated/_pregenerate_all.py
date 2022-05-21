"""
Author       : noeru_desu
Date         : 2022-05-20 16:02:29
LastEditors  : noeru_desu
LastEditTime : 2022-05-21 06:16:52
Description  : 自动加载_[文件名].py文件, 并调用其中gen_func以生成目标文件内容, 保存为[文件名].py, 替换其中"`"为"{", "~"为"}"
"""
from os import getcwd, walk
from os.path import splitext
from importlib import import_module


for top, dirs, files in walk(getcwd()):
    for fn in files:
        if fn == '_pregenerate_all.py':
            continue
        if not (fn.startswith('_') and fn.endswith('.py')):
            continue
        with open(fn.lstrip('_'), 'w', encoding='utf-8') as f:
            f.write(import_module(splitext(fn)[0]).gen_func().replace('`', '{').replace('~', '}'))
        print(f'{fn}已完成')
