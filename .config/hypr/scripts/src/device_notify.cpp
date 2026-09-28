#include <iostream>
#include <fstream>
#include <string>
#include <set>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <filesystem>

namespace fs = std::filesystem;

void play_sound(const std::string& sound_name) {
    std::string cmd = "canberra-gtk-play -i " + sound_name + " >/dev/null 2>&1 &";
    (void)std::system(cmd.c_str());
}

void send_notification(const std::string& summary, const std::string& body, const std::string& icon = "drive-removable-media") {
    std::string cmd = "notify-send -i " + icon + " \"" + summary + "\" \"" + body + "\" >/dev/null 2>&1 &";
    (void)std::system(cmd.c_str());
}

std::set<std::string> get_usb_devices() {
    std::set<std::string> devices;
    std::string usb_dir = "/sys/bus/usb/devices";
    if (fs::exists(usb_dir)) {
        for (const auto& entry : fs::directory_iterator(usb_dir)) {
            fs::path product_path = entry.path() / "product";
            if (fs::exists(product_path)) {
                std::ifstream f(product_path);
                if (f.is_open()) {
                    std::string name;
                    std::getline(f, name);
                    if (!name.empty()) {
                        devices.insert(entry.path().filename().string() + ":" + name);
                    }
                }
            }
        }
    }
    return devices;
}

int main() {
    std::set<std::string> known_devices = get_usb_devices();

    while (true) {
        std::set<std::string> current_devices = get_usb_devices();

        // New devices added
        for (const auto& dev : current_devices) {
            if (known_devices.find(dev) == known_devices.end()) {
                size_t pos = dev.find(':');
                std::string dev_name = (pos != std::string::npos) ? dev.substr(pos + 1) : "Device";
                play_sound("device-added");
                send_notification("Device Connected 🔌", dev_name + " has been connected.");
            }
        }

        // Devices removed
        for (const auto& dev : known_devices) {
            if (current_devices.find(dev) == current_devices.end()) {
                size_t pos = dev.find(':');
                std::string dev_name = (pos != std::string::npos) ? dev.substr(pos + 1) : "Device";
                play_sound("device-removed");
                send_notification("Device Removed 🔌", dev_name + " has been disconnected.");
            }
        }

        known_devices = current_devices;
        std::this_thread::sleep_for(std::chrono::seconds(2));
    }

    return 0;
}
