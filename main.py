"""
Put together all the display elements and render to the display.

TODO: cava binary pipe
TODO: check font licence
TODO: scrolling LMS text?
TODO: kid's pixel art
"""

from time import time
from datetime import datetime
from time import sleep
from itertools import cycle

import display
from display import Image, ImageChops, ImageOps, ImageEnhance
import cava
import schemes
import clock
from colors import *


font = "pf_tempesta_seven_compressed.ttf"
clock_font = "fonts/" + font
clock_size = 8
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
FADE_CLOCK = True
# 0.05 works well at 120fps
AFTERIMAGE_ALPHA = 0.05
CLOCK_COLOR = AMBER
CLOCK_HZ = 10
SCHEME_SWITCH_TIMER = 900
CAVA_CONFIG_TIMER = 1
SCROLL_SPEED = 4
BG = True
BG_ALPHA = 0.2


if __name__ == "__main__":

    # ---- WELCOME SCREEN ---- #
    bg = display.open("images/rainbow_mountains.jpg")
    display.render(bg)
    sleep(1)

    cava_frame = display.blank()
    f = display.blank()
    timers = [0] * 5
    cava_ps = cava.start()

    while True:
        t = time()
        f_last = f

        # ---- CAVA ---- #
        cava_frame_last = cava_frame
        # blocking to framerate set by cava
        l, r, is_mute = cava.read_bars(cava_ps.stdout)
        cava_frame = cava.frame(l, r, scheme=SCHEME)
        cava_frame = Image.blend(cava_frame_last, cava_frame, AFTERIMAGE_ALPHA)

        # ---- UPDATE TIMERS ---- #
        if t - timers[0] >= 1.0 / CLOCK_HZ:
            timers[0] = t

            # ---- TIME OF DAY BRIGHTNESS ---- #
            now = datetime.now()
            # fade is lowest at 3am, highest 3pm
            fade = (abs(now.hour + now.minute / 60 + now.second / 3600 - 3) % 24) / 24.0
            display.brightness(0.10 + 0.9*fade)

            # ---- CLOCK ---- #
            c = clock.now(clock_font, size=clock_size)
            c = display.tint(c, CLOCK_COLOR)
            
            c = display.add(display.blank(), c, dy=13 - clock_size)
            cbg = display.add(display.blank(), bg)
            c = Image.blend(cbg, c, BG_ALPHA)

        if t - timers[1] >= SCHEME_SWITCH_TIMER:
            timers[1] = t
            SCHEME = next(SCHEMES)

        if t - timers[2] >= CAVA_CONFIG_TIMER:
            timers[2] = t
            cava.reload_config(cava_ps)

        if t - timers[3] >= 1.0 / SCROLL_SPEED:
            timers[3] = t

        # ---- COMPOSE AND RENDER ---- #
        if FADE_CLOCK and not is_mute:
            f = cava_frame
        else:
            f = ImageChops.lighter(cava_frame, c)
        display.render_changes(f, f_last)

