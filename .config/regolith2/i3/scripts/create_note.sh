#!/bin/bash

# 设置保存笔记的目录
notes_dir=~/Documents/articles/note

# 创建以今日日期命名的 Markdown 文件
filename="$notes_dir/$(date +'%Y-%m-%d').md"

if [ ! -f "$filename" ]; then
    touch "$filename"
fi

# 使用 Ghostwriter 以 float 模式打开新建的文件
ghostwriter --platformtheme qt5ct "$filename"

