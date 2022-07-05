#!/bin/bash

# 终端可能已经有在运行的实例
killall -q polybar

# 等待进程被终止
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

# 运行Polybar，使用默认的配置文件路径 ~/.config/polybar/config
for m in $(polybar --list-monitors | cut -d":" -f1); do
			MONITOR=$m polybar -q example &	
	done

echo "Polybar launched..."
