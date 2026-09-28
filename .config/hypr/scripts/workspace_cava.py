import os
import subprocess
import sys
import json
import re
import time
import socket

# Prevent duplicate instances
try:
    # Using a local TCP socket as a lock
    lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lock_socket.bind(('127.0.0.1', 49280))
except socket.error:
    sys.exit(0)


INDICATOR = "󰎆"  # Nerd Font music note icon

def get_audio_playing_pids():
    try:
        out = subprocess.check_output(["pactl", "list", "sink-inputs"], text=True, stderr=subprocess.DEVNULL)
    except Exception:
        return []
    
    pids = []
    matches = re.findall(r'application\.process\.id\s*=\s*"(\d+)"', out)
    for m in matches:
        pids.append(int(m))
    return pids

def get_workspace_from_playerctl():
    try:
        status = subprocess.check_output(["playerctl", "status"], text=True, stderr=subprocess.DEVNULL).strip()
        if status != "Playing":
            return None
    except Exception:
        return None

    try:
        title = subprocess.check_output(["playerctl", "metadata", "--format", "{{title}}"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        title = ""

    try:
        clients_json = subprocess.check_output(["hyprctl", "clients", "-j"], text=True, stderr=subprocess.DEVNULL)
        clients = json.loads(clients_json)
    except Exception:
        return None

    if title:
        for client in clients:
            if title.lower() in client.get("title", "").lower():
                return client.get("workspace", {}).get("id")

    try:
        player_name = subprocess.check_output(["playerctl", "metadata", "--format", "{{playerName}}"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        player_name = ""

    if player_name:
        for client in clients:
            cls = client.get("class", "").lower()
            if player_name.lower() in cls or cls in player_name.lower():
                return client.get("workspace", {}).get("id")
                
    return None

def get_playing_workspace():
    pids = get_audio_playing_pids()
    if not pids:
        return get_workspace_from_playerctl()
        
    try:
        clients_json = subprocess.check_output(["hyprctl", "clients", "-j"], text=True, stderr=subprocess.DEVNULL)
        clients = json.loads(clients_json)
    except Exception:
        return get_workspace_from_playerctl()
        
    for client in clients:
        pid = client.get("pid")
        if pid in pids:
            return client.get("workspace", {}).get("id")
            
    return get_workspace_from_playerctl()

modified_workspaces = {}

try:
    while True:
        playing_ws = get_playing_workspace()
        
        if playing_ws is not None:
            ws_str = str(playing_ws)
            new_name = f"{ws_str} {INDICATOR}"
            
            # Update playing workspace if name changed
            if modified_workspaces.get(playing_ws) != new_name:
                cmd = f'hyprctl dispatch \'hl.dsp.workspace.rename({{ workspace = {playing_ws}, name = "{new_name}" }})\''
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                modified_workspaces[playing_ws] = new_name
            
            # Restore other workspaces
            to_restore = [ws for ws in modified_workspaces if ws != playing_ws]
            for ws in to_restore:
                cmd = f'hyprctl dispatch \'hl.dsp.workspace.rename({{ workspace = {ws}, name = "{ws}" }})\''
                subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                del modified_workspaces[ws]
        else:
            # Restore all if none playing
            if modified_workspaces:
                for ws in list(modified_workspaces.keys()):
                    cmd = f'hyprctl dispatch \'hl.dsp.workspace.rename({{ workspace = {ws}, name = "{ws}" }})\''
                    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                modified_workspaces.clear()
                
        time.sleep(0.5)

except KeyboardInterrupt:
    pass
finally:
    # Restore all workspaces on exit
    for ws in modified_workspaces:
        cmd = f'hyprctl dispatch \'hl.dsp.workspace.rename({{ workspace = {ws}, name = "{ws}" }})\''
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
