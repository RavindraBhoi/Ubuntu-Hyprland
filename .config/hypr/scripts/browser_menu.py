#!/usr/bin/env python3
"""
Material You Browser Dock Selector for Hyprland
Renders a premium floating dock popup with large crisp browser icons, hover states, and tooltips.
Supports arrow key navigation (Left/Right/Up/Down) + Enter + Escape.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import os
import sys
import subprocess
import shutil

import cairo

BROWSERS = [
    {"name": "Helium Browser", "exec": "helium", "icon": "helium"},
    {"name": "Zen Browser", "exec": "zen-browser", "icon": "zen-browser"},
    {"name": "Firefox", "exec": "firefox", "icon": "firefox"},
    {"name": "Google Chrome", "exec": "google-chrome-stable", "icon": "google-chrome"},
    {"name": "Brave Browser", "exec": "brave-browser", "icon": "brave-browser"},
    {"name": "Chromium", "exec": "chromium", "icon": "chromium"},
]

class BrowserDockWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="browser-menu-popup")
        
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_name("BrowserDockWindow")
        self.set_app_paintable(True)

        # Enable Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.connect("draw", self.on_draw)
        self.apply_css()

        # Layout Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        main_box.set_name("DockBox")
        self.add(main_box)

        # Populate available browsers
        self.buttons = []
        first_btn = None
        for b in BROWSERS:
            if shutil.which(b["exec"]):
                btn = self.create_browser_button(b)
                main_box.pack_start(btn, False, False, 0)
                self.buttons.append(btn)
                if first_btn is None:
                    first_btn = btn

        if not self.buttons:
            lbl = Gtk.Label(label="No supported browser found")
            lbl.set_name("ErrorLabel")
            main_box.pack_start(lbl, True, True, 0)

        self.connect("key-press-event", self.on_key_press)
        self.connect("focus-out-event", lambda w, e: Gtk.main_quit())

        if first_btn:
            GLib.idle_add(first_btn.grab_focus)

    def create_browser_button(self, browser):
        btn = Gtk.Button()
        btn.set_name("BrowserBtn")
        btn.set_tooltip_text(browser["name"])
        btn.set_relief(Gtk.ReliefStyle.NONE)
        btn.set_can_focus(True)

        icon_img = self.load_icon(browser["icon"])
        btn.set_image(icon_img)

        btn.connect("clicked", lambda w: self.launch_browser(browser["exec"]))
        return btn

    def load_icon(self, icon_name):
        icon_paths = [
            f"/usr/share/icons/hicolor/256x256/apps/{icon_name}.png",
            f"/usr/share/icons/hicolor/128x128/apps/{icon_name}.png",
            f"/usr/share/icons/hicolor/64x64/apps/{icon_name}.png",
            f"/home/ravindra/.local/share/icons/{icon_name}.png",
        ]

        for p in icon_paths:
            if os.path.exists(p):
                try:
                    pix = GdkPixbuf.Pixbuf.new_from_file_at_scale(p, 48, 48, True)
                    return Gtk.Image.new_from_pixbuf(pix)
                except Exception:
                    pass

        img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DND)
        img.set_pixel_size(48)
        return img

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        style_css = """
        @import url("/home/ravindra/.config/waybar/colors.css");

        #BrowserDockWindow {
            background-color: transparent;
            border: none;
            box-shadow: none;
        }

        #DockBox {
            background-color: alpha(@surface_container_highest, 0.90);
            border: 2px solid @primary;
            border-radius: 12px;
            padding: 14px 20px;
        }

        #BrowserBtn {
            background-color: alpha(@surface_variant, 0.4);
            border-radius: 48px;
            padding: 10px 14px;
            border: 1px solid transparent;
            transition: all 200ms ease-in-out;
        }

        #BrowserBtn:focus, #BrowserBtn:hover {
            background-color: alpha(@primary, 0.35);
            border: 2px solid @primary;
            outline: none;
        }

        #ErrorLabel {
            font-family: "JetBrains Mono", sans-serif;
            font-size: 14px;
            color: @on_surface;
            padding: 10px;
        }
        """
        css_provider.load_from_data(style_css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def launch_browser(self, exec_cmd):
        subprocess.Popen([exec_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        Gtk.main_quit()

    def on_key_press(self, widget, event):
        key = event.keyval
        if key == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        elif key in (Gdk.KEY_Right, Gdk.KEY_Down):
            self.move_focus_direction(1)
            return True
        elif key in (Gdk.KEY_Left, Gdk.KEY_Up):
            self.move_focus_direction(-1)
            return True
        elif key in (Gdk.KEY_Return, Gdk.KEY_KP_Enter, Gdk.KEY_space):
            current = self.get_focus()
            if current and isinstance(current, Gtk.Button):
                current.clicked()
                return True
        return False

    def move_focus_direction(self, step):
        if not self.buttons:
            return
        current = self.get_focus()
        idx = 0
        if current in self.buttons:
            idx = self.buttons.index(current)
            idx = (idx + step) % len(self.buttons)
        self.buttons[idx].grab_focus()

    def on_draw(self, widget, cr):
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        return False

def main():
    GLib.set_prgname("browser-menu-popup")
    win = BrowserDockWindow()
    win.show_all()
    win.present()
    Gtk.main()

if __name__ == "__main__":
    main()
