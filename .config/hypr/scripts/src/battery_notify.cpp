#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <unistd.h>
#include <sys/stat.h>

bool warned_20 = false;
bool warned_10 = false;
bool warned_full = false;
int last_state = -1;

void play_sound(const std::string& sound_name) {
    std::string cmd = "canberra-gtk-play -i " + sound_name + " >/dev/null 2>&1 &";
    std::system(cmd.c_str());
}

void send_notification(const std::string& summary, const std::string& body, const std::string& icon, const std::string& urgency) {
    std::string cmd = "notify-send -u " + urgency + " -i " + icon + " \"" + summary + "\" \"" + body + "\" >/dev/null 2>&1 &";
    std::system(cmd.c_str());
}

void get_battery_info(int& capacity, std::string& status, int& ac_online) {
    std::string cap_path = "/sys/class/power_supply/BAT1/capacity";
    std::string status_path = "/sys/class/power_supply/BAT1/status";
    std::string ac_path = "/sys/class/power_supply/ACAD/online";

    struct stat buffer;
    if (stat(cap_path.c_str(), &buffer) != 0) {
        cap_path = "/sys/class/power_supply/BAT0/capacity";
        status_path = "/sys/class/power_supply/BAT0/status";
    }

    if (stat(ac_path.c_str(), &buffer) != 0) {
        ac_path = "/sys/class/power_supply/AC/online";
    }

    capacity = 100;
    status = "Unknown";
    ac_online = 0;

    std::ifstream cap_file(cap_path);
    if (cap_file.is_open()) {
        cap_file >> capacity;
    }

    std::ifstream status_file(status_path);
    if (status_file.is_open()) {
        status_file >> status;
    }

    std::ifstream ac_file(ac_path);
    if (ac_file.is_open()) {
        ac_file >> ac_online;
    }
}

int main() {
    int capacity = 100;
    std::string status;
    int ac_online = 0;

    get_battery_info(capacity, status, ac_online);
    last_state = ac_online;

    while (true) {
        get_battery_info(capacity, status, ac_online);

        if (last_state != -1 && ac_online != last_state) {
            if (ac_online == 1) {
                play_sound("power-plug");
                send_notification("Charger Connected 🔌", "Power adapter plugged in (" + std::to_string(capacity) + "%). Charging...", "battery-charging", "normal");
                warned_20 = false;
                warned_10 = false;
            } else {
                play_sound("power-unplug");
                send_notification("Charger Disconnected 🔋", "Running on battery power (" + std::to_string(capacity) + "% remaining).", "battery-standard", "normal");
                warned_full = false;
            }
            last_state = ac_online;
        }

        if (ac_online == 0 || status == "Discharging") {
            if (capacity <= 10 && !warned_10) {
                send_notification("Critical Battery Level! ⚠️", "Battery is at " + std::to_string(capacity) + "%. Plug in your charger immediately!", "battery-caution", "critical");
                warned_10 = true;
                warned_20 = true;
            } else if (capacity <= 20 && !warned_20) {
                send_notification("Low Battery Warning 🪫", "Battery level dropped to " + std::to_string(capacity) + "%. Consider plugging in your charger.", "battery-low", "normal");
                warned_20 = true;
            }
        }

        if ((capacity >= 99 || status == "Full" || status == "Fully charged") && ac_online == 1) {
            if (!warned_full) {
                send_notification("Battery Fully Charged ⚡", "Battery is at 100%. You can safely unplug your charger.", "battery-full", "normal");
                warned_full = true;
            }
        } else {
            if (capacity < 95) {
                warned_full = false;
            }
        }

        std::this_thread::sleep_for(std::chrono::seconds(4));
    }

    return 0;
}
