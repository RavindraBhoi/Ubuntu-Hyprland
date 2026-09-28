#!/usr/bin/env python3
"""
Battery & Power Notification Daemon for Hyprland
Monitors power supply events and sends desktop notifications via notify-send:
- Low Battery Warning (20%)
- Critical Battery Level (10%)
- Fully Charged (100% / Fully-charged)
- Charger Connected / Disconnected
"""

import time
import os
import subprocess

warned_20 = False
warned_10 = False
warned_full = False
last_state = None

def get_battery_info():
    cap_path = "/sys/class/power_supply/BAT1/capacity"
    status_path = "/sys/class/power_supply/BAT1/status"
    ac_path = "/sys/class/power_supply/ACAD/online"

    if not os.path.exists(cap_path):
        cap_path = "/sys/class/power_supply/BAT0/capacity"
        status_path = "/sys/class/power_supply/BAT0/status"

    if not os.path.exists(ac_path):
        ac_path = "/sys/class/power_supply/AC/online"

    capacity = 100
    status = "Unknown"
    ac_online = 0

    try:
        with open(cap_path) as f:
            capacity = int(f.read().strip())
        with open(status_path) as f:
            status = f.read().strip()
    except Exception:
        pass

    try:
        with open(ac_path) as f:
            ac_online = int(f.read().strip())
    except Exception:
        pass

    return capacity, status, ac_online

def play_sound(sound_name):
    try:
        subprocess.Popen(["canberra-gtk-play", "-i", sound_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def send_notification(summary, body, icon="battery-good", urgency="normal"):
    try:
        subprocess.run([
            "notify-send",
            "-u", urgency,
            "-i", icon,
            summary,
            body
        ], check=False)
    except Exception:
        pass

def main():
    global warned_20, warned_10, warned_full, last_state

    capacity, status, ac_online = get_battery_info()
    last_state = ac_online

    while True:
        try:
            capacity, status, ac_online = get_battery_info()

            # State change: Charger Plugged / Unplugged
            if last_state is not None and ac_online != last_state:
                if ac_online == 1:
                    play_sound("power-plug")
                    send_notification(
                        "Charger Connected 🔌",
                        f"Power adapter plugged in ({capacity}%). Charging...",
                        icon="battery-charging",
                        urgency="normal"
                    )
                    warned_20 = False
                    warned_10 = False
                else:
                    play_sound("power-unplug")
                    send_notification(
                        "Charger Disconnected 🔋",
                        f"Running on battery power ({capacity}% remaining).",
                        icon="battery-standard",
                        urgency="normal"
                    )
                    warned_full = False

                last_state = ac_online

            # Discharging checks
            if ac_online == 0 or status == "Discharging":
                if capacity <= 10 and not warned_10:
                    send_notification(
                        "Critical Battery Level! ⚠️",
                        f"Battery is at {capacity}%. Plug in your charger immediately!",
                        icon="battery-caution",
                        urgency="critical"
                    )
                    warned_10 = True
                    warned_20 = True
                elif capacity <= 20 and not warned_20:
                    send_notification(
                        "Low Battery Warning 🪫",
                        f"Battery level dropped to {capacity}%. Consider plugging in your charger.",
                        icon="battery-low",
                        urgency="normal"
                    )
                    warned_20 = True

            # Full Charge check
            if (capacity >= 99 or status == "Full" or status == "Fully charged") and ac_online == 1:
                if not warned_full:
                    send_notification(
                        "Battery Fully Charged ⚡",
                        "Battery is at 100%. You can safely unplug your charger.",
                        icon="battery-full",
                        urgency="normal"
                    )
                    warned_full = True
            else:
                if capacity < 95:
                    warned_full = False

        except Exception:
            pass

        time.sleep(5)

if __name__ == '__main__':
    main()
