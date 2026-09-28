#!/usr/bin/env python3
import json
import subprocess
import sys

def main():
    ws_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    try:
        active = json.loads(subprocess.check_output(["hyprctl", "activeworkspace", "-j"], text=True))
        active_id = active.get("id", 1)
        all_ws = json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"], text=True))
        
        # Only show workspaces that are active or contain open windows
        occupied_ids = set()
        for w in all_ws:
            w_id = w.get("id", 0)
            if w_id > 0 and (w.get("windows", 0) > 0 or w_id == active_id):
                occupied_ids.add(w_id)
        occupied_ids.add(active_id)
    except Exception:
        active_id = 1
        occupied_ids = {1}

    is_active = (active_id == ws_num)
    
    if ws_num in occupied_ids:
        data = {
            "text": str(ws_num),
            "class": "active" if is_active else "inactive"
        }
    else:
        data = {
            "text": "",
            "class": "hidden"
        }
        
    print(json.dumps(data))

if __name__ == "__main__":
    main()
