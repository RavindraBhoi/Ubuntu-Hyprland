#!/usr/bin/env python3
"""
Custom GTK OSD Indicator — Reads /tmp/wobpipe and renders a perfectly rounded pill volume & brightness bar using GTK3 & wallpaper colors.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
import sys
import threading

pipe_path = "/tmp/wobpipe"

class OSDWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="wob-osd-popup")
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_name("OSDWindow")
        self.set_default_size(280, 44)

        # Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        # Layout
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_name("OSDBox")
        self.add(box)

        # Icon Label
        self.icon_lbl = Gtk.Label(label="🔊")
        self.icon_lbl.set_name("OSDIcon")
        box.pack_start(self.icon_lbl, False, False, 0)

        # Level Bar / Scale
        self.progress = Gtk.LevelBar()
        self.progress.set_min_value(0)
        self.progress.set_max_value(100)
        self.progress.set_name("OSDProgress")
        box.pack_start(self.progress, True, True, 0)

        # Percentage Label
        self.val_lbl = Gtk.Label(label="0%")
        self.val_lbl.set_name("OSDVal")
        box.pack_start(self.val_lbl, False, False, 0)

        self.apply_css()
        self.hide_timer = None

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        style_css = """
        @import url("/home/ravindra/.config/waybar/colors.css");

        #OSDWindow {
            background-color: alpha(@surface, 0.95);
            border: 2px solid @primary;
            border-radius: 22px;
        }

        #OSDBox {
            padding: 8px 16px;
        }

        #OSDIcon {
            font-size: 16px;
            color: @primary;
        }

        #OSDProgress {
            min-height: 12px;
            border-radius: 10px;
        }

        #OSDProgress block.filled {
            background-color: @primary;
            border-radius: 10px;
        }

        #OSDProgress block.empty {
            background-color: alpha(@surface_variant, 0.6);
            border-radius: 10px;
        }

        #OSDVal {
            font-family: "JetBrains Mono", sans-serif;
            font-size: 13px;
            font-weight: bold;
            color: @on_surface;
            min-width: 38px;
        }
        """
        css_provider.load_from_data(style_css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def show_value(self, val):
        self.apply_css() # Reload colors
        self.progress.set_value(val)
        self.val_lbl.set_text(f"{val}%")
        
        self.show_all()
        self.present()

        if self.hide_timer:
            GLib.source_remove(self.hide_timer)
        self.hide_timer = GLib.timeout_add(1500, self.hide_window)

    def hide_window(self):
        self.hide()
        self.hide_timer = None
        return False

def listen_pipe(app):
    if not os.path.exists(pipe_path):
        try:
            os.mkfifo(pipe_path)
        except Exception:
            pass

    while True:
        try:
            with open(pipe_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.isdigit():
                        val = int(line)
                        GLib.idle_add(app.show_value, val)
        except Exception as e:
            pass

if __name__ == '__main__':
    GLib.set_prgname("wob-osd-popup")
    app = OSDWindow()

    # Position at bottom-center (40px margin)
    def on_size_allocate(win, allocation):
        display = Gdk.Display.get_default()
        monitor = display.get_monitor(0)
        geo = monitor.get_geometry()
        x = geo.x + (geo.width - allocation.width) // 2
        y = geo.y + geo.height - allocation.height - 50
        win.move(x, y)

    app.connect("size-allocate", on_size_allocate)

    t = threading.Thread(target=listen_pipe, args=(app,), daemon=True)
    t.start()

    Gtk.main()
