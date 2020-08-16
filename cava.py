"""
Read fifo socket for cava's raw output, and construct a virtual image to update
the display with.

A S Sharma 2020
"""

import sys
import select

from display import blank, Image


MAX_BAR_HEIGHT = 65536


def cleaner(h):
    """
    Return an int from an ascii bar.
    """
    return min(int('0' if h == '' else h), MAX_BAR_HEIGHT - 1)


def read_bars():
    """
    Read cava ascii bar heights from stdin.
    Cava config should set:
        raw_target = /dev/stdout
        data_format = ascii
        bar_delimiter = 59
        frame_delimiter = 10
        ascii_max_range = 65535 # (1 less than MAX_BAR_HEIGHT)
    """
    # avoid blocking
    i, o, e = select.select( [sys.stdin], [], [], 1.0 / 30.0)
    if (i):
        ascii_bars = sys.stdin.readline()
    else:
        return [0] * 16, [0] * 16
    try:
        heights = list(map(cleaner, ascii_bars.strip().split(';')[:-1]))
    except ValueError:
        return [0] * 16, [0] * 16
    bars = len(heights)
    left = heights[0:bars // 2]
    right = heights[bars:bars // 2 - 1:-1]
    return left, right


def frame(left, right):
    """
    Render bar heights to an image.
    """
    im = blank()
    H, W = im.size
    r, g, b = im.split()
    # pixel access objects
    rp, gp, bp = r.load(), g.load(), b.load()
    for x, h in enumerate(left):
        v = min(H-1, int(h * (H - 1) / MAX_BAR_HEIGHT))
        for y in range(v):
            rp[x, y] = 255
            bp[x, y] = (v - y) * 8
    for x, h in enumerate(right):
        v = min(H-1, int(h * (H - 1) / MAX_BAR_HEIGHT))
        for y in range(v):
            gp[x, y] = 255
            bp[x, y] = bp[x, y] + (v - y) * 8
    return Image.merge('RGB', (r, g, b))
