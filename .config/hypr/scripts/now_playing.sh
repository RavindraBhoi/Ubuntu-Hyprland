#!/bin/bash
STATUS=$(playerctl status 2>/dev/null)
if [ "$STATUS" = "Playing" ]; then
    ICON="▶"
elif [ "$STATUS" = "Paused" ]; then
    ICON="⏸"
else
    echo ""
    exit 0
fi

META=$(playerctl metadata --format '{{title}}' 2>/dev/null)
if [ ${#META} -gt 15 ]; then
    META="${META:0:12}..."
fi
echo "$ICON $META"
