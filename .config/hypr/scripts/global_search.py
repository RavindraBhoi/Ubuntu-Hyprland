#!/usr/bin/env python3
import gi
import os
import sys
import glob
import threading
import subprocess
import urllib.parse

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import json
import base64

class GlobalSearch(Gtk.Window):
    def __init__(self):
        super().__init__(title="global-search")
        
        # Native GTK Window Properties (Hyprland handles it natively now)
        self.set_decorated(False)
        self.set_default_size(800, -1)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        
        # Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        self.set_app_paintable(True)
        
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.main_box.set_name("MainBox")
        self.add(self.main_box)
        
        # Input Area
        self.entry = Gtk.Entry()
        self.entry.set_name("SearchInput")
        self.entry.set_placeholder_text("Search apps, files, or web...")
        self.entry.connect("changed", self.on_text_changed)
        self.entry.connect("activate", self.on_activate_entry)
        self.entry.connect("key-press-event", self.on_entry_key)
        self.main_box.pack_start(self.entry, False, False, 0)
        
        # Results Area
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scroll.set_name("ScrollArea")
        
        if hasattr(self.scroll, 'set_propagate_natural_height'):
            self.scroll.set_propagate_natural_height(True)
        self.scroll.set_max_content_height(450)
        
        self.main_box.pack_start(self.scroll, True, True, 0)
        
        self.listbox = Gtk.ListBox()
        self.listbox.set_name("ResultsList")
        self.listbox.connect("row-activated", self.on_row_activated)
        self.scroll.add(self.listbox)
        
        self.connect("key-press-event", self.on_key_press)
        
        # Caches
        self.apps = self.load_apps()
        self.search_thread = None
        self.search_counter = 0
        
        self.apply_css()
        self.populate_results("")
        
    def load_apps(self):
        apps = []
        app_dirs = ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]
        for d in app_dirs:
            if not os.path.exists(d): continue
            for f in glob.glob(os.path.join(d, "*.desktop")):
                try:
                    name = None
                    exec_cmd = None
                    with open(f, "r") as fp:
                        for line in fp:
                            if line.startswith("Name=") and not name:
                                name = line.strip().split("=", 1)[1]
                            elif line.startswith("Exec=") and not exec_cmd:
                                exec_cmd = line.strip().split("=", 1)[1]
                    if name and exec_cmd:
                        apps.append({"type": "app", "name": name, "exec": exec_cmd, "path": f})
                except:
                    pass
        # Deduplicate and sort
        seen = set()
        unique_apps = []
        for a in sorted(apps, key=lambda x: x["name"]):
            if a["name"] not in seen:
                seen.add(a["name"])
                unique_apps.append(a)
        return unique_apps

    def on_text_changed(self, entry):
        query = entry.get_text().strip()
        
        # Proper GTK debounce
        if hasattr(self, '_search_timer') and self._search_timer:
            GLib.source_remove(self._search_timer)
            
        self._search_timer = GLib.timeout_add(250, self.start_search_thread, query)

    def start_search_thread(self, query):
        self._search_timer = None
        self.search_counter += 1
        threading.Thread(target=self.run_search, args=(query, self.search_counter), daemon=True).start()
        return False

    def run_search(self, query, counter):
        if counter != self.search_counter:
            return
            
        results = []
        if query:
            try:
                # 1. Web Search
                results.append({"type": "web", "name": f"🌐 Search web for '{query}'", "url": f"https://google.com/search?q={urllib.parse.quote(query)}"})
                
                # 2. Apps
                q_lower = query.lower()
                matched_apps = [a for a in self.apps if q_lower in a["name"].lower()][:5]
                results.extend(matched_apps)
                
                # 3. Files
                try:
                    out = subprocess.check_output(
                        ["fdfind", "-i", query, os.path.expanduser("~"), "--max-depth", "6", "--max-results", "15"],
                        stderr=subprocess.DEVNULL, timeout=2
                    ).decode("utf-8").strip().split('\n')
                    for path in out:
                        if path:
                            results.append({"type": "file", "name": f"📄 {os.path.basename(path)}", "path": path})
                except Exception as ex:
                    with open("/tmp/search_debug.log", "a") as f:
                        f.write(f"File search error: {ex}\n")
            except Exception as e:
                with open("/tmp/search_debug.log", "a") as f:
                    f.write(f"General error: {e}\n")
        else:
            # Default state is an empty list to keep the window small
            results = []
            
        with open("/tmp/search_debug.log", "w") as f:
            f.write(f"Query: {query} | Total Results: {len(results)}\n")
            for r in results:
                f.write(f" - {r['type']}: {r['name']}\n")
                
        GLib.idle_add(self.update_listbox, results, counter)

    def update_listbox(self, results, counter):
        if counter != self.search_counter:
            return
            
        for child in self.listbox.get_children():
            self.listbox.remove(child)
            
        if not results:
            self.scroll.hide()
        else:
            self.scroll.show()
            # Force Layer Shell to allocate vertical pixels!
            self.scroll.set_min_content_height(min(450, len(results) * 45))
            
        for r in results:
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            
            if r["type"] == "app":
                lbl = Gtk.Label(label=f"📱 {r['name']}")
            elif r["type"] == "file":
                lbl = Gtk.Label(label=r['name'])
            else:
                lbl = Gtk.Label(label=r['name'])
                
            lbl.set_halign(Gtk.Align.START)
            box.pack_start(lbl, True, True, 10)
            
            if r["type"] == "file":
                path_lbl = Gtk.Label(label=r['path'].replace(os.path.expanduser("~"), "~"))
                path_lbl.set_halign(Gtk.Align.END)
                path_lbl.get_style_context().add_class("dim-label")
                box.pack_start(path_lbl, False, False, 10)
                
            row.add(box)
            row.data = r
            self.listbox.add(row)
            
        self.listbox.show_all()
        # Force Wayland compositor to recalculate window height dynamically
        self.resize(1, 1)
        
        # Automatically select the first row so Enter works instantly
        if results:
            self.listbox.select_row(self.listbox.get_row_at_index(0))

    def close_app(self):
        self.destroy()
        while Gtk.events_pending():
            Gtk.main_iteration()
            
        # Brutally terminate all instances
        os.system("pkill -f '[g]lobal_search.py'")
        sys.exit(0)

    def on_row_activated(self, listbox, row):
        data = row.data
        if data["type"] == "web":
            subprocess.Popen(["xdg-open", data["url"]])
        elif data["type"] == "app":
            app_id = os.path.basename(data['path'])
            subprocess.Popen(f"gtk-launch '{app_id}' || ({data['exec'].split(' %')[0]} &)", shell=True)
        elif data["type"] == "file":
            subprocess.Popen(["xdg-open", data["path"]])
            
        self.close_app()

    def on_activate_entry(self, entry):
        row = self.listbox.get_selected_row()
        if row:
            self.on_row_activated(self.listbox, row)
            
    def on_entry_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.close_app()
            return True
        elif event.keyval in (Gdk.KEY_Down, Gdk.KEY_Up):
            row = self.listbox.get_selected_row()
            next_row = None
            if not row:
                if event.keyval == Gdk.KEY_Down:
                    next_row = self.listbox.get_row_at_index(0)
            else:
                idx = row.get_index()
                if event.keyval == Gdk.KEY_Down:
                    next_row = self.listbox.get_row_at_index(idx + 1)
                else:
                    next_row = self.listbox.get_row_at_index(idx - 1)
            
            if next_row:
                self.listbox.select_row(next_row)
                # Auto-scroll to keep selection in view
                adj = self.scroll.get_vadjustment()
                alloc = next_row.get_allocation()
                if alloc.y < adj.get_value():
                    adj.set_value(alloc.y)
                elif alloc.y + alloc.height > adj.get_value() + adj.get_page_size():
                    adj.set_value(alloc.y + alloc.height - adj.get_page_size())
            return True
        return False

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.close_app()
            return True
        return False

    def populate_results(self, query):
        self.on_text_changed(self.entry)

    def apply_css(self):
        settings = Gtk.Settings.get_default()
        if settings:
            settings.set_property("gtk-application-prefer-dark-theme", True)
            
        try:
            with open("/home/ravindra/.config/waybar/colors.css", "r") as f:
                colors_css = f.read()
        except:
            colors_css = ""

        custom_css = """
        window {
            background-color: transparent;
        }
        #MainBox {
            padding: 20px;
            background-color: alpha(@surface, 0.85);
            border-radius: 0px 0px 20px 20px;
            border-bottom: 2px solid alpha(@outline, 0.5);
            border-left: 2px solid alpha(@outline, 0.5);
            border-right: 2px solid alpha(@outline, 0.5);
        }
        #ScrollArea {
            background-color: transparent;
        }
        #SearchInput {
            padding: 16px;
            border-radius: 14px;
            background-color: alpha(@surface_variant, 0.5);
            color: @on_surface;
            font-size: 20px;
            font-weight: bold;
            border: 1px solid alpha(@outline, 0.3);
            box-shadow: none;
        }
        #ResultsList {
            background-color: transparent;
        }
        row {
            padding: 12px;
            color: @on_surface;
            font-size: 16px;
            border-radius: 12px;
            margin-bottom: 4px;
        }
        row:hover {
            background-color: alpha(@surface_variant, 0.5);
        }
        row:selected {
            background-color: @primary;
            color: @on_primary;
        }
        .dim-label {
            opacity: 0.6;
            font-size: 13px;
        }
        """
        combined_css = colors_css + "\n" + custom_css
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(combined_css.encode('utf-8'))
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

if __name__ == "__main__":
    app = GlobalSearch()
    app.show_all()
    app.entry.grab_focus()
    Gtk.main()
