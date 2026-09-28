#!/usr/bin/env python3
import os
import sys
import glob
import socket
import select

def get_real_socket_path():
    uid = os.getuid()
    matches = glob.glob(f'/run/user/{uid}/hypr/*/.socket.sock')
    if matches:
        matches.sort(key=os.path.getmtime, reverse=True)
        return matches[0]
    return None

PROXY_SOCKET = "/tmp/waybar_hypr.sock"

def main():
    if os.path.exists(PROXY_SOCKET):
        try:
            os.remove(PROXY_SOCKET)
        except Exception:
            pass

    real_sock_path = get_real_socket_path()
    if not real_sock_path:
        print("Real Hyprland socket not found!", file=sys.stderr)
        sys.exit(1)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(PROXY_SOCKET)
    server.listen(10)

    while True:
        try:
            client_conn, _ = server.accept()
            try:
                real_sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                real_sock.connect(real_sock_path)
            except Exception:
                client_conn.close()
                continue

            sockets = [client_conn, real_sock]
            connected = True
            while connected:
                readable, _, _ = select.select(sockets, [], [], 10)
                if not readable:
                    break

                for s in readable:
                    data = s.recv(4096)
                    if not data:
                        connected = False
                        break

                    if s is client_conn:
                        cmd_str = data.decode('utf-8', errors='ignore')
                        if cmd_str.startswith("dispatch workspace "):
                            parts = cmd_str.strip().split(" ")
                            if len(parts) >= 3:
                                ws_arg = parts[2]
                                new_cmd = f"dispatch workspace '{ws_arg}'"
                                data = new_cmd.encode('utf-8')
                        real_sock.sendall(data)
                    else:
                        client_conn.sendall(data)

            client_conn.close()
            real_sock.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
