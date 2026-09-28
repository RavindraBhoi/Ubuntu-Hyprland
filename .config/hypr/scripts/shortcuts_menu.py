#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import math
import sys

SHORTCUTS = [
    ("SUPER + RETURN / T", "Open Terminal (Kitty)"),
    ("SUPER + SPACE", "App Launcher"),
    ("SUPER + B", "Web Browser Selector"),
    ("SUPER + E", "File Manager"),
    ("SUPER + F", "Search Files"),
    ("SUPER + A", "AI Chat Assistant"),
    ("SUPER + SHIFT + C", "Control Center"),
    ("SUPER + V", "Toggle Window Float"),
    ("SUPER + Q", "Close Window"),
    ("SUPER + SHIFT + P", "Restart Waybar & Wob Daemon"),
    ("SUPER + SHIFT + Q", "Logout / Power Menu"),
    ("SUPER + L", "Lock Screen"),
    ("SUPER + PRINT", "Take Screenshot"),
    ("SUPER + 1..9", "Switch Workspace"),
    ("SUPER + SHIFT + 1..9", "Move Window to Workspace"),
]

class ShortcutsMenuWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="shortcuts-popup")
        
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_name("ShortcutsMenuWindow")

        # Enable Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        # Apply CSS Styling
        self.apply_css()

        # Main Layout
        outer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        outer_box.set_name("OuterBox")
        self.add(outer_box)

        # Header Title
        header = Gtk.Label(label="⌨ Keyboard Shortcuts")
        header.set_name("HeaderTitle")
        header.set_halign(Gtk.Align.START)
        outer_box.pack_start(header, False, False, 0)

        # Main 2-column Grid
        grid = Gtk.Grid(column_spacing=24, row_spacing=12)
        grid.set_name("ShortcutsGrid")
        outer_box.pack_start(grid, True, True, 0)

        half = math.ceil(len(SHORTCUTS) / 2)
        left_col = SHORTCUTS[:half]
        right_col = SHORTCUTS[half:]

        # Left Column
        for row_idx, (keys, desc) in enumerate(left_col):
            key_lbl = Gtk.Label(label=keys)
            key_lbl.set_name("KeyLabel")
            key_lbl.set_halign(Gtk.Align.START)
            grid.attach(key_lbl, 0, row_idx, 1, 1)

            desc_lbl = Gtk.Label(label=desc)
            desc_lbl.set_name("DescLabel")
            desc_lbl.set_halign(Gtk.Align.START)
            grid.attach(desc_lbl, 1, row_idx, 1, 1)

        # Vertical Separator between columns
        sep = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        sep.set_name("ColSeparator")
        grid.attach(sep, 2, 0, 1, half)

        # Right Column
        for row_idx, (keys, desc) in enumerate(right_col):
            key_lbl = Gtk.Label(label=keys)
            key_lbl.set_name("KeyLabel")
            key_lbl.set_halign(Gtk.Align.START)
            grid.attach(key_lbl, 3, row_idx, 1, 1)

            desc_lbl = Gtk.Label(label=desc)
            desc_lbl.set_name("DescLabel")
            desc_lbl.set_halign(Gtk.Align.START)
            grid.attach(desc_lbl, 4, row_idx, 1, 1)

        # Keyboard & Window Events (close on Escape)
        self.connect("key-press-event", self.on_key_press)

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        style_css = """
        @import url("/home/ravindra/.config/waybar/colors.css");

        #ShortcutsMenuWindow {
            background-color: alpha(@surface, 0.94);
            border: 2px solid @primary;
            border-radius: 24px;
        }

        #OuterBox {
            padding: 24px 30px;
        }

        #HeaderTitle {
            font-family: "JetBrains Mono", sans-serif;
            font-size: 18px;
            font-weight: bold;
            color: @primary;
            margin-bottom: 4px;
        }

        #KeyLabel {
            font-family: "JetBrains Mono", sans-serif;
            font-size: 13px;
            font-weight: bold;
            color: @primary;
            background-color: alpha(@surface_variant, 0.6);
            border-radius: 8px;
            padding: 4px 10px;
        }

        #DescLabel {
            font-family: "JetBrains Mono", "Roboto", sans-serif;
            font-size: 13px;
            font-weight: 500;
            color: @on_surface;
        }

        #ColSeparator {
            margin-left: 10px;
            margin-right: 10px;
            opacity: 0.3;
            background-color: @outline;
        }
        """
        css_provider.load_from_data(style_css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.close_menu()
            return True
        return False

    def close_menu(self):
        Gtk.main_quit()

def main():
    win = ShortcutsMenuWindow()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
