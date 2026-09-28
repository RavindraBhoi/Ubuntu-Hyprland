#!/usr/bin/env python3
"""
Material You GTK3 Notification Daemon for Hyprland
Implements org.freedesktop.Notifications DBus Service and renders floating notification popups styled with Matugen wallpaper colors.
Supports DBus ActionInvoked signal so clicking notifications opens screenshots or links.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import dbus
import dbus.service
import dbus.mainloop.glib
import os
import sys

GLib.set_prgname("hypr-notification")
GLib.set_application_name("hypr-notification")

BUS_NAME = 'org.freedesktop.Notifications'
OBJECT_PATH = '/org/freedesktop/Notifications'

class NotificationPopup(Gtk.Window):
    def __init__(self, nid, app_name, app_icon, summary, body, expire_timeout, on_close_cb, on_action_cb, actions):
        super().__init__(title="hypr-notification")
        self.nid = nid
        self.on_close_cb = on_close_cb
        self.on_action_cb = on_action_cb
        self.actions = actions
        
        self.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.set_name("NotificationWindow")

        # Enable Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        self.apply_css()

        # Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        main_box.set_name("NotificationBox")
        self.add(main_box)

        # Icon
        icon_widget = self.create_icon_widget(app_icon)
        if icon_widget:
            main_box.pack_start(icon_widget, False, False, 0)

        # Content Text Box
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        content_box.set_valign(Gtk.Align.CENTER)
        main_box.pack_start(content_box, True, True, 0)

        # App Name & Summary
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        summary_lbl = Gtk.Label()
        summary_lbl.set_markup(f"<b>{GLib.markup_escape_text(summary)}</b>")
        summary_lbl.set_name("NotificationSummary")
        summary_lbl.set_xalign(0.0)
        summary_lbl.set_ellipsize(3) # PANGO_ELLIPSIZE_END
        header_box.pack_start(summary_lbl, True, True, 0)

        content_box.pack_start(header_box, False, False, 0)

        # Body Text
        if body:
            body_lbl = Gtk.Label()
            body_lbl.set_markup(GLib.markup_escape_text(body))
            body_lbl.set_name("NotificationBody")
            body_lbl.set_xalign(0.0)
            body_lbl.set_line_wrap(True)
            body_lbl.set_max_width_chars(35)
            content_box.pack_start(body_lbl, False, False, 0)

        # Close Button
        close_btn = Gtk.Button(label="✕")
        close_btn.set_name("NotificationCloseBtn")
        close_btn.set_valign(Gtk.Align.START)
        close_btn.connect("clicked", lambda w: self.dismiss())
        main_box.pack_start(close_btn, False, False, 0)

        # Click anywhere on card triggers action (or default)
        self.connect("button-press-event", self.on_card_clicked)

        # Auto dismiss timeout
        timeout_ms = 3500 if actions else 2000
        self.timer_id = GLib.timeout_add(timeout_ms, self.dismiss)

    def on_card_clicked(self, widget, event):
        action_key = "default"
        if self.actions and len(self.actions) >= 2:
            action_key = str(self.actions[0])
        elif self.actions and len(self.actions) == 1:
            action_key = str(self.actions[0])
        
        if self.on_action_cb:
            self.on_action_cb(self.nid, action_key)
        self.dismiss()
        return True

    def create_icon_widget(self, icon_name):
        if not icon_name:
            icon_name = "dialog-information"
        
        # Check if file path
        if os.path.exists(icon_name):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_name, 36, 36, True)
                return Gtk.Image.new_from_pixbuf(pixbuf)
            except Exception:
                pass
        
        # Fallback to theme icon
        img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
        img.set_pixel_size(36)
        img.set_name("NotificationIcon")
        return img

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        style_css = """
        @import url("/home/ravindra/.config/waybar/colors.css");

        #NotificationWindow {
            background-color: alpha(@surface, 0.94);
            border: none;
            border-radius: 8px;
            min-width: 406px;
        }

        #NotificationBox {
            padding: 12px 16px;
        }

        #NotificationSummary {
            font-family: "JetBrains Mono", sans-serif;
            font-size: 14px;
            color: @primary;
        }

        #NotificationBody {
            font-family: "JetBrains Mono", "Roboto", sans-serif;
            font-size: 12px;
            color: @on_surface;
        }

        #NotificationCloseBtn {
            background: transparent;
            border: none;
            box-shadow: none;
            color: @on_surface_variant;
            font-size: 12px;
            padding: 0px 4px;
        }

        #NotificationCloseBtn:hover {
            color: @error;
        }
        """
        css_provider.load_from_data(style_css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def dismiss(self):
        if hasattr(self, 'timer_id') and self.timer_id:
            GLib.source_remove(self.timer_id)
            self.timer_id = None
        self.destroy()
        if self.on_close_cb:
            self.on_close_cb(self.nid)
        return False

class NotificationService(dbus.service.Object):
    def __init__(self, bus):
        bus_name = dbus.service.BusName(BUS_NAME, bus)
        super().__init__(bus_name, OBJECT_PATH)
        self.current_id = 0
        self.popups = {}

    @dbus.service.signal(BUS_NAME, signature='us')
    def ActionInvoked(self, id, action_key):
        pass

    @dbus.service.signal(BUS_NAME, signature='uu')
    def NotificationClosed(self, id, reason):
        pass

    @dbus.service.method(BUS_NAME, out_signature='as')
    def GetCapabilities(self):
        return ['body', 'icon-static', 'actions']

    @dbus.service.method(BUS_NAME, in_signature='susssasa{sv}i', out_signature='u')
    def Notify(self, app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout):
        if replaces_id > 0 and replaces_id in self.popups:
            self.popups[replaces_id].dismiss()
            nid = replaces_id
        else:
            self.current_id += 1
            nid = self.current_id

        def on_close(closed_nid):
            if closed_nid in self.popups:
                del self.popups[closed_nid]
            self.NotificationClosed(closed_nid, 2)

        def on_action(action_nid, action_key):
            self.ActionInvoked(action_nid, action_key)

        popup = NotificationPopup(nid, app_name, app_icon, summary, body, expire_timeout, on_close, on_action, actions)
        self.popups[nid] = popup

        popup.show_all()
        popup.present()

        return nid

    @dbus.service.method(BUS_NAME, in_signature='u', out_signature='')
    def CloseNotification(self, id):
        if id in self.popups:
            self.popups[id].dismiss()

    @dbus.service.method(BUS_NAME, in_signature='', out_signature='ssss')
    def GetServerInformation(self):
        return ("MaterialNotification", "AGY", "1.0", "1.2")

if __name__ == '__main__':
    GLib.set_prgname("hypr-notification")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()

    service = NotificationService(session_bus)
    print("Notification daemon started with ActionInvoked support!")
    Gtk.main()
