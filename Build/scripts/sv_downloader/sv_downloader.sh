#!/bin/bash

# 检查参数是否为空
if [ -z "$1" ]; then
  echo "请输入 StreetVoice 上的音频 ID！"
  exit 1
fi

if [ -z "$2" ]; then
  song_name=$1
else
  song_name=$2
fi

OUTPUT_MP3="$HOME/Music/nowhere/$song_name.mp3"

# 运行 java 命令获取 m3u8 链接
echo "正在获取 m3u8 链接..."
m3u8_link=$(java -jar 'StreetVoiceCrawler.jar' $1 | grep 'http.*m3u8')

# 下载音频文件并保存为 mp3 格式
echo "正在下载音频文件..."
ffmpeg -i "$m3u8_link" "$OUTPUT_MP3"
echo "下载完成！"

