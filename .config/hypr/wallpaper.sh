#!/bin/bash
if ! pgrep -x "swww-daemon" > /dev/null; then
    swww-daemon &
    sleep 1
fi

DIR="/home/ravindra/Pictures/Wallpapers/Garuda"

WALLPAPER=$(find "$DIR" -type f \( -iname \*.jpg -o -iname \*.png -o -iname \*.jpeg \) | shuf -n 1)
if [ -n "$WALLPAPER" ]; then
    swww img "$WALLPAPER" --transition-type grow --transition-pos 0.5,0.5 --transition-duration 2
    ln -sf "$WALLPAPER" ~/.cache/current_wallpaper.jpg
    ~/.cargo/bin/matugen image "$WALLPAPER" --source-color-index 0
    bash /home/ravindra/.config/hypr/scripts/wob.sh &
    killall -USR1 kitty
    hyprctl reload
    if pgrep -x "ashell" > /dev/null; then
        # ashell auto-reloads via config watch
        :
    elif pgrep -x "waybar" > /dev/null; then
        killall waybar
        waybar & disown
    fi
fi
