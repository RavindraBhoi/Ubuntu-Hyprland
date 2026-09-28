#!/usr/bin/env python3
"""
DankMaterialShell-style Control Center Popup
Matches exact UI layout from menu.png (Header Profile + Action Buttons, Sliders, Large Toggle Cards)
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import subprocess
import os
import sys

GLib.set_prgname("dms-control-center")
GLib.set_application_name("dms-control-center")

css_path = os.path.expanduser("~/.config/hypr/scripts/control_center.css")

def get_uptime():
    try:
        out = subprocess.check_output(["uptime", "-p"]).decode("utf-8").strip()
        # e.g., "up 10 hours, 23 minutes"
        return out
    except Exception:
        return "up 0 minutes"

def get_wifi_status():
    try:
        out = subprocess.check_output(["nmcli", "-t", "-f", "TYPE,STATE,CONNECTION", "dev"], timeout=1).decode("utf-8").strip()
        for line in out.split("\n"):
            if line.startswith("wifi:connected:"):
                parts = line.split(":", 2)
                conn = parts[2] if len(parts) > 2 and parts[2] else "Connected"
                return conn, "Connected", True
        return "Not connected", "Disconnected", False
    except Exception:
        return "Not connected", "Disconnected", False

def get_bluetooth_status():
    try:
        out = subprocess.check_output(["bluetoothctl", "show"]).decode("utf-8")
        if "Powered: yes" in out:
            # Check for connected device
            try:
                devs = subprocess.check_output(["bluetoothctl", "devices", "Connected"]).decode("utf-8").strip()
                if devs:
                    dev_name = devs.split(" ", 2)[-1]
                    return "Connected", dev_name, True
            except Exception:
                pass
            return "Enabled", "No devices", True
        return "Disabled", "Off", False
    except Exception:
        return "Disabled", "Off", False

def get_tailscale_status():
    try:
        out = subprocess.check_output(["tailscale", "ip", "-4"], timeout=1).decode("utf-8").strip()
        if out:
            return "Tailscale", "Connected", True
        return "Tailscale", "Off", False
    except Exception:
        return "Tailscale", "Off", False

pid_file = "/tmp/control_center.pid"
if os.path.exists(pid_file):
    try:
        with open(pid_file) as f:
            old_pid = int(f.read().strip())
        os.kill(old_pid, 9)
        os.remove(pid_file)
        sys.exit(0)
    except Exception:
        if os.path.exists(pid_file):
            try:
                os.remove(pid_file)
            except Exception:
                pass

with open(pid_file, "w") as f:
    f.write(str(os.getpid()))

def cleanup():
    if os.path.exists(pid_file):
        try:
            os.remove(pid_file)
        except Exception:
            pass

import cairo

class ControlCenter(Gtk.Window):
    def __init__(self):
        super().__init__(title="control-center-popup")
        self.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_name("MainWindow")
        self.set_default_size(460, -1)
        self.set_app_paintable(True)

        # Enable Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.connect("draw", self.on_draw)

        # Main Vertical Container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        main_box.set_name("MainBox")
        self.add(main_box)

        # ============================================================
        # 1. USER PROFILE HEADER CARD
        # ============================================================
        header_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        header_card.set_name("HeaderCard")

        # Avatar Image
        avatar_box = Gtk.Box()
        avatar_box.set_name("AvatarBox")
        avatar_img = Gtk.Image()
        avatar_img.set_from_icon_name("avatar-default", Gtk.IconSize.DND)
        avatar_box.pack_start(avatar_img, True, True, 0)
        header_card.pack_start(avatar_box, False, False, 0)

        # User Info Stack
        user_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        user_info_box.set_name("UserInfoBox")
        user_info_box.set_valign(Gtk.Align.CENTER)

        try:
            username = os.getlogin().capitalize()
        except Exception:
            username = "Ravindra"

        self.user_label = Gtk.Label(label=username)
        self.user_label.set_name("UserNameLabel")
        self.user_label.set_xalign(0.0)

        self.uptime_label = Gtk.Label(label=get_uptime())
        self.uptime_label.set_name("UptimeLabel")
        self.uptime_label.set_xalign(0.0)

        user_info_box.pack_start(self.user_label, False, False, 0)
        user_info_box.pack_start(self.uptime_label, False, False, 0)
        header_card.pack_start(user_info_box, True, True, 0)

        # Quick Action Buttons (Lock, Power, Settings, Edit)
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        actions_box.set_name("ActionsBox")
        actions_box.set_valign(Gtk.Align.CENTER)

        btn_lock = Gtk.Button(label="🔒")
        btn_lock.set_name("ActionBtn")
        btn_lock.connect("clicked", lambda x: (subprocess.Popen(["hyprlock"]), Gtk.main_quit()))

        btn_power = Gtk.Button(label="⏻")
        btn_power.set_name("ActionBtn")
        btn_power.connect("clicked", lambda x: (subprocess.Popen(["wlogout", "--layout", "/home/ravindra/.config/wlogout/layout", "--css", "/home/ravindra/.config/wlogout/style.css", "-b", "3"]), Gtk.main_quit()))

        btn_settings = Gtk.Button(label="")
        btn_settings.set_name("ActionBtn")
        btn_settings.connect("clicked", lambda x: (subprocess.Popen(["kitty", "-e", "nmtui"]), Gtk.main_quit()))

        btn_edit = Gtk.Button(label="✎")
        btn_edit.set_name("ActionBtn")
        btn_edit.connect("clicked", lambda x: (subprocess.Popen(["bash", "/home/ravindra/.config/hypr/wallpaper.sh"]), Gtk.main_quit()))

        actions_box.pack_start(btn_lock, False, False, 0)
        actions_box.pack_start(btn_power, False, False, 0)
        actions_box.pack_start(btn_settings, False, False, 0)
        actions_box.pack_start(btn_edit, False, False, 0)

        header_card.pack_start(actions_box, False, False, 0)
        main_box.pack_start(header_card, False, False, 0)

        # ============================================================
        # 2. SLIDERS ROW (Volume & Brightness)
        # ============================================================
        sliders_grid = Gtk.Grid(column_spacing=16, column_homogeneous=True)
        sliders_grid.set_name("SlidersGrid")

        # Volume Box
        vol_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vol_box.set_name("SliderBox")
        vol_icon = Gtk.Label(label="🔊")
        vol_icon.set_name("SliderIcon")

        self.vol_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.vol_scale.set_range(0, 100)
        self.vol_scale.set_value(self.get_volume())
        self.vol_scale.set_draw_value(False)
        self.vol_scale.connect("value-changed", self.set_volume)

        vol_box.pack_start(vol_icon, False, False, 0)
        vol_box.pack_start(self.vol_scale, True, True, 0)
        sliders_grid.attach(vol_box, 0, 0, 1, 1)

        # Brightness Box
        bright_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        bright_box.set_name("SliderBox")
        bright_icon = Gtk.Label(label="🔅")
        bright_icon.set_name("SliderIcon")

        self.bright_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        self.bright_scale.set_range(5, 100)
        self.bright_scale.set_value(self.get_brightness())
        self.bright_scale.set_draw_value(False)
        self.bright_scale.connect("value-changed", self.set_brightness)

        bright_box.pack_start(bright_icon, False, False, 0)
        bright_box.pack_start(self.bright_scale, True, True, 0)
        sliders_grid.attach(bright_box, 1, 0, 1, 1)

        main_box.pack_start(sliders_grid, False, False, 0)

        # ============================================================
        # 3. QUICK TOGGLE CARDS (Wi-Fi & Bluetooth)
        # ============================================================
        tiles_grid = Gtk.Grid(column_spacing=10, column_homogeneous=True)
        tiles_grid.set_name("TilesGrid")

        # Wi-Fi Tile
        self.wifi_btn = Gtk.Button()
        self.wifi_btn.set_name("TileCard")
        self.wifi_btn.connect("clicked", self.toggle_wifi)

        wifi_tile_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.wifi_icon_box = Gtk.Box()
        self.wifi_icon_box.set_name("TileIconBox")
        self.wifi_icon_box.set_valign(Gtk.Align.CENTER)
        self.wifi_icon_lbl = Gtk.Label(label="󰤨")
        self.wifi_icon_lbl.set_name("TileIcon")
        self.wifi_icon_lbl.set_xalign(0.5)
        self.wifi_icon_lbl.set_yalign(0.5)
        self.wifi_icon_box.pack_start(self.wifi_icon_lbl, True, True, 0)

        wifi_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        wifi_text_box.set_valign(Gtk.Align.CENTER)

        self.wifi_title_lbl = Gtk.Label()
        self.wifi_title_lbl.set_name("TileTitle")
        self.wifi_title_lbl.set_xalign(0.0)

        self.wifi_sub_lbl = Gtk.Label()
        self.wifi_sub_lbl.set_name("TileSubtitle")
        self.wifi_sub_lbl.set_xalign(0.0)

        wifi_text_box.pack_start(self.wifi_title_lbl, False, False, 0)
        wifi_text_box.pack_start(self.wifi_sub_lbl, False, False, 0)

        wifi_tile_box.pack_start(self.wifi_icon_box, False, False, 0)
        wifi_tile_box.pack_start(wifi_text_box, True, True, 0)
        self.wifi_btn.add(wifi_tile_box)
        tiles_grid.attach(self.wifi_btn, 0, 0, 1, 1)

        # Bluetooth Tile
        self.bt_btn = Gtk.Button()
        self.bt_btn.set_name("TileCard")
        self.bt_btn.connect("clicked", self.toggle_bt)

        bt_tile_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.bt_icon_box = Gtk.Box()
        self.bt_icon_box.set_name("TileIconBox")
        self.bt_icon_box.set_valign(Gtk.Align.CENTER)
        self.bt_icon_lbl = Gtk.Label(label="󰂯")
        self.bt_icon_lbl.set_name("TileIcon")
        self.bt_icon_lbl.set_xalign(0.5)
        self.bt_icon_lbl.set_yalign(0.5)
        self.bt_icon_box.pack_start(self.bt_icon_lbl, True, True, 0)

        bt_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        bt_text_box.set_valign(Gtk.Align.CENTER)

        self.bt_title_lbl = Gtk.Label()
        self.bt_title_lbl.set_name("TileTitle")
        self.bt_title_lbl.set_xalign(0.0)

        self.bt_sub_lbl = Gtk.Label()
        self.bt_sub_lbl.set_name("TileSubtitle")
        self.bt_sub_lbl.set_xalign(0.0)

        bt_text_box.pack_start(self.bt_title_lbl, False, False, 0)
        bt_text_box.pack_start(self.bt_sub_lbl, False, False, 0)

        bt_tile_box.pack_start(self.bt_icon_box, False, False, 0)
        bt_tile_box.pack_start(bt_text_box, True, True, 0)
        self.bt_btn.add(bt_tile_box)
        tiles_grid.attach(self.bt_btn, 1, 0, 1, 1)

        # Tailscale Tile
        self.ts_btn = Gtk.Button()
        self.ts_btn.set_name("TileCard")
        self.ts_btn.connect("clicked", self.toggle_tailscale)

        ts_tile_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.ts_icon_box = Gtk.Box()
        self.ts_icon_box.set_name("TileIconBox")
        self.ts_icon_box.set_valign(Gtk.Align.CENTER)
        self.ts_icon_lbl = Gtk.Label(label="󰖂")
        self.ts_icon_lbl.set_name("TileIcon")
        self.ts_icon_lbl.set_xalign(0.5)
        self.ts_icon_lbl.set_yalign(0.5)
        self.ts_icon_box.pack_start(self.ts_icon_lbl, True, True, 0)

        ts_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        ts_text_box.set_valign(Gtk.Align.CENTER)

        self.ts_title_lbl = Gtk.Label()
        self.ts_title_lbl.set_name("TileTitle")
        self.ts_title_lbl.set_xalign(0.0)

        self.ts_sub_lbl = Gtk.Label()
        self.ts_sub_lbl.set_name("TileSubtitle")
        self.ts_sub_lbl.set_xalign(0.0)

        ts_text_box.pack_start(self.ts_title_lbl, False, False, 0)
        ts_text_box.pack_start(self.ts_sub_lbl, False, False, 0)

        ts_tile_box.pack_start(self.ts_icon_box, False, False, 0)
        ts_tile_box.pack_start(ts_text_box, True, True, 0)
        self.ts_btn.add(ts_tile_box)
        tiles_grid.attach(self.ts_btn, 2, 0, 1, 1)

        main_box.pack_start(tiles_grid, False, False, 0)

        # Asynchronous State Refresh
        GLib.idle_add(self.update_state)
        GLib.timeout_add_seconds(2, self.update_state)

        self.apply_css()
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        self.connect("focus-out-event", lambda w, e: Gtk.main_quit())

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        return False

    def get_brightness(self):
        try:
            res = subprocess.check_output(["brightnessctl", "-m"]).decode("utf-8").strip()
            perc = res.split(",")[3].replace("%", "")
            return float(perc)
        except Exception:
            return 50.0

    def set_brightness(self, widget):
        val = int(widget.get_value())
        subprocess.Popen(["brightnessctl", "set", f"{val}%"])

    def get_volume(self):
        try:
            res = subprocess.check_output(["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"]).decode("utf-8").strip()
            val = float(res.split()[1]) * 100
            return val
        except Exception:
            return 50.0

    def set_volume(self, widget):
        val = int(widget.get_value())
        subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{val/100:.2f}"])

    def toggle_wifi(self, widget):
        subprocess.Popen(["nmcli", "radio", "wifi", "toggle"])
        GLib.timeout_add(500, self.update_state)

    def toggle_bt(self, widget):
        subprocess.Popen(["rfkill", "toggle", "bluetooth"])
        GLib.timeout_add(500, self.update_state)

    def toggle_tailscale(self, widget):
        try:
            out = subprocess.check_output(["tailscale", "ip", "-4"], timeout=1).decode("utf-8").strip()
            if out:
                subprocess.Popen(["tailscale", "down"])
            else:
                subprocess.Popen(["tailscale", "up", "--ssh"])
        except Exception:
            subprocess.Popen(["tailscale", "up", "--ssh"])
        GLib.timeout_add(800, self.update_state)

    def update_state(self):
        # Update Uptime
        self.uptime_label.set_text(get_uptime())

        # Update Wi-Fi Status
        title, sub, active = get_wifi_status()
        self.wifi_title_lbl.set_text(title)
        self.wifi_sub_lbl.set_text(sub)
        if active:
            self.wifi_icon_lbl.set_text("󰤨")
            self.wifi_icon_box.get_style_context().add_class("active")
        else:
            self.wifi_icon_lbl.set_text("󰖪")
            self.wifi_icon_box.get_style_context().remove_class("active")

        # Update Bluetooth Status
        title, sub, active = get_bluetooth_status()
        self.bt_title_lbl.set_text(title)
        self.bt_sub_lbl.set_text(sub)
        if active:
            self.bt_icon_lbl.set_text("󰂯")
            self.bt_icon_box.get_style_context().add_class("active")
        else:
            self.bt_icon_lbl.set_text("󰂲")
            self.bt_icon_box.get_style_context().remove_class("active")

        # Update Tailscale Status
        title, sub, active = get_tailscale_status()
        self.ts_title_lbl.set_text(title)
        self.ts_sub_lbl.set_text(sub)
        if active:
            self.ts_icon_box.get_style_context().add_class("active")
        else:
            self.ts_icon_box.get_style_context().remove_class("active")

        return True

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        try:
            with open("/home/ravindra/.config/waybar/colors.css", "r") as f:
                colors_css = f.read()
            with open(css_path, "r") as f:
                main_css = f.read()
            
            main_css = main_css.replace('@import url("/home/ravindra/.config/waybar/colors.css");', '')
            combined_css = colors_css + "\n" + main_css
            css_provider.load_from_data(combined_css.encode('utf-8'))
            
            screen = Gdk.Screen.get_default()
            Gtk.StyleContext.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        except Exception as e:
            print(f"Error loading CSS: {e}")

    def on_draw(self, widget, cr):
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        return False

if __name__ == '__main__':
    win = ControlCenter()
    win.connect("destroy", lambda w: (cleanup(), Gtk.main_quit()))
    win.show_all()
    win.present()
    Gtk.main()
