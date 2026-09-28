#!/usr/bin/env python3
"""Minimal popup calendar with bottom month navigator — closes ONLY with ESC. Shows Indian holidays."""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib
import subprocess, os, sys
from datetime import date

# Kill existing instance (toggle behavior)
pid_file = "/tmp/popup_calendar.pid"
if os.path.exists(pid_file):
    with open(pid_file) as f:
        old_pid = f.read().strip()
    try:
        subprocess.run(["kill", old_pid], check=True)
        os.remove(pid_file)
        sys.exit(0)
    except Exception:
        os.remove(pid_file)

# Write PID
with open(pid_file, "w") as f:
    f.write(str(os.getpid()))

MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

# Indian public holidays (month, day): name
INDIAN_HOLIDAYS = {
    (1,  26): "Republic Day",
    (3,  14): "Holi",
    (4,  14): "Ambedkar Jayanti",
    (4,  18): "Good Friday",
    (5,  1):  "Labour Day",
    (6,  2):  "Telangana Formation Day",
    (8,  15): "Independence Day",
    (9,  16): "Eid al-Adha",
    (10, 2):  "Gandhi Jayanti",
    (10, 24): "Dussehra",
    (11, 1):  "Diwali",
    (11, 5):  "Diwali (Bhai Dooj)",
    (11, 15): "Guru Nanak Jayanti",
    (12, 25): "Christmas",
}

win = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
win.set_title("Calendar")
win.set_decorated(False)
win.set_resizable(False)
win.set_skip_taskbar_hint(True)
win.set_skip_pager_hint(True)
win.set_keep_above(True)
win.set_type_hint(Gdk.WindowTypeHint.UTILITY)
win.set_size_request(400, 320)

# CSS
css = b"""
window {
    background: rgba(20, 16, 26, 0.98);
    border: 2px solid rgba(200,150,255,0.35);
    border-radius: 20px;
    padding: 16px;
}
calendar {
    background: transparent;
    color: #f0e8f8;
    font-size: 20px;
}
calendar:selected {
    background: rgba(180, 90, 220, 0.75);
    border-radius: 10px;
    color: #ffffff;
}
calendar.highlight {
    color: #ff8080;
    font-weight: bold;
}
#nav-box {
    margin-top: 4px;
}
#nav-label {
    color: #d0a0f0;
    font-weight: bold;
    font-size: 20px;
}
.nav-btn {
    background: rgba(180, 90, 220, 0.30);
    color: #ffffff;
    border-radius: 10px;
    border: none;
    font-size: 18px;
    padding: 4px 14px;
}
.nav-btn:hover {
    background: rgba(180, 90, 220, 0.65);
}
#holiday-label {
    color: #ff9090;
    font-size: 15px;
    font-weight: bold;
    padding: 8px 4px 2px 4px;
}
"""
provider = Gtk.CssProvider()
provider.load_from_data(css)
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
win.add(vbox)

# GTK Calendar (Date Grid Only - Heading Disabled)
cal = Gtk.Calendar()
cal.set_property("show-heading", False)
cal.set_property("show-day-names", True)
cal.set_property("show-week-numbers", False)

# Mark Indian holidays for current month
def mark_holidays(calendar):
    calendar.clear_marks()
    year, month, _ = calendar.get_date()
    month += 1  # GTK months are 0-indexed
    for (m, d), name in INDIAN_HOLIDAYS.items():
        if m == month:
            try:
                calendar.mark_day(d)
            except Exception:
                pass

# Bottom Month Navigator Controls
nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
nav_box.set_name("nav-box")

prev_btn = Gtk.Button(label="◀")
prev_btn.get_style_context().add_class("nav-btn")

nav_label = Gtk.Label()
nav_label.set_name("nav-label")

next_btn = Gtk.Button(label="▶")
next_btn.get_style_context().add_class("nav-btn")

nav_box.pack_start(prev_btn, False, False, 0)
nav_box.pack_start(nav_label, True, True, 0)
nav_box.pack_start(next_btn, False, False, 0)

# Holiday label below calendar
holiday_label = Gtk.Label(label="")
holiday_label.set_name("holiday-label")
holiday_label.set_xalign(0.5)
holiday_label.set_line_wrap(True)
holiday_label.set_max_width_chars(30)

def update_nav_label(calendar):
    year, month, day = calendar.get_date()
    nav_label.set_text(f"{MONTH_NAMES[month]} {year}")
    holiday = INDIAN_HOLIDAYS.get((month + 1, day))
    if holiday:
        holiday_label.set_text(f"🎉 {holiday}")
    else:
        holiday_label.set_text("")

def on_prev_clicked(btn):
    year, month, _ = cal.get_date()
    if month == 0:
        year -= 1
        month = 11
    else:
        month -= 1
    cal.select_month(month, year)

def on_next_clicked(btn):
    year, month, _ = cal.get_date()
    if month == 11:
        year += 1
        month = 0
    else:
        month += 1
    cal.select_month(month, year)

prev_btn.connect("clicked", on_prev_clicked)
next_btn.connect("clicked", on_next_clicked)

def on_day_selected(calendar):
    update_nav_label(calendar)

def on_month_changed(calendar):
    mark_holidays(calendar)
    update_nav_label(calendar)

cal.connect("day-selected", on_day_selected)
cal.connect("month-changed", on_month_changed)

mark_holidays(cal)
update_nav_label(cal)

# Layout: Grid at top -> Navigator & Holiday directly underneath
vbox.pack_start(cal, False, False, 0)
vbox.pack_start(nav_box, False, False, 0)
vbox.pack_start(holiday_label, False, False, 0)

def close(w=None, *a):
    if os.path.exists(pid_file):
        os.remove(pid_file)
    Gtk.main_quit()

# ONLY close on ESC — no focus-out close
def on_key(w, event):
    if event.keyval == Gdk.KEY_Escape:
        close()

win.connect("destroy", close)
win.connect("key-press-event", on_key)

# Position near bottom-right (near Waybar clock)
display = Gdk.Display.get_default()
monitor = display.get_monitor(0)
geo = monitor.get_geometry()
sw = geo.x + geo.width
sh = geo.y + geo.height
win.show_all()
GLib.idle_add(lambda: win.move(sw - win.get_size()[0] - 20, sh - win.get_size()[1] - 50) or False)
win.present()

Gtk.main()
