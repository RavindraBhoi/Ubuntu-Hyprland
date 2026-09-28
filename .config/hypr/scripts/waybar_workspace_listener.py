#!/usr/bin/env python3
import os
import glob
import socket
import subprocess
import json
import time

CACHE_FILE = "/tmp/hypr_waybar_ws.json"

def get_socket_path():
    uid = os.getuid()
    matches = glob.glob(f'/run/user/{uid}/hypr/*/.socket2.sock')
    if matches:
        matches.sort(key=os.path.getmtime, reverse=True)
        return matches[0]
    return None

def update_ws_cache():
    try:
        active = json.loads(subprocess.check_output(["hyprctl", "activeworkspace", "-j"], text=True))
        active_id = active.get("id", 1)
        all_ws = json.loads(subprocess.check_output(["hyprctl", "workspaces", "-j"], text=True))
        
        occupied = set()
        for w in all_ws:
            w_id = w.get("id", 0)
            if w_id > 0 and (w.get("windows", 0) > 0 or w_id == active_id):
                occupied.add(w_id)
        occupied.add(active_id)
        
        ws_list = sorted(list(occupied))
        
        spans = []
        for w in ws_list:
            if w == active_id:
                spans.append(f"<span background='#d0bcff' foreground='#381e72' weight='bold'>  {w}  </span>")
            else:
                spans.append(f"  {w}  ")
                
        output_json = {
            "text": "".join(spans),
            "alt": str(active_id),
            "tooltip": f"Active Workspace: {active_id}"
        }
        
        with open(CACHE_FILE, "w") as f:
            json.dump(output_json, f)
            
        subprocess.run(["pkill", "-RTMIN+8", "waybar"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        pass

def main():
    while True:
        sock_path = get_socket_path()
        if not sock_path:
            time.sleep(2)
            continue
            
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(sock_path)
            
            # Initial update on connect
            update_ws_cache()
            
            buffer = ""
            while True:
                data = s.recv(4096).decode('utf-8', errors='ignore')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if any(line.startswith(ev) for ev in ["workspace>>", "workspacev2>>", "createworkspace>>", "destroyworkspace>>", "openwindow>>", "closewindow>>", "movewindow>>", "focusedmon>>"]):
                        update_ws_cache()
        except Exception as e:
            time.sleep(1)

if __name__ == "__main__":
    main()
