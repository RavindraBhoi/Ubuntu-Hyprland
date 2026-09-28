#!/bin/bash
mkdir -p ~/Pictures/Screenshots
FILE=~/Pictures/Screenshots/Screenshot_$(date +%Y-%m-%d_%H%M%S).png

# Capture selected region with slurp and grim
GEOM=$(slurp)
if [ -z "$GEOM" ]; then
    exit 0
fi

grim -g "$GEOM" "$FILE"
if [ ! -f "$FILE" ]; then
    exit 0
fi

# Copy image to clipboard
wl-copy < "$FILE"

# Send notification with clickable action to open image viewer
ACTION=$(notify-send -i "$FILE" -a "Screenshot" --action="open=Open Image" "Screenshot Saved 📸" "Saved to Screenshots & Clipboard.\nClick to view image.")

if [ "$ACTION" = "open" ] || [ "$ACTION" = "default" ] || [ -n "$ACTION" ]; then
    xdg-open "$FILE" &
fi
