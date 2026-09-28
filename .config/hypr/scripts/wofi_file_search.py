#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import re

def get_file_icon(path, is_dir):
    if is_dir:
        return "📁"
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico']:
        return "🖼️"
    elif ext in ['.mp4', '.mkv', '.webm', '.avi', '.mov', '.flv']:
        return "🎬"
    elif ext in ['.mp3', '.flac', '.wav', '.m4a', '.ogg', '.opus']:
        return "🎵"
    elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md', '.csv']:
        return "📄"
    elif ext in ['.py', '.sh', '.json', '.lua', '.js', '.ts', '.html', '.css', '.c', '.cpp', '.h', '.conf']:
        return "💻"
    elif ext in ['.zip', '.tar', '.gz', '.7z', '.bz2', '.xz', '.rar']:
        return "📦"
    else:
        return "📄"

def main():
    home = os.path.expanduser("~")
    
    search_dirs = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Documents"),
        os.path.join(home, "Pictures")
    ]
    search_dirs = [d for d in search_dirs if os.path.isdir(d)]
    
    fd_cmd = shutil.which("fdfind") or shutil.which("fd")
    
    if fd_cmd:
        cmd = [fd_cmd, ".", "--type", "f", "--no-ignore-vcs"] + search_dirs + [
            "--exclude", ".git",
            "--exclude", ".cache",
            "--exclude", ".local",
            "--exclude", ".gemini",
            "--exclude", "node_modules",
            "--exclude", ".venv",
            "--exclude", "__pycache__",
            "--exclude", ".cargo"
        ]
        try:
            res = subprocess.check_output(cmd, text=True, errors="ignore")
            paths = res.strip().split("\n")
        except Exception:
            paths = []
    else:
        cmd = ["find"] + search_dirs + ["-type", "f", "-not", "-path", "*/.*"]
        try:
            res = subprocess.check_output(cmd, text=True, errors="ignore")
            paths = res.strip().split("\n")
        except Exception:
            paths = []

    if not paths or paths == [""]:
        return

    # Cap at top 40,000 files for fast loading
    paths = paths[:40000]

    lines = []
    path_map = {}
    
    for path in paths:
        if not path:
            continue
        is_dir = os.path.isdir(path)
        icon = get_file_icon(path, is_dir)
        basename = os.path.basename(path) or path
        relpath = path.replace(home, "~")
        
        formatted_line = f"{icon}  <b>{basename}</b>  <span color='#888888'>({relpath})</span>"
        lines.append(formatted_line)
        path_map[formatted_line] = path

    input_str = "\n".join(lines)

    wofi_cmd = [
        "wofi",
        "--dmenu",
        "--prompt", "Search Files...",
        "--allow-markup",
        "--insensitive",
        "--width", "850",
        "--height", "550",
        "--style", os.path.expanduser("~/.config/wofi/style.css")
    ]

    try:
        proc = subprocess.Popen(wofi_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        selected, _ = proc.communicate(input=input_str)
    except Exception:
        return

    if not selected:
        return

    selected = selected.strip()
    target_path = path_map.get(selected)
    
    if not target_path:
        m = re.search(r'\((~?.*?)\)', selected)
        if m:
            extracted = m.group(1)
            if extracted.startswith("~"):
                target_path = os.path.join(home, extracted[2:])
            elif extracted.startswith("/"):
                target_path = extracted

    if target_path and os.path.exists(target_path):
        subprocess.Popen(["xdg-open", target_path], start_new_session=True)

if __name__ == "__main__":
    main()
