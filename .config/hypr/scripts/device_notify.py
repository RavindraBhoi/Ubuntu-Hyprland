#!/usr/bin/env python3
"""
Peripheral & USB Device Notification & Sound Daemon for Hyprland
Monitors hardware device connection and disconnection events (USB drives, input devices, peripherals)
and plays sound effects + sends notifications.
"""

import subprocess
import time
import os

def play_sound(sound_name):
    try:
        subprocess.Popen(["canberra-gtk-play", "-i", sound_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def send_notification(summary, body, icon="drive-removable-media"):
    try:
        subprocess.run([
            "notify-send",
            "-i", icon,
            summary,
            body
        ], check=False)
    except Exception:
        pass

def get_usb_devices():
    devices = set()
    usb_dir = "/sys/bus/usb/devices"
    if os.path.exists(usb_dir):
        for item in os.listdir(usb_dir):
            product_path = os.path.join(usb_dir, item, "product")
            if os.path.exists(product_path):
                try:
                    with open(product_path) as f:
                        name = f.read().strip()
                        if name:
                            devices.add(f"{item}:{name}")
                except Exception:
                    pass
    return devices

def main():
    known_devices = get_usb_devices()
    
    while True:
        try:
            current_devices = get_usb_devices()
            
            # New devices added
            added = current_devices - known_devices
            for dev in added:
                dev_name = dev.split(":", 1)[1] if ":" in dev else "Device"
                play_sound("device-added")
                send_notification("Device Connected 🔌", f"{dev_name} has been connected.", icon="drive-removable-media")

            # Devices removed
            removed = known_devices - current_devices
            for dev in removed:
                dev_name = dev.split(":", 1)[1] if ":" in dev else "Device"
                play_sound("device-removed")
                send_notification("Device Removed 🔌", f"{dev_name} has been disconnected.", icon="drive-removable-media")

            known_devices = current_devices
        except Exception:
            pass

        time.sleep(2)

if __name__ == '__main__':
    main()
