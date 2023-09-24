#     ___  _   _ _         ____             __ _
#    / _ \| |_(_) | ___   / ___|___  _ __  / _(_) __ _
#   | | | | __| | |/ _ \ | |   / _ \| '_ \| |_| |/ _` |
#   | |_| | |_| | |  __/ | |__| (_) | | | |  _| | (_| |
#    \__\_\\__|_|_|\___|  \____\___/|_| |_|_| |_|\__, |
#                                                 |___/

# -----------------------------------------------------------------------------------------
#   IMPORTS
# -----------------------------------------------------------------------------------------

import os
import subprocess
from libqtile import hook
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# -----------------------------------------------------------------------------------------
#   USER OPTIONS
# -----------------------------------------------------------------------------------------

wmname = "QTILE"
mod = "mod4"
terminal = "kitty"
browser = "brave-browser"

# -----------------------------------------------------------------------------------------
#   Window Management Keys
# -----------------------------------------------------------------------------------------

keys = [

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes")
]


# -----------------------------------------------------------------------------------------
#   Keys
# -----------------------------------------------------------------------------------------
SpecialKeys = [
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.spawn("rofi -show drun -show-icons"), desc="Spawn a command using a prompt widget")
]

keys.extend(SpecialKeys)
# -----------------------------------------------------------------------------------------
#   Numbered Workspaces
# -----------------------------------------------------------------------------------------

groups = [Group(i) for i in "12345"]

for group in groups:
    keys.extend(
        [
            Key([mod],group.name,lazy.group[group.name].toscreen(),desc="Switch to group {}".format(group.name),),
            Key([mod, "shift"],group.name,lazy.window.togroup(group.name, switch_group=True),desc="Switch to & move focused window to group {}".format(group.name),),
        ]
    )

# -----------------------------------------------------------------------------------------
#   SCRATCHPADS
# -----------------------------------------------------------------------------------------

groups.append(ScratchPad("scratchpad", [

    DropDown("terminal", "kitty", x=0.125, y=0.125, width = 0.75, height = 0.75, on_focus_lost_hide = True),
    DropDown("browser", "google-chrome --app=https://chat.openai.com", x=0.125, y=0.125, width = 0.75, height = 0.75, on_focus_lost_hide = True),

    DropDown("mixer", "kitty alsamixer", x=0.125, y=0.125, width = 0.75, height = 0.75, on_focus_lost_hide = True),
    DropDown("pipegraph", "qpwgraph", x=0.125, y=0.125, width = 0.75, height = 0.75, on_focus_lost_hide = True)
]))

ScratchPadKeys = [
    Key([mod], "t", lazy.group["scratchpad"].dropdown_toggle("terminal")),
    Key([mod], "a", lazy.group["scratchpad"].dropdown_toggle("browser")),
    Key([mod], "m", lazy.group["scratchpad"].dropdown_toggle("mixer")),
    Key([mod, "shift"], "m", lazy.group["scratchpad"].dropdown_toggle("pipegraph"))
]

keys.extend(ScratchPadKeys)
# -----------------------------------------------------------------------------------------
#   LAYOUTS
# -----------------------------------------------------------------------------------------

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4, margin_on_single = 84, margin = 10),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=26,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        
        wallpaper="Pictures/Wallpapers/wallpaper.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(chords_colors={"launch": ("#ff0000", "#ffffff"),},name_transform=lambda name: name.upper(),),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%m-%d-%Y %a %I:%M %p"),
                widget.QuickExit(),
            ],
            40,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

# -----------------------------------------------------------------------------------------
#   CONFIGS
# -----------------------------------------------------------------------------------------

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
