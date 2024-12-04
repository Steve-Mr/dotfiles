#!/usr/bin/python

# This script requires i3ipc-python package (install it from a system package manager
# or pip).
# It makes inactive windows transparent. Use `transparency_val` variable to control
# transparency strength in range of 0…1 or use the command line argument -o.

import argparse
import signal
import sys
from functools import partial

import i3ipc

def should_ignore_window(window):
    """
    判断窗口是否需要跳过透明度设置：
    - 如果窗口是浮动窗口，跳过。
    """
    return window.floating == "user_on" or window.floating == "auto_on"


def should_force_full_opacity(window):
    """
    判断窗口是否需要强制设置为 100% 透明度：
    - 如果窗口名称匹配规则，强制设置为 100%。
    """
    if window.name and (
        "- YouTube" in window.name or
        "哔哩哔哩_bilibili" in window.name or
        "哔哩哔哩直播" in window.name or
        "哔哩哔哩" in window.name
    ):
        return True
    return False


def on_window_focus(args, ipc, event):
    global prev_focused
    global prev_workspace

    focused_workspace = ipc.get_tree().find_focused()

    if focused_workspace is None:
        return

    focused = event.container
    workspace = focused_workspace.workspace().num

    if focused.id != prev_focused.id:  # https://github.com/swaywm/sway/issues/2859
        if should_force_full_opacity(focused):
            focused.command("opacity 1.0")  # 强制设置为 100%
        elif not should_ignore_window(focused):
            focused.command("opacity " + args.focused)

        if workspace == prev_workspace and not should_ignore_window(prev_focused):
            if should_force_full_opacity(prev_focused):
                prev_focused.command("opacity 1.0")  # 强制设置为 100%
            else:
                prev_focused.command("opacity " + args.opacity)

        prev_focused = focused
        prev_workspace = workspace


def remove_opacity(ipc, focused_opacity):
    for workspace in ipc.get_tree().workspaces():
        for window in workspace:
            if should_force_full_opacity(window):
                window.command("opacity 1.0")  # 强制设置为 100%
            elif not should_ignore_window(window):
                window.command("opacity " + focused_opacity)
    ipc.main_quit()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script allows you to set the transparency of unfocused windows in sway."
    )
    parser.add_argument(
        "--opacity",
        "-o",
        type=str,
        default="0.80",
        help="set inactive opacity value in range 0...1",
    )
    parser.add_argument(
        "--focused",
        "-f",
        type=str,
        default="1.0",
        help="set focused opacity value in range 0...1",
    )
    args = parser.parse_args()

    ipc = i3ipc.Connection()
    prev_focused = None
    prev_workspace = ipc.get_tree().find_focused().workspace().num

    for window in ipc.get_tree():
        if window.focused:
            prev_focused = window
        else:
            # 跳过需要忽略的窗口
            if should_ignore_window(window):
                continue

            # 强制将符合规则的窗口设置为 100% 透明度
            if should_force_full_opacity(window):
                window.command("opacity 1.0")
            else:
                # 对非浮动且不匹配规则的窗口设置透明度
                window.command("opacity " + args.opacity)

    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, lambda signal, frame: remove_opacity(ipc, args.focused))
    ipc.on("window::focus", partial(on_window_focus, args))
    ipc.main()