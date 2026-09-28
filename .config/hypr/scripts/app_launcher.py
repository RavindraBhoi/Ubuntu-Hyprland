#!/usr/bin/env python3
import gi
import os
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, GLib

class AppItem(Gtk.Box):
    def __init__(self, app_info):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.app_info = app_info
        self.set_name("AppItem")
        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        
        # Load Icon
        icon_widget = Gtk.Image()
        icon_widget.set_pixel_size(48)
        icon = app_info.get_icon()
        if icon:
            if type(icon) == Gio.FileIcon:
                # Sometimes icons are raw files
                icon_widget.set_from_file(icon.get_file().get_path())
            else:
                icon_theme = Gtk.IconTheme.get_default()
                try:
                    pixbuf = icon_theme.load_icon(icon.to_string(), 48, 0)
                    icon_widget.set_from_pixbuf(pixbuf)
                except:
                    icon_widget.set_from_icon_name("application-x-executable", Gtk.IconSize.DND)
        else:
            icon_widget.set_from_icon_name("application-x-executable", Gtk.IconSize.DND)
            
        self.pack_start(icon_widget, False, False, 0)
        
        # Load Label
        label = Gtk.Label(label=app_info.get_display_name())
        label.set_name("AppLabel")
        label.set_max_width_chars(12)
        label.set_ellipsize(3) # Pango.EllipsizeMode.END
        label.set_justify(Gtk.Justification.CENTER)
        self.pack_start(label, False, False, 0)
        
        # Make the box a bit larger for click area
        self.set_size_request(80, 80)

class AppLauncher(Gtk.Window):
    def __init__(self):
        super().__init__(title="app-launcher-popup")
        self.set_decorated(False)
        self.set_default_size(800, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        self.set_app_paintable(True)
        
        # Main Layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.main_box.set_name("MainBox")
        self.add(self.main_box)
        
        # Left Sidebar (Categories)
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.sidebar.set_name("Sidebar")
        self.sidebar.set_size_request(200, -1)
        self.main_box.pack_start(self.sidebar, False, False, 0)
        
        title = Gtk.Label(label="Categories")
        title.set_name("SidebarTitle")
        title.set_halign(Gtk.Align.START)
        self.sidebar.pack_start(title, False, False, 10)
        
        self.category_list = Gtk.ListBox()
        self.category_list.set_name("CategoryList")
        self.category_list.connect("row-activated", self.on_category_selected)
        
        # Right Area (Search + Grid)
        self.right_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.right_area.set_name("RightArea")
        self.main_box.pack_start(self.right_area, True, True, 0)
        
        # Search Bar
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.set_name("SearchBox")
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_name("SearchEntry")
        self.search_entry.set_placeholder_text("Search apps...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        search_box.pack_start(self.search_entry, True, True, 0)
        self.right_area.pack_start(search_box, False, False, 0)
        
        # App Grid
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.right_area.pack_start(scroll, True, True, 0)
        
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_name("AppGrid")
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(6)
        self.flowbox.set_min_children_per_line(4)
        self.flowbox.set_homogeneous(True)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.connect("child-activated", self.on_app_activated)
        scroll.add(self.flowbox)
        
        # Load Apps
        self.all_apps = []
        self.load_apps()
        
        # Escape to close
        self.connect("key-press-event", self.on_key_press)
        self.connect("destroy", Gtk.main_quit)
        
        # Close on focus out (Wayland might need hyprland window rules for this though, but good practice)
        self.connect("focus-out-event", lambda w, e: Gtk.main_quit())
        
        self.apply_css()

    def load_apps(self):
        apps = Gio.AppInfo.get_all()
        categories = set(["All Apps"])
        
        for app in apps:
            if not app.should_show():
                continue
            
            # Extract main category
            cats = app.get_categories()
            main_cat = "Other"
            if cats:
                for c in ["Network", "Game", "Development", "System", "Utility", "Office", "AudioVideo", "Graphics"]:
                    if c in cats:
                        main_cat = c
                        break
            
            categories.add(main_cat)
            
            item = AppItem(app)
            item.category = main_cat
            item.search_text = app.get_display_name().lower()
            
            # Wrap in FlowBoxChild
            child = Gtk.FlowBoxChild()
            child.add(item)
            child.set_name("AppChild")
            child.set_halign(Gtk.Align.CENTER)
            child.set_valign(Gtk.Align.START)
            self.flowbox.add(child)
            self.all_apps.append(child)
            
        # Populate Category List
        sorted_cats = ["All Apps"] + sorted([c for c in categories if c != "All Apps"])
        for cat in sorted_cats:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=cat)
            label.set_halign(Gtk.Align.START)
            label.set_margin_top(10)
            label.set_margin_bottom(10)
            label.set_margin_start(15)
            row.add(label)
            row.category_name = cat
            self.category_list.add(row)
            
        self.sidebar.pack_start(self.category_list, True, True, 0)
        
        # Setup Filter
        self.current_category = "All Apps"
        self.flowbox.set_filter_func(self.filter_apps)
        
        # Select first category
        row = self.category_list.get_row_at_index(0)
        self.category_list.select_row(row)

    def on_category_selected(self, listbox, row):
        if row:
            self.current_category = row.category_name
            self.flowbox.invalidate_filter()

    def on_search_changed(self, entry):
        self.flowbox.invalidate_filter()

    def filter_apps(self, child):
        item = child.get_child()
        
        # Category Filter
        if self.current_category != "All Apps" and item.category != self.current_category:
            return False
            
        # Search Filter
        search_query = self.search_entry.get_text().lower()
        if search_query and search_query not in item.search_text:
            return False
            
        return True

    def on_app_activated(self, flowbox, child):
        app_info = child.get_child().app_info
        try:
            # Launch via Gio
            app_info.launch([], None)
            Gtk.main_quit()
        except Exception as e:
            print(f"Failed to launch: {e}")

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        return False

    def apply_css(self):
        try:
            with open("/home/ravindra/.config/waybar/colors.css", "r") as f:
                colors_css = f.read()
        except:
            colors_css = ""

        try:
            with open("/home/ravindra/.config/hypr/scripts/app_launcher.css", "r") as f:
                custom_css = f.read()
        except:
            custom_css = ""

        combined_css = colors_css + "\n" + custom_css
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(combined_css.encode('utf-8'))
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

if __name__ == "__main__":
    app = AppLauncher()
    app.show_all()
    Gtk.main()
