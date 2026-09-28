#!/bin/bash
# Toggle popup calendar — ESC closes it
if pgrep -f "popup_calendar.py" > /dev/null; then
    pkill -f "popup_calendar.py"
else
    GDK_BACKEND=wayland python3 ~/.config/waybar/popup_calendar.py &
fi
