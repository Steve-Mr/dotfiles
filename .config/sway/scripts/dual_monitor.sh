#!/bin/bash

# pkill -f "/usr/bin/mons -a -x /home/maary/.config/i3/scripts/dual_monitor_manager.sh"
if ! pgrep -f "mons" > /dev/null; then
	mons -a -x "/home/maary/.config/i3/scripts/dual_monitor_manager.sh" &
fi    

