#!/bin/bash
BAT=$(upower -i /org/freedesktop/UPower/devices/battery_BAT1)
PERC=$(echo "$BAT" | grep "percentage:" | awk '{print $2}' | tr -d '%')
STATE=$(echo "$BAT" | grep "state:" | awk '{print $2}')

BAR_WIDTH=20
FILLED=$(($PERC * $BAR_WIDTH / 100))
EMPTY=$(($BAR_WIDTH - $FILLED))

BAR="["
for ((i=0; i<FILLED; i++)); do BAR="${BAR}■"; done
for ((i=0; i<EMPTY; i++)); do BAR="${BAR}□"; done
BAR="${BAR}]"

STATUS_ICON=""
if [ "$STATE" = "charging" ]; then
    STATUS_ICON=" ⚡"
elif [ "$STATE" = "fully-charged" ]; then
    STATUS_ICON=" 🔌"
fi

echo "$BAR ${PERC}%${STATUS_ICON}"
