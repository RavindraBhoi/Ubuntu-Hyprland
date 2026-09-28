-- This is an example Hyprland Lua config file.
-- Refer to the wiki for more information.
-- https://wiki.hypr.land/Configuring/Start/

-- Please note not all available settings / options are set here.
-- For a full list, see the wiki

-- You can (and should!!) split this configuration into multiple files
-- Create your files separately and then require them like this:
-- require("myColors")

hl.exec_cmd("export GEMINI_API_KEY="YOUR_API_KEY_HERE"

-- Global workspace dispatcher helper for Waybar / hyprctl CLI
function _G.workspace(num)
    return hl.dsp.focus({ workspace = num })
end
------------------
---- MONITORS ----
------------------

-- See https://wiki.hypr.land/Configuring/Basics/Monitors/
hl.monitor({
    output   = "",
    mode     = "preferred",
    position = "auto",
    scale    = "1.25",
})


---------------------
---- MY PROGRAMS ----
---------------------

-- Set programs that you use
local terminal    = "/usr/bin/kitty"
local fileManager = "dolphin"
local menu        = "wofi --show drun"
-- Lock the screen and turn off the display. Wake up on mouse move or key press.
local lock = "sh -c 'pidof hyprlock || (hyprlock & sleep 0.5 && hyprctl dispatch dpms off)'"

-------------------
---- AUTOSTART ----
-------------------

-- See https://wiki.hypr.land/Configuring/Basics/Autostart/

-- Autostart necessary processes (like notifications daemons, status bars, etc.)
-- Or execute your favorite apps at launch like this:
--
hl.on("hyprland.start", function () 
  hl.exec_cmd("/home/ravindra/.config/hypr/wallpaper.sh")
  hl.exec_cmd("hypridle")
  hl.exec_cmd("nm-applet --indicator")
  hl.exec_cmd("wl-paste --type text --watch cliphist store")
  hl.exec_cmd("wl-paste --type image --watch cliphist store")
  hl.exec_cmd("bash /home/ravindra/.config/hypr/scripts/wob.sh")
  hl.exec_cmd("python3 /home/ravindra/.config/hypr/scripts/workspace_cava.py")
  hl.exec_cmd("python3 /home/ravindra/.config/hypr/scripts/notify_daemon.py")
  hl.exec_cmd("/home/ravindra/.config/hypr/scripts/bin/battery_notify")
  hl.exec_cmd("/home/ravindra/.config/hypr/scripts/bin/device_notify")
end)


-------------------------------
---- ENVIRONMENT VARIABLES ----
-------------------------------

-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Environment-variables/

hl.env("PATH", "/home/ravindra/bin:/home/ravindra/.local/bin:/usr/local/bin:/usr/bin:/bin")
hl.env("TERMINAL", "/usr/bin/kitty")
hl.env("XCURSOR_THEME", "Bibata-Modern-Ice")
hl.env("XCURSOR_SIZE", "24")
hl.env("HYPRCURSOR_THEME", "Bibata-Modern-Ice")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("QT_QPA_PLATFORMTHEME", "kde")
hl.env("QT_STYLE_OVERRIDE", "Breeze")
hl.env("QT_QPA_PLATFORM", "wayland;xcb")
hl.env("ELECTRON_OZONE_PLATFORM_HINT", "auto")


-----------------------
----- PERMISSIONS -----
-----------------------

-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Permissions/
-- Please note permission changes here require a Hyprland restart and are not applied on-the-fly
-- for security reasons

-- hl.config({
--   ecosystem = {
--     enforce_permissions = true,
--   },
-- })

-- hl.permission("/usr/(bin|local/bin)/grim", "screencopy", "allow")
-- hl.permission("/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland", "screencopy", "allow")
-- hl.permission("/usr/(bin|local/bin)/hyprpm", "plugin", "allow")


-----------------------
---- LOOK AND FEEL ----
-----------------------

-- Refer to https://wiki.hypr.land/Configuring/Basics/Variables/
local matugen_colors = pcall(dofile, os.getenv("HOME") .. "/.config/hypr/colors.lua") and dofile(os.getenv("HOME") .. "/.config/hypr/colors.lua") or { primary = "rgb(ffffff)", surface_variant = "rgb(444444)" }
hl.config({
    general = {
        gaps_in  = 5,
        gaps_out = 5,

        border_size = 2,

        col = {
            active_border   = matugen_colors.primary,
            inactive_border = matugen_colors.surface_variant,
        },

        -- Set to true to enable resizing windows by clicking and dragging on borders and gaps
        resize_on_border = false,

        -- Please see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Tearing/ before you turn this on
        allow_tearing = false,

        layout = "dwindle",
    },

    decoration = {
        rounding       = 12,
        rounding_power = 2,

        -- Change transparency of focused and unfocused windows
        active_opacity   = 1.0,
        inactive_opacity = 0.95,

        dim_inactive = true,
        dim_strength = 0.2,

        shadow = {
            enabled      = true,
            range        = 25,
            render_power = 4,
            color        = 0x99000000,
        },

        blur = {
            enabled   = true,
            size      = 8,
            passes    = 3,
            vibrancy  = 0.5,
        },
    },

    animations = {
        enabled = true,
    },
})

-- Default curves and animations, see https://wiki.hypr.land/Configuring/Advanced-and-Cool/Animations/
hl.curve("easeOutQuint",   { type = "bezier", points = { {0.23, 1},    {0.32, 1}    } })
hl.curve("easeInOutCubic", { type = "bezier", points = { {0.65, 0.05}, {0.36, 1}    } })
hl.curve("linear",         { type = "bezier", points = { {0, 0},       {1, 1}       } })
hl.curve("almostLinear",   { type = "bezier", points = { {0.5, 0.5},   {0.75, 1}    } })
hl.curve("quick",          { type = "bezier", points = { {0.15, 0},    {0.1, 1}     } })
hl.curve("macos",          { type = "bezier", points = { {0.25, 1},    {0.5, 1}     } })
hl.curve("overshot",       { type = "bezier", points = { {0.05, 0.9},  {0.1, 1.1}   } })

hl.animation({ leaf = "global",        enabled = true,  speed = 10,   bezier = "default" })
hl.animation({ leaf = "border",        enabled = true,  speed = 5.39, bezier = "easeOutQuint" })
hl.animation({ leaf = "windows",       enabled = true,  speed = 6,    bezier = "overshot",     style = "slide" })
hl.animation({ leaf = "windowsIn",     enabled = true,  speed = 6,    bezier = "overshot",     style = "slide" })
hl.animation({ leaf = "windowsOut",    enabled = true,  speed = 6,    bezier = "overshot",     style = "slide" })
hl.animation({ leaf = "fadeIn",        enabled = true,  speed = 1.73, bezier = "almostLinear" })
hl.animation({ leaf = "fadeOut",       enabled = true,  speed = 1.46, bezier = "almostLinear" })
hl.animation({ leaf = "layers",        enabled = true,  speed = 5,    bezier = "overshot" })
hl.animation({ leaf = "layersIn",      enabled = true,  speed = 5,    bezier = "overshot",     style = "fade" })
hl.animation({ leaf = "layersOut",     enabled = true,  speed = 5,    bezier = "overshot",     style = "fade" })
hl.animation({ leaf = "fadeLayersIn",  enabled = true,  speed = 1.79, bezier = "almostLinear" })
hl.animation({ leaf = "fadeLayersOut", enabled = true,  speed = 1.39, bezier = "almostLinear" })
hl.animation({ leaf = "workspaces",    enabled = true,  speed = 6,    bezier = "overshot",     style = "slide" })
hl.animation({ leaf = "workspacesIn",  enabled = true,  speed = 6,    bezier = "overshot",     style = "slide" })
hl.animation({ leaf = "workspacesOut", enabled = true,  speed = 6,    bezier = "overshot",     style = "slide" })

-- Ref https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/
-- "Smart gaps" / "No gaps when only"
-- uncomment all if you wish to use that.
-- hl.workspace_rule({ workspace = "w[tv1]", gaps_out = 0, gaps_in = 0 })
-- hl.workspace_rule({ workspace = "f[1]",   gaps_out = 0, gaps_in = 0 })
-- hl.window_rule({
--     name  = "no-gaps-wtv1",
--     match = { float = false, workspace = "w[tv1]" },
--     border_size = 0,
--     rounding    = 0,
-- })
-- hl.window_rule({
--     name  = "no-gaps-f1",
--     match = { float = false, workspace = "f[1]" },
--     border_size = 0,
--     rounding    = 0,
-- })

-- See https://wiki.hypr.land/Configuring/Layouts/Dwindle-Layout/ for more
hl.config({
    dwindle = {
        preserve_split = true, -- You probably want this
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Master-Layout/ for more
hl.config({
    master = {
        new_status = "master",
    },
})

-- See https://wiki.hypr.land/Configuring/Layouts/Scrolling-Layout/ for more
hl.config({
    scrolling = {
        fullscreen_on_one_column = true,
    },
})

----------------
----  MISC  ----
----------------

hl.config({
    misc = {
        force_default_wallpaper = -1,    -- Set to 0 or 1 to disable the anime mascot wallpapers
        disable_hyprland_logo   = false, -- If true disables the random hyprland logo / anime girl background. :(
        mouse_move_enables_dpms = true,  -- Automatically wake up display on mouse move
        key_press_enables_dpms  = true,  -- Automatically wake up display on key press
    },
})

hl.config({
    xwayland = {
        force_zero_scaling = true,
    },
})


---------------
---- INPUT ----
---------------

hl.config({
    input = {
        kb_layout  = "us",
        kb_variant = "",
        kb_model   = "",
        kb_options = "",
        kb_rules   = "",

        follow_mouse = 1,
        natural_scroll = true,

        sensitivity = 0, -- -1.0 - 1.0, 0 means no modification.

        touchpad = {
            natural_scroll = true,
        },
    },
})

hl.gesture({
    fingers = 3,
    direction = "horizontal",
    action = "workspace"
})

-- Example per-device config
-- See https://wiki.hypr.land/Configuring/Advanced-and-Cool/Devices/ for more
hl.device({
    name        = "epic-mouse-v1",
    sensitivity = -0.5,
})


---------------------
---- KEYBINDINGS ----
---------------------

local mainMod = "SUPER" -- Sets "Windows" key as main modifier

-- Example binds, see https://wiki.hypr.land/Configuring/Basics/Binds/ for more
hl.bind(mainMod .. " + RETURN", hl.dsp.exec_cmd(terminal))
hl.bind(mainMod .. " + T", hl.dsp.exec_cmd(terminal))
local closeWindowBind = hl.bind(mainMod .. " + C", hl.dsp.window.close())
-- closeWindowBind:set_enabled(false)
hl.bind(mainMod .. " + Q", hl.dsp.window.close())
hl.bind(mainMod .. " + SHIFT + Q", hl.dsp.exec_cmd("wlogout --layout /home/ravindra/.config/wlogout/layout --css /home/ravindra/.config/wlogout/style.css -b 3"))
hl.bind(mainMod .. " + SHIFT + C", hl.dsp.exec_cmd("python3 /home/ravindra/.config/hypr/scripts/control_center.py"))
hl.bind(mainMod .. " + M", hl.dsp.exec_cmd("command -v hyprshutdown >/dev/null 2>&1 && hyprshutdown || hyprctl dispatch 'hl.dsp.exit()'"))
hl.bind(mainMod .. " + E", hl.dsp.exec_cmd(fileManager))
hl.bind(mainMod .. " + B", hl.dsp.exec_cmd("python3 /home/ravindra/.config/hypr/scripts/browser_menu.py"))
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + A", hl.dsp.exec_cmd("python3 /home/ravindra/.config/hypr/scripts/ai_chat.py"))
hl.bind(mainMod .. " + SPACE", hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + F", hl.dsp.exec_cmd("python3 /home/ravindra/.config/hypr/scripts/wofi_file_search.py"))
hl.bind(mainMod .. " + SHIFT + F", hl.dsp.exec_cmd("hyprctl dispatch fullscreen 0"))
hl.bind(mainMod .. " + P", hl.dsp.window.pseudo())
hl.bind(mainMod .. " + SHIFT + P", hl.dsp.exec_cmd("bash /home/ravindra/.config/hypr/scripts/restart_desktop.sh"))
hl.bind(mainMod .. " + SHIFT + W", hl.dsp.exec_cmd("/home/ravindra/.config/hypr/wallpaper.sh"))
hl.bind(mainMod .. " + J", hl.dsp.layout("togglesplit"))    -- dwindle only
hl.bind(mainMod .. " + L", hl.dsp.exec_cmd(lock))
hl.bind(mainMod .. " + SHIFT + N", hl.dsp.exec_cmd("bash /home/ravindra/.config/hypr/scripts/toggle_bar.sh"))
hl.bind(mainMod .. " + PRINT", hl.dsp.exec_cmd("bash /home/ravindra/.config/hypr/scripts/screenshot.sh"))
hl.bind("CTRL + SHIFT + ESCAPE", hl.dsp.exec_cmd("kitty --class htop-popup -e htop"))
hl.bind(mainMod .. " + ESCAPE", hl.dsp.exec_cmd("kitty --class htop-popup -e htop"))

-- Move focus with mainMod + arrow keys
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down" }))

-- Resize windows with mainMod + SHIFT + arrow keys
hl.bind(mainMod .. " + SHIFT + right", hl.dsp.window.resize({ x = 30, y = 0, relative = true }), { repeating = true })
hl.bind(mainMod .. " + SHIFT + left",  hl.dsp.window.resize({ x = -30, y = 0, relative = true }), { repeating = true })
hl.bind(mainMod .. " + SHIFT + up",    hl.dsp.window.resize({ x = 0, y = -30, relative = true }), { repeating = true })
hl.bind(mainMod .. " + SHIFT + down",  hl.dsp.window.resize({ x = 0, y = 30, relative = true }), { repeating = true })

-- Switch workspaces with mainMod + [0-9]
-- Move active window to a workspace with mainMod + SHIFT + [0-9]
for i = 1, 10 do
    local key = i % 10 -- 10 maps to key 0
    hl.bind(mainMod .. " + " .. key,             hl.dsp.focus({ workspace = i}))
    hl.bind(mainMod .. " + SHIFT + " .. key,     hl.dsp.window.move({ workspace = i }))
end

-- Example special workspace (scratchpad)
hl.bind(mainMod .. " + S",         hl.dsp.workspace.toggle_special("magic"))
hl.bind(mainMod .. " + SHIFT + S", hl.dsp.window.move({ workspace = "special:magic" }))

-- Go to next empty workspace
hl.bind(mainMod .. " + D", hl.dsp.focus({ workspace = "empty" }))

-- Scroll through existing workspaces with mainMod + scroll
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))

-- Move/resize windows with mainMod + LMB/RMB and dragging
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(),   { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+ && wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{print int($2 * 100)}' > /tmp/wobpipe"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%- && wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{print int($2 * 100)}' > /tmp/wobpipe"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle && (wpctl get-volume @DEFAULT_AUDIO_SINK@ | grep -q MUTED && echo 0 > /tmp/wobpipe || wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk '{print int($2 * 100)}' > /tmp/wobpipe)"),     { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("brightnessctl -e4 -n2 -m set 5%+ | awk -F, '{print substr($4, 1, length($4)-1)}' > /tmp/wobpipe"),                  { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("brightnessctl -e4 -n2 -m set 5%- | awk -F, '{print substr($4, 1, length($4)-1)}' > /tmp/wobpipe"),                  { locked = true, repeating = true })

-- Requires playerctl
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("playerctl next"),       { locked = true })
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("playerctl play-pause"), { locked = true })
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("playerctl previous"),   { locked = true })


--------------------------------
---- WINDOWS AND WORKSPACES ----
--------------------------------

-- See https://wiki.hypr.land/Configuring/Basics/Window-Rules/
-- and https://wiki.hypr.land/Configuring/Basics/Workspace-Rules/

-- Example window rules that are useful

local suppressMaximizeRule = hl.window_rule({
    -- Ignore maximize requests from all apps. You'll probably like this.
    name  = "suppress-maximize-events",
    match = { class = ".*" },

    suppress_event = "maximize",
})
-- suppressMaximizeRule:set_enabled(false)

hl.window_rule({
    -- Fix some dragging issues with XWayland
    name  = "fix-xwayland-drags",
    match = {
        class      = "^$",
        title      = "^$",
        xwayland   = true,
        float      = true,
        fullscreen = false,
        pin        = false,
    },

    no_focus = true,
})

-- Layer rules also return a handle.
-- local overlayLayerRule = hl.layer_rule({
--     name  = "no-anim-overlay",
--     match = { namespace = "^my-overlay$" },
--     no_anim = true,
-- })
-- overlayLayerRule:set_enabled(false)

-- Hyprland-run windowrule
hl.window_rule({
    name  = "move-hyprland-run",
    match = { class = "hyprland-run" },

    move  = "20 monitor_h-120",
    float = true,
})

hl.window_rule({
    name  = "zenity-calendar",
    match = { class = "zenity" },
    float = true,
    move = "40% 5%",
    pin = true,
})

-- VPN Menu Rules
hl.window_rule({
    name = "vpn-menu-popup",
    match = { title = "vpn-menu-popup" },
    float = true,
    pin = true,
    move = "100%-290 40",
})

-- Blur Wlogout Background
-- Control Center Rules
hl.window_rule({
    name = "control-center-popup",
    match = { class = "dms-control-center" },
    float = true,
    pin = true,
    move = "1066 50",
    border_size = 2,
    focus_on_activate = true,
})

-- Blur Wlogout Background
hl.exec_cmd("hyprctl keyword layerrule 'blur,logout_dialog'")

hl.window_rule({
    name  = "float-nm-connection-editor",
    match = { class = "nm-connection-editor" },

    float = true,
})

hl.window_rule({
    name = "float-pavucontrol",
    match = { class = "pavucontrol" },
    float = true,
})

hl.window_rule({
    name = "float-ai-chat",
    match = { title = "ai-chat-popup" },
    float = true,
    size = "700 500",
    center = true,
    animation = "popin",
})

hl.window_rule({
    name = "float-htop",
    match = { class = "htop-popup" },
    float = true,
    size = "950 600",
    center = true,
    focus_on_activate = true,
})

hl.window_rule({
    name = "float-browser-select",
    match = { title = "browser-select-popup" },
    float = true,
    center = true,
    pin = true,
    animation = "popin",
    border_size = 0,
})

hl.window_rule({
    name = "float-shortcuts-popup",
    match = { title = "shortcuts-popup" },
    float = true,
    center = true,
    pin = true,
    animation = "popin",
    border_size = 0,
})

hl.exec_cmd("hyprctl keyword layerrule 'blur,ai-chat-popup'")
hl.exec_cmd("hyprctl keyword layerrule 'blur,global-search'")
hl.exec_cmd("hyprctl keyword layerrule 'ignorezero,global-search'")
hl.exec_cmd("hyprctl keyword layerrule 'animation slide top,global-search'")

hl.window_rule({
    name  = "float-blueman-manager",
    match = { class = "blueman-manager" },
    float = true,
})

-- ML4W Float Apps
hl.window_rule({ name = "float-fileroller", match = { class = "file-roller" }, float = true, center = true })
hl.window_rule({ name = "float-calc", match = { class = "qalculate-gtk" }, float = true, center = true })
hl.window_rule({ name = "float-gnome-calc", match = { class = "org.gnome.Calculator" }, float = true, center = true })
hl.window_rule({ name = "float-xdg", match = { class = "xdg-desktop-portal-gtk" }, float = true, center = true })
hl.window_rule({ name = "float-polkit", match = { class = "polkit-gnome-authentication-agent-1" }, float = true, center = true })
hl.window_rule({ name = "float-onlyoffice-dialog", match = { class = "DesktopEditors" }, float = true, center = true })


-- Picture in Picture (Browsers)
hl.window_rule({ name = "global-search", match = { title = "global-search" }, float = true, pin = true, move = "50%-w/2 0%" })
hl.window_rule({ name = "pip-ff", match = { title = "Picture-in-Picture" }, float = true, pin = true })
hl.window_rule({ name = "pip-ff-pos", match = { title = "Picture-in-Picture" }, move = "100%-w-20 20", size = "30% 30%" })
hl.window_rule({ name = "pip-ch", match = { title = "Picture in picture" }, float = true, pin = true })

-- Opacity / Transparency Settings
hl.window_rule({ name = "opacity-kitty",  match = { class = "kitty" },       opacity = "0.95 0.90" })
hl.window_rule({ name = "opacity-wofi",   match = { class = "wofi" },        opacity = "0.90 0.90", border_size = 0 })
hl.window_rule({ name = "opacity-signal", match = { class = "signal" },      opacity = "1.0 1.0 override" })

-- Google Calendar popup window rules
hl.window_rule({ name = "gcal-popup", match = { class = "gcal-popup" }, float = true, pin = true })
hl.window_rule({ name = "browser-menu-popup", match = { class = "browser-menu-popup" }, float = true, center = true, focus_on_activate = true, border_size = 0 })
hl.window_rule({ name = "hypr-notification", match = { class = "hypr-notification" }, float = true, pin = true, move = "1160 45", border_size = 0, rounding = 8 })

-- Blur the wofi app launcher background
hl.layer_rule({ name = "blur-wofi", match = { namespace = "wofi" }, blur = true })



