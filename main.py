"""
Put together all the display elements and render to the display.

TODO: cava binary pipe
TODO: check font licence
TODO: scrolling LMS text?
TODO: kid's pixel art

A S Sharma 2020.
"""

from time import time
from datetime import datetime
from time import sleep
from itertools import cycle
import configparser
import json

import display
from display import Image, ImageChops, ImageOps, ImageEnhance
import cava
import schemes
import clock
from colors import *


SCHEMES = cycle([
    schemes.rg,
    schemes.fire,
    schemes.kitt,
    schemes.blue_yellow_phosphor,
    schemes.blue_phosphor,
    schemes.green_phosphor,
    schemes.orange_phosphor,
    schemes.amber_phosphor,
    schemes.split_pulse
    ])
SCHEME = next(SCHEMES)


def configure():
    """
    Load the configuration options.
    """
    config = configparser.ConfigParser()
    config.read("cava.config")
    clock_font = config["pluto"].get("clock_font", "fonts/pf_tempesta_seven_compressed.ttf")
    clock_size = config["pluto"].getint("clock_size", 8)
    configuration = {
        "clock_font" : clock_font,
        "clock_color" : tuple(json.loads(config["pluto"].get("clock_color", "(255, 255, 255)"))),
        "clock_size" : clock_size,
        "clock_hz" : config["pluto"].getfloat("clock_hz", 30),
        "fade_clock" : config["pluto"].getboolean("fade_clock", True),
        "clock_blend_alpha" : config["pluto"].getfloat("clock_blend_alpha", 0.00001),
        "text_font" : config["pluto"].get("text_font", clock_font),
        "text_color" : tuple(json.loads(config["pluto"].get("text_color", "(255, 255, 255)"))),
        "text_size" : config["pluto"].getint("text_size", 8),
        "scroll_speed" : config["pluto"].getfloat("scroll_speed", 4),
        "afterimage_alpha" : config["pluto"].getfloat("afterimage_alpha", 0.05),
        "scheme_switch_timer" : config["pluto"].getfloat("scheme_switch_timer", 900),
        "cava_config_timer" : config["pluto"].getfloat("cava_config_timer", 1),
        "splash_screen" : config["pluto"].get("splash_screen")
        }
    cava.MAX_BAR_HEIGHT = config["output"].get("ascii_range_max", 2 ** 16)
    return configuration


def welcome(cfg):
    image = display.text(" Pluto   ", cfg["text_font"], cfg["text_size"]) 
    image = display.tint(image, cfg["text_color"])
    return image


def splash_screen(cfg):
    bg = display.open(cfg["splash_screen"])
    display.render(bg)
    sleep(5)
    display.render(f)


if __name__ == "__main__":

    cfg = configure()
    f = display.blank()
    timers = [0] * 5

    # ---- WELCOME SCREEN ---- #
    if cfg["splash_screen"]:
        splash_screen(cfg)

    welcome_image = welcome(cfg)
    t0 = time()
    while time() < t0 + 10:
        t = time()
        if t - timers[4] >= 1.0 / cfg["scroll_speed"]:
            timers[4] = t
            welcome_image = display.cycle(welcome_image)
            image = display.add(display.blank(), welcome_image, dy=3)
            display.render(image)
    display.clear()

    # ---- CAVA PROCESS AND FRAMES ---- #
    cava_frame = display.blank()
    c = display.blank()
    blank = display.blank()
    cava_ps = cava.start()

    while True:
        t = time()
        f_last = f
        c_last = c

        # ---- CAVA ---- #
        cava_frame_last = cava_frame
        # blocking to framerate set by cava
        l, r, is_playing = cava.read_bars(cava_ps.stdout)
        cava_frame = cava.frame(l, r, scheme=SCHEME)
        cava_frame = Image.blend(cava_frame_last, cava_frame, cfg["afterimage_alpha"])

        # ---- UPDATE TIMERS ---- #
        if t - timers[0] >= 1.0 / cfg["clock_hz"]:
            timers[0] = t

            # ---- TIME OF DAY BRIGHTNESS ---- #
            now = datetime.now()
            # fade is lowest at 3am, highest 3pm
            fade = (abs(now.hour + now.minute / 60 + now.second / 3600 - 3) % 24) / 24.0
            display.brightness(0.10 + 0.9*fade)

            # ---- CLOCK ---- #
            if cfg["fade_clock"] and is_playing:
                c = Image.blend(c_last, blank, cfg["clock_blend_alpha"])
            else:
                c = clock.now(cfg["clock_font"], size=cfg["clock_size"], tint=cfg["clock_color"])
                c = Image.blend(c_last, c, cfg["afterimage_alpha"])

        if t - timers[1] >= cfg["scheme_switch_timer"]:
            timers[1] = t
            SCHEME = next(SCHEMES)

        if t - timers[2] >= cfg["cava_config_timer"]:
            timers[2] = t
            cava.reload_config(cava_ps)
            cfg = configure()

        if t - timers[3] >= 1.0 / cfg["scroll_speed"]:
            timers[3] = t

        # ---- COMPOSE AND RENDER ---- #
        f = ImageChops.lighter(cava_frame, c)
        display.render_changes(f, f_last)

