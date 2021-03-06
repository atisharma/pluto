"""
Read fifo socket for cava's raw output, and construct a virtual image to update
the display with.

Copyright 2020 A S Sharma.
"""

import select
import subprocess
import signal
import os

from display import blank, Image
import schemes


MAX_BAR_HEIGHT = 65536


def start():
    """
    Start the cava subprocess.
    """
    cwd = os.path.dirname(os.path.realpath(__file__))
    config_file = f"{cwd}/cava.config"
    print("Starting cava with", config_file)
    cava_ps = subprocess.Popen(f"/usr/local/bin/cava -p {config_file}", shell=True, stdout=subprocess.PIPE, text=True, cwd=cwd)
    return cava_ps


def reload_config(ps):
    """
    Send a signal to cava to reload the config file.
    """
    ps.send_signal(signal.SIGUSR1)


def cleaner(h):
    """
    Return an int from an ascii bar.
    """
    return 0 if h == '' else float(h) / MAX_BAR_HEIGHT


def read_bars(stdin):
    """
    Read cava ascii bar heights from cava subprocess' stdout, or sys.stdin.
    Cava config should set:
        raw_target = /dev/stdout
        data_format = ascii
        bar_delimiter = 59
        frame_delimiter = 10
        ascii_max_range = 65535 # (1 less than MAX_BAR_HEIGHT)
    Returns left heights, right heights, is_playing.
    """
    # avoid blocking
    i, o, e = select.select( [stdin], [], [], 1.0 / 30.0)
    if i:
        ascii_bars = stdin.readline()
    else:
        return [0] * 16, [0] * 16, False
    try:
        heights = list(map(cleaner, ascii_bars.strip().split(';')[:-1]))
        bars = len(heights)
        left = [h for h in heights[0:bars // 2]]
        right = [h for h in heights[bars:bars // 2 - 1:-1]]
        is_playing = max(heights) > 2e-2
        return left, right, is_playing
    except ValueError:
        # occasional glitch and also null input
        return [0] * 16, [0] * 16, False


def frame(left, right, scheme=schemes.rg):
    """
    Render bar heights to an image.
    """
    image = blank()
    H, W = image.size
    pixels = image.load()
    for x, (lh, rh) in enumerate(zip(left, right)):
        for y in range(H):
            r, g, b = scheme(x, y, lh, rh, H)
            pixels[x, y] = r, g, b
    return image

