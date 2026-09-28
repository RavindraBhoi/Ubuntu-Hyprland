# Ubuntu Hyprland Dotfiles (Waybar Only)

This repository contains my personal Hyprland configuration for Ubuntu, featuring a clean aesthetic with Waybar.

## Requirements

The installation assumes you are running Ubuntu 24.04 (Noble Numbat) or newer.

## Installation Instructions

1. **Update and Upgrade System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Core Dependencies & Packages**
   ```bash
   sudo apt install -y \
       git curl wget unzip tar \
       wl-clipboard jq fzf ripgrep \
       kitty wofi thunar btop \
       network-manager-gnome \
       brightnessctl \
       playerctl \
       xwayland \
       kde-cli-tools
   ```

3. **Install Hyprland and Waybar (via PPA for Ubuntu)**
   It's recommended to use the official PPA or compile from source to get the latest Hyprland on Ubuntu.
   ```bash
   sudo add-apt-repository ppa:hyprland/releases
   sudo apt update
   sudo apt install -y hyprland waybar
   ```

4. **Install Rust and Cargo Tools (for dynamic theming)**
   Matugen is used for dynamic theming based on wallpapers.
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source "$HOME/.cargo/env"
   cargo install matugen
   ```

5. **Deploy the Dotfiles**
   Clone this repository and copy the configurations:
   ```bash
   git clone git@github.com:RavindraBhoi/Ubuntu-Hyprland.git ~/Ubuntu-Hyprland
   cp -r ~/Ubuntu-Hyprland/.config/* ~/.config/
   ```

6. **Configure Gemini API (Optional but recommended)**
   In `~/.config/hypr/hyprland.lua`, locate the `export GEMINI_API_KEY="..."` line and replace `"YOUR_API_KEY_HERE"` with your actual API key if you want to use Gemini integration.

## Usage
Log out of your current session, and from your Display Manager (like GDM or SDDM), select "Hyprland" to log in.
