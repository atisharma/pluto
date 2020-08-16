"""
Put together all the display elements and render to the display.

TODO: add to git repo, push
TODO: cava binary pipe
TODO: check font licence
TODO: scrolling LMS text?
TODO: kid's pixel art
TODO: cava subprocess rather than call as a pipe
"""

from time import time
from datetime import datetime
from math import log2

import display
from display import Image, ImageChops
import cava
import clock


# image.putdata(data, scale, offset)
# image.paste(im, box)
# image.getdata() # flat iterator
# image.blend(im1, im2, alpha)

## many bitmap-inspired fonts expect 8 height
#font = "uni05_63.ttf"           # excellent at 8
#font = "Apple ][.ttf"           # excellent
#font = "A Goblin Appears!.otf"  # good even at 6
#font = "PressStart2P.ttf"
#font = "earthbound-beginnings.ttf"  # super clear
#font = "ABSTRACT.TTF"           # super clear, uppercase
#font = "04B_03__.TTF"
#font = "Tinier.ttf"             # legible at 4px!
#font = "prstartk.ttf"
#font = "goodbyeDespair.ttf"     # v clean all-caps
#font = "Diary of an 8-bit mage.otf"
#font = "Code 7x5.ttf"           # excellent
#font = "zx-spectrum.ttf"
#font = "Minitel.ttf"            # excellent monospaced
#font = "casio-fx-115es-plus.ttf"
#font = "uni05_53.ttf"           # excellent at 8; unicode
#font = "pf_tempesta_seven.ttf"  # really excellent; unicode, use this!
font = "pf_tempesta_seven_compressed.ttf"
clock_font = "fonts/" + font
clock_size = 8

if __name__ == "__main__":
    f = display.blank()
    cava_frame = display.blank()
    t_last = 0
    while True:
        t = time()
        f_last = f

        # ---- CAVA ---- #
        cava_frame_last = cava_frame
        # blocking to framerate set by cava
        l, r = cava.read_bars()
        cava_frame = cava.frame(l, r)
        # 0.05 works well with 120fps
        cava_frame = Image.blend(cava_frame_last, cava_frame, 0.05)

        # ---- UPDATE EVERY PERIOD ---- #
        if t - t_last >= 1.0 / 30:
            t_last = t

            # ---- TIME OF DAY ---- #
            now = datetime.now()
            # fade is lowest at 3am
            fade = (abs(now.hour + now.minute / 60 + now.second / 3600 - 3) % 24) / 24.0
            display.brightness(0.1 + 0.8 * fade)

            # ---- CLOCK ---- #
            c = clock.now(clock_font, size=clock_size)
            c = display.tint(c, (int(255 - fade * 255), int(fade * 128), int(fade * 255)))
            c = display.add(display.blank(), c, dy=14 - clock_size)
            # probably playing
            level = display.peak(cava_frame) ** 2 / 65025.0
            c = Image.blend(c, display.blank(), level)
            
        # ---- COMPOSE AND RENDER ---- #
        f = ImageChops.lighter(cava_frame, c)
        display.render_changes(f, f_last)

