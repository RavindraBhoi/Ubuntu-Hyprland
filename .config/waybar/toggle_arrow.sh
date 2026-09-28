#!/bin/bash
STATE_FILE="/tmp/waybar_drawer_state"

if [ ! -f "$STATE_FILE" ]; then
    echo "closed" > "$STATE_FILE"
fi

STATE=$(cat "$STATE_FILE")

if [ "$1" == "toggle" ]; then
    if [ "$STATE" == "closed" ]; then
        echo "open" > "$STATE_FILE"
        sed -i 's/"modules-right": \["custom\/cliphist", "custom\/expand", "group\/hardware", "battery", "custom\/logout"\],/"modules-right": \["custom\/cliphist", "custom\/expand", "keyboard-state#numlock", "keyboard-state#capslock", "tray", "group\/hardware", "battery", "custom\/logout"\],/g' ~/.config/waybar/config
    else
        echo "closed" > "$STATE_FILE"
        sed -i 's/"modules-right": \["custom\/cliphist", "custom\/expand", "keyboard-state#numlock", "keyboard-state#capslock", "tray", "group\/hardware", "battery", "custom\/logout"\],/"modules-right": \["custom\/cliphist", "custom\/expand", "group\/hardware", "battery", "custom\/logout"\],/g' ~/.config/waybar/config
    fi
    killall -SIGUSR2 waybar
    exit 0
fi

# Use zero-width space (\u200b) to fix Waybar vertical alignment bug!
if [ "$STATE" == "closed" ]; then
    echo '{"text": "<\u200b"}'
else
    echo '{"text": ">\u200b"}'
fi
