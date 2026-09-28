import time
import subprocess

frames = [
    "  ▂ ",
    " ▂▃ ",
    "▂▃▄▃",
    "▃▄▅▄",
    "▄▅▆▅",
    "▅▆▇▆",
    "▆▇██",
    "▇███",
    "████",
    "██▇▆",
    "▇▆▅▄",
    "▆▅▄▃",
    "▅▄▃▂",
    "▄▃▂ ",
    "▃▂  ",
    "▂   ",
]

print("Starting test...")
try:
    for i in range(50): # 50 iterations * 100ms = 5 seconds
        frame = frames[i % len(frames)]
        name = f"1 {frame}"
        # We escape the name for Lua command
        cmd = f'hyprctl dispatch \'hl.dsp.workspace.rename({{ workspace = 1, name = "{name}" }})\''
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.1)
finally:
    # Restore workspace 1
    print("Restoring workspace 1...")
    cmd = 'hyprctl dispatch \'hl.dsp.workspace.rename({ workspace = 1, name = "1" })\''
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Done.")
