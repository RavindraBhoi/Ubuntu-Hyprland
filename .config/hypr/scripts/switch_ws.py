#!/usr/bin/env python3
import subprocess
import sys
import os

if len(sys.argv) > 1:
    arg = sys.argv[1].strip()
    ws_num = arg.split()[0]
    cmd = f"workspace({ws_num})"
    subprocess.run(["hyprctl", "dispatch", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Signal waybar to refresh workspace status immediately
    subprocess.run(["pkill", "-RTMIN+8", "waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
