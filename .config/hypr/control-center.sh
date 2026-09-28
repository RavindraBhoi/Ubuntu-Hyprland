#!/bin/bash
if pgrep -f "control_center_config" > /dev/null; then
    pkill -f "control_center_config"
    exit 0
fi

mkdir -p ~/Pictures/Screenshots

WIFI_STATE=$(rfkill list wifi | grep -i 'Soft blocked: yes')
if [ -n "$WIFI_STATE" ]; then
    WIFI="<span color='#888888'>   Wi-Fi (OFF)</span>"
else
    WIFI="<span color='#a8c7fa'>   Wi-Fi (ON)</span>"
fi

BT_STATE=$(rfkill list bluetooth | grep -i 'Soft blocked: yes')
if [ -n "$BT_STATE" ]; then
    BT="<span color='#888888'>   Bluetooth (OFF)</span>"
else
    BT="<span color='#a8c7fa'>   Bluetooth (ON)</span>"
fi

SCREENSHOT="   Screenshot"
POWER="⏻   Power"

CHOICE=$(echo -e "$WIFI\n$BT\n$SCREENSHOT\n$POWER" | wofi --allow-markup --dmenu --columns 2 --lines 2 --location=top_right --xoffset=-10 --yoffset=40 --style ~/.config/wofi/android16.css --conf ~/.config/wofi/control_center_config)

case "$CHOICE" in
    "$WIFI")
        if [ -n "$WIFI_STATE" ]; then
            rfkill unblock wifi
        else
            rfkill block wifi
        fi
        ;;
    "$BT")
        # Sub-menu for Bluetooth just like Android 16
        BT_CHOICE=$(echo -e "Toggle Power\nMore Options" | wofi --dmenu --columns 1 --lines 2 --location=top_right --xoffset=-10 --yoffset=40 --style ~/.config/wofi/android16.css --conf ~/.config/wofi/control_center_config)
        case "$BT_CHOICE" in
            "Toggle Power")
                if [ -n "$BT_STATE" ]; then
                    rfkill unblock bluetooth
                else
                    rfkill block bluetooth
                fi
                ;;
            "More Options")
                blueman-manager &
                ;;
        esac
        ;;
    "$SCREENSHOT")
        sleep 0.5
        grim -g "$(slurp)" ~/Pictures/Screenshots/Screenshot_$(date +'%Y-%m-%d_%H%M%S').png
        notify-send "Screenshot Saved"
        ;;
    "$POWER")
        wlogout --layout /home/ravindra/.config/wlogout/layout --css /home/ravindra/.config/wlogout/style.css -b 3
        ;;
esac
