#!/bin/bash
if [ "$1" == "up" ]; then
    hyprctl dispatch "hl.dsp.focus({ workspace = 'e-1' })"
else
    hyprctl dispatch "hl.dsp.focus({ workspace = 'e+1' })"
fi
echo "$(date) scrolled $1" >> /tmp/scroll.log
