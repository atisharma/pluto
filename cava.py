"""
Read fifo socket for cava's raw output, and construct a virtual image to update
the display with.

A S Sharma 2020
"""

import select
import subprocess
import signal

from display import blank, Image
import schemes


MAX_BAR_HEIGHT = 65536


def start():
    """
    Start the cava subprocess.
    """
    cava_ps = subprocess.Popen(['cava'], stdout=subprocess.PIPE, text=True)
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
    Returns left heights, right heights, is_mute.
    """
    # avoid blocking
    i, o, e = select.select( [stdin], [], [], 1.0 / 30.0)
    if i:
        ascii_bars = stdin.readline()
    else:
        return [0] * 16, [0] * 16, True
    try:
        heights = list(map(cleaner, ascii_bars.strip().split(';')[:-1]))
    except ValueError:
        return [0] * 16, [0] * 16, True
    bars = len(heights)
    left = [h for h in heights[0:bars // 2]]
    right = [h for h in heights[bars:bars // 2 - 1:-1]]
    is_quiet = sum(heights) < 1e-4     # -80db
    return left, right, is_quiet


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

