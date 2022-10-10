#!/bin/bash              

DIR="$HOME/.config/polybar/polybar-themes/simple/material"                                                         

# Terminate already running bars                                                   
killall -q polybar                                                                 
                                                                                   
# Launch new polybar(s)                                                            
if type "xrandr"; then                                                             
    IFS=$'\n'  # must set internal field separator to avoid dumb                   
    for entry in $(xrandr --query | grep " connected"); do                         
        mon=$(cut -d" " -f1 <<< "$entry")                                          
        status=$(cut -d" " -f3 <<< "$entry")                                       
                                                                                   
        tray_pos=""                                                                
        if [ "$status" == "primary" ]; then                                        
            tray_pos="right"                                                       
        fi                                                                         
                                                                                   
        # MONITOR=$mon TRAY_POS=$tray_pos polybar -r example 2>&1 | tee -a /tmp/polybar-monitor-"$mon".log & disown                                                     
    MONITOR=$mon TRAY_POS=$tray_pos polybar -q main -c "$DIR"/config.ini 2>&1 | tee -a /tmp/polybar-monitor-"$mon".log & disown
    done                                                                           
    unset IFS  # avoid mega dumb by resetting the IFS                              
else                                                                               
    # polybar -r example 2>&1 | tee -a /tmp/polybar.log & disown
    polybar -q main -c "$DIR"/config.ini 2>&1 | tee -a /tmp/polybar.log & disown                      

fi                                                                                 
                                                                                   
echo "Polybar launched..."
