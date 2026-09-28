#!/usr/bin/env python3
import gi
import os
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class AIChatPopup(Gtk.Window):
    def __init__(self):
        super().__init__(title="ai-chat-popup")
        self.set_decorated(False)
        self.set_default_size(700, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        self.set_app_paintable(True)
        
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_box.set_name("MainBox")
        self.add(self.main_box)
        
        # Output Area
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_name("ScrollArea")
        self.main_box.pack_start(scroll, True, True, 0)
        
        self.text_view = Gtk.TextView()
        self.text_view.set_name("ChatOutput")
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        scroll.add(self.text_view)
        
        # Input Area
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        input_box.set_name("InputBox")
        self.main_box.pack_start(input_box, False, False, 10)
        
        self.entry = Gtk.Entry()
        self.entry.set_name("ChatInput")
        self.entry.set_placeholder_text("Ask Gemini Pro...")
        self.entry.connect("activate", self.on_send)
        input_box.pack_start(self.entry, True, True, 0)
        
        self.spinner = Gtk.Spinner()
        input_box.pack_start(self.spinner, False, False, 0)
        
        # Initialization
        self.buffer = self.text_view.get_buffer()
        self.api_key = os.environ.get("GEMINI_API_KEY", "")
        self.attached_image = None
        
        # Fallback to reading from a file if environment variable isn't set
        key_file = os.path.expanduser("~/.gemini_api_key")
        if not self.api_key and os.path.exists(key_file):
            try:
                with open(key_file, "r") as f:
                    self.api_key = f.read().strip()
            except Exception:
                pass
        
        if not HAS_GENAI:
            self.append_text("System: google-genai library is not installed.\n")
        elif not self.api_key:
            self.append_text("System: Welcome! Please save your API key in ~/.gemini_api_key\n\n")
        else:
            self.append_text("System: Ready to chat with Gemini Pro.\n\n")
            self.client = genai.Client(api_key=self.api_key)
            
        self.connect("key-press-event", self.on_key_press)
        self.apply_css()

    def append_text(self, text):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, text)
        
        # Scroll to bottom
        GLib.idle_add(self.scroll_to_bottom)
        
    def scroll_to_bottom(self):
        adj = self.text_view.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_send(self, entry):
        text = entry.get_text().strip()
        if not text and not self.attached_image:
            return
            
        entry.set_text("")
        self.append_text(f"You: {text if text else '[Attached Image]'}\n\n")
        
        if not HAS_GENAI or not self.api_key:
            self.append_text("System: API Key missing or library not installed.\n\n")
            return
            
        self.spinner.start()
        self.entry.set_sensitive(False)
        
        img_buffer = self.attached_image
        self.attached_image = None
        
        # Run in thread to not block GTK
        threading.Thread(target=self.generate_response, args=(text, img_buffer), daemon=True).start()

    def generate_response(self, prompt, img_buffer=None):
        try:
            from google.genai import types
            
            contents = []
            if img_buffer:
                part = types.Part.from_bytes(data=img_buffer, mime_type='image/png')
                contents.append(part)
            if prompt:
                contents.append(prompt)
                
            response = self.client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=contents,
            )
            reply = response.text
        except Exception as e:
            reply = f"Error: {e}"
            
        GLib.idle_add(self.on_response_ready, reply)

    def on_response_ready(self, reply):
        self.append_text(f"Gemini: {reply}\n\n")
        self.spinner.stop()
        self.entry.set_sensitive(True)
        self.entry.grab_focus()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
            return True
        elif event.keyval == Gdk.KEY_v and (event.state & Gdk.ModifierType.CONTROL_MASK):
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            if clipboard.wait_is_image_available():
                pixbuf = clipboard.wait_for_image()
                if pixbuf:
                    success, buffer = pixbuf.save_to_bufferv("png", [], [])
                    if success:
                        self.attached_image = buffer
                        self.append_text("System: 📎 Image attached from clipboard!\n\n")
        return False

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
            background-color: alpha(@surface, 0.85);
            border-radius: 20px;
            border: 2px solid alpha(@outline, 0.5);
        }
        #MainBox {
            padding: 20px;
            background-color: transparent;
        }
        #ScrollArea {
            background-color: transparent;
        }
        #ChatOutput, #ChatOutput text {
            background-color: transparent;
            color: @on_surface;
            font-family: "JetBrains Mono";
            font-size: 14px;
        }
        #InputBox {
            margin-top: 15px;
            background-color: transparent;
        }
        #ChatInput {
            padding: 12px;
            border-radius: 12px;
            background-color: alpha(@surface_variant, 0.5);
            color: @on_surface;
            font-size: 15px;
            border: 1px solid alpha(@outline, 0.3);
            box-shadow: none;
        }
        """

        combined_css = colors_css + "\n" + custom_css
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(combined_css.encode('utf-8'))
        screen = Gdk.Screen.get_default()
        context = Gtk.StyleContext()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

if __name__ == "__main__":
    app = AIChatPopup()
    app.show_all()
    app.entry.grab_focus()
    Gtk.main()
