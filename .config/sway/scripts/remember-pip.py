#!/usr/bin/python

import i3ipc
import os
import json

def save_location(window):
    """
    Record the window's location and save it to .data/saved_locations.
    If the directory or file does not exist, create them.
    """
    # Ensure the .data directory exists
    data_dir = os.path.join(os.getcwd(), ".data")
    os.makedirs(data_dir, exist_ok=True)

    # File to save the locations
    file_path = os.path.join(data_dir, "saved_locations")

    # Read existing locations if the file exists
    locations = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                locations = json.load(file)
            except json.JSONDecodeError:
                pass

    # Update or add the location for the current window
    locations = {
        "x": window.rect.x,
        "y": window.rect.y,
        "width": window.rect.width,
        "height": window.rect.height,
    }

    # Save back to the file
    with open(file_path, "w") as file:
        json.dump(locations, file, indent=4)

def restore_location(window):
    """
    Restore the window's location based on saved data or move it to the bottom right.
    """

    # Ensure the .data directory and file path
    data_dir = os.path.join(os.getcwd(), ".data")
    file_path = os.path.join(data_dir, "saved_locations")

    if not os.path.exists(file_path):
        move_bottom_right(window)
        return

    # Load saved locations
    try:
        with open(file_path, "r") as file:
            location = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        move_bottom_right(window)
        return

    # Check if the window ID exists in the saved locations
    window.command(f"resize set width {location['width']}px height {location['height']}px")
    window.command(f"move absolute position {location['x']} {location['y']}")



def move_bottom_right(window):
    """Moves the given window to the bottom right corner of the screen."""

    i3 = i3ipc.Connection()
    outputs = i3.get_outputs()
    focused_output = next((o for o in outputs if o.focused), None)
    if not focused_output:
        raise RuntimeError("No focused output found.")

    # Calculate monitor dimensions considering scale
    monitor_width = int(focused_output.rect.width / focused_output.scale)
    monitor_height = int(focused_output.rect.height / focused_output.scale)

    # Get window dimensions
    win_width = window.rect.width
    win_height = window.rect.height
    deco_height = window.deco_rect.height  # Assuming this gives the decoration height

    # Calculate new position
    spacing_x = 5
    spacing_y = 35
    new_x = monitor_width - win_width - 2 * spacing_x
    new_y = monitor_height - win_height - deco_height - spacing_y

    # Move the window
    window.command(f"move position {new_x} {new_y}")

def main():
    # Create a connection to the i3/sway IPC
    ipc = i3ipc.Connection()

    # Dictionary to track the focus state of windows
    tracked_windows = {}

    def on_window_event(ipc, event):
        current_window = event.container

        # Check if the window meets the conditions
        if current_window.name == "Picture-in-Picture" and current_window.floating.startswith('user_on'):
            if event.change == "focus":
                restore_location(current_window)
                tracked_windows[current_window.id] = current_window


        focused_window = ipc.get_tree().find_focused()
        for window_id, window in list(tracked_windows.items()):
            if focused_window.id != window.id and window.focused:
                try:
                    tree = ipc.get_tree()
                    window = tree.find_by_id(window_id)
                    if window is not None and window.floating.startswith('user_on'):
                        save_location(window)
                    del tracked_windows[window_id]
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

    # Subscribe to window focus and window new events
    ipc.on("window::focus", on_window_event)

    # Start the main event loop
    ipc.main()

if __name__ == "__main__":
    main()