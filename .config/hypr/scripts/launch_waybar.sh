#!/bin/bash
# Ensure hypr_socket_proxy is running
pgrep -f hypr_socket_proxy.py >/dev/null || python3 /home/ravindra/.config/hypr/scripts/hypr_socket_proxy.py &

# Resolve Hyprland signature and set up proxy socket directory
REAL_SOCK="$(ls /run/user/$(id -u)/hypr/*/.socket.sock 2>/dev/null | head -n1)"
if [ -n "$REAL_SOCK" ]; then
    REAL_SIG="$(basename $(dirname "$REAL_SOCK"))"
    PROXY_DIR="/run/user/$(id -u)/hypr_proxy/$REAL_SIG"
    mkdir -p "$PROXY_DIR"
    ln -sf /tmp/waybar_hypr.sock "$PROXY_DIR/.socket.sock"
    ln -sf "/run/user/$(id -u)/hypr/$REAL_SIG/.socket2.sock" "$PROXY_DIR/.socket2.sock"
    export HYPRLAND_INSTANCE_SIGNATURE="../hypr_proxy/$REAL_SIG"
fi

killall waybar 2>/dev/null
waybar &
