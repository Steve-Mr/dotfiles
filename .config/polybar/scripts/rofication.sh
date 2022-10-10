#!/bin/bash

rofication_print() {
    status=$(/home/maary/.config/polybar/scripts/rofication-status)
    if [ $status = '?' ]; then
        printf $status
    elif [ $status -gt 0 ]; then
        printf " %s" "$status"
    else
        printf " 0"
    fi
    printf '\n'
}

rofication_show() {
    ilia -p notifications
}

case "$1" in
    --show)
        rofication_show
        ;;
    *)
        rofication_print
        ;;
esac
