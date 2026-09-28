#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <cstdio>

struct Browser {
    std::string name;
    std::string icon;
    std::string exec;
};

bool command_exists(const std::string& cmd) {
    std::string check_cmd = "which " + cmd + " >/dev/null 2>&1";
    return (std::system(check_cmd.c_str()) == 0);
}

int main() {
    std::vector<Browser> browsers = {
        {"Helium Browser", "helium", "helium"},
        {"Zen Browser", "zen-browser", "zen-browser"},
        {"Firefox", "firefox", "firefox"},
        {"Google Chrome", "google-chrome", "google-chrome-stable"},
        {"Brave Browser", "brave-browser", "brave-browser"},
        {"Chromium", "chromium", "chromium"}
    };

    std::string wofi_input;
    std::vector<Browser> available;

    for (const auto& b : browsers) {
        if (command_exists(b.exec)) {
            available.push_back(b);
            wofi_input += "img:" + b.icon + ":text:\\n";
        }
    }

    if (available.empty()) {
        (void)std::system("notify-send 'Browser Menu' 'No supported web browser found.'");
        return 0;
    }

    int count = available.size();
    int width = count * 56 + 20;
    int height = 64;

    std::string cmd = "printf \"" + wofi_input + "\" | wofi --dmenu --allow-images --columns " + std::to_string(count) + " --lines 1 --prompt \"\" --width " + std::to_string(width) + " --height " + std::to_string(height) + " --style /home/ravindra/.config/wofi/browser_menu.css 2>/dev/null";
    
    FILE* pipe = popen(cmd.c_str(), "r");
    if (!pipe) return 1;

    char buffer[256];
    std::string result;
    if (fgets(buffer, sizeof(buffer), pipe) != NULL) {
        result = buffer;
    }
    pclose(pipe);

    while (!result.empty() && (result.back() == '\n' || result.back() == '\r' || result.back() == ' ')) {
        result.pop_back();
    }

    if (result.empty()) return 0;

    for (const auto& b : available) {
        std::string formatted = "img:" + b.icon + ":text:";
        if (result == formatted || result.find(b.icon) != std::string::npos) {
            std::string launch = b.exec + " >/dev/null 2>&1 &";
            (void)std::system(launch.c_str());
            break;
        }
    }

    return 0;
}
