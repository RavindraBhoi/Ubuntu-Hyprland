import os
import subprocess
import sys

# Unicode block characters for audio visualization
blocks = [' ', '▂', '▃', '▄', '▅', '▆', '▇', '█']

cava_conf = os.path.expanduser("~/.config/cava/waybar.conf")
os.makedirs(os.path.dirname(cava_conf), exist_ok=True)

with open(cava_conf, "w") as f:
    f.write("""
[general]
bars = 35
framerate = 60
autosens = 1
lower_cutoff_freq = 50
higher_cutoff_freq = 10000

[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = 7
""")

# Run cava with unbuffered output
process = subprocess.Popen(['cava', '-p', cava_conf], stdout=subprocess.PIPE, text=True, bufsize=1)

try:
    for line in process.stdout:
        line = line.strip()
        if not line:
            continue
        values = line.split(';')[:-1]
        
        output = "".join(
            blocks[min(max(int(val), 0), 7)] if val.isdigit() else blocks[0]
            for val in values
        )
        
        print(output, flush=True)
except (KeyboardInterrupt, BrokenPipeError):
    pass
finally:
    if process:
        process.terminate()
