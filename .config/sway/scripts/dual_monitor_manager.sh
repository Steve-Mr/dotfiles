#!/usr/bin/env bash

# Set the directory where workspace_layout.txt will be stored
workspace_dir="$HOME/.config/i3/scripts/running_files"
workspace_file="$workspace_dir/workspace_layout.txt"

mkdir -p "$workspace_dir"

case ${MONS_NUMBER} in
    1)
	# Get workspace information
	workspaces=$(i3-msg -t get_workspaces)

	# Parse workspace information
	echo "$workspaces" | jq -r '.[] | "\(.name) \(.output)"' > "$workspace_file"

	# Output the result to a file
	cat "$workspace_file"
        mons -o
        sleep 1
        i3-msg restart
        ;;
    2)
        mons -e right --primary eDP
        sleep 1
        i3-msg restart
	# Read workspace layout from file
	while read -r line; do
	    # Split each line into workspace name and output
	    workspace=$(echo "$line" | awk '{print $1}')
	    output=$(echo "$line" | awk '{print $2}')
	    
	    # Move workspace to corresponding output
	    i3-msg "workspace $workspace; move workspace to output $output"
	done < "$workspace_file"
        ;;

esac
