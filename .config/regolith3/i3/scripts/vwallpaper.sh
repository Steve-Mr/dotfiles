#!/usr/bin/env bash
#set video as wallpaper using xwinwrap and mpv - change path to your video!!

killall -9 xwinwrap
killall -9 mpv

# xwinwrap -g 1920x1080 -un -fdt -ni -b -ov -nf -- mpv -profile=wallpaper -wid WID -shuffle /home/maary/Videos/Hidamari

xwinwrap -g 1920x1080 -un -fdt -ni -b -ov -nf -- mpv -profile=wallpaper -wid WID /home/maary/Pictures/Wallpapers/44607aab956016c08fe4449861774a9804188fa7.webm
