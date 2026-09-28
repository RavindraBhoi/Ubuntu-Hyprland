#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>

struct Shortcut {
    std::string keys;
    std::string desc;
};

int main() {
    std::vector<Shortcut> shortcuts = {
        {"SUPER + RETURN / T", "Open Terminal (Kitty)"},
        {"SUPER + SPACE", "App Launcher"},
        {"SUPER + B", "Web Browser Selector"},
        {"SUPER + E", "File Manager"},
        {"SUPER + F", "Search Files"},
        {"SUPER + A", "AI Chat Assistant"},
        {"SUPER + SHIFT + C", "Control Center"},
        {"SUPER + SHIFT + F", "Toggle Fullscreen"},
        {"SUPER + V", "Toggle Window Float"},
        {"SUPER + Q", "Close Window"},
        {"SUPER + SHIFT + P", "Restart Waybar & Wob Daemon"},
        {"SUPER + SHIFT + Q", "Logout / Power Menu"},
        {"SUPER + L", "Lock Screen"},
        {"SUPER + PRINT", "Take Screenshot"},
        {"SUPER + 1..9", "Switch Workspace"},
        {"SUPER + SHIFT + 1..9", "Move Window to Workspace"}
    };

    std::string wofi_input;
    for (const auto& s : shortcuts) {
        wofi_input += s.keys + "  ➔  " + s.desc + "\\n";
    }

    std::string cmd = "echo -e \"" + wofi_input + "\" | wofi --dmenu --prompt \"⌨ Keyboard Shortcuts\" --width 520 --height 460 --style ~/.config/wofi/shortcuts.css 2>/dev/null";
    (void)std::system(cmd.c_str());

    return 0;
}
