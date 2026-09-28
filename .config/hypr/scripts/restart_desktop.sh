#!/bin/bash
hyprctl reload &
if pgrep -x "ashell" >/dev/null; then
    killall ashell 2>/dev/null || true
    sleep 0.2
    ashell & disown
elif pgrep -x "waybar" >/dev/null; then
    killall waybar 2>/dev/null || true
    sleep 0.2
    waybar & disown
else
    ashell & disown
fi
bash /home/ravindra/.config/hypr/scripts/wob.sh &
pkill -f notify_daemon.py 2>/dev/null || true
GDK_BACKEND=wayland python3 /home/ravindra/.config/hypr/scripts/notify_daemon.py &
sleep 1
notify-send -i dialog-information "Desktop Reloaded 🔄" "Hyprland config, Status Bar, Wob & Notifications restarted."
