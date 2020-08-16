"""
Cava display colour schemes.
"""

from colors import *


def _rg_phosphor(x, y, lh, rh, H, rgb):
    """
    Colour scheme with rg tint.
    """
    lv = int((0.55 * lh + 0.45 * rh) * (H - 1))
    rv = int((0.45 * lh + 0.55 * rh) * (H - 1))
    v = int((rh + lv) * (H - 1) / 2)
    r = rgb[0] if y < lv else 0
    g = rgb[1] if y < rv else 0
    b = rgb[2] if y < v else 0
    return r, g, b


def rg(x, y, lh, rh, H):
    """
    Colour scheme with red and green for L and R channels, and blue for height.
    """
    lv = int(lh * (H - 1))
    rv = int(rh * (H - 1))
    r = 255 if y < lv else 0
    g = 255 if y < rv else 0
    b = (lv + rv - 2 * y) * 8
    return r, g, b


def green_phosphor(x, y, lh, rh, H):
    """
    Colour scheme with a green tint (approximates P1 phosphor).
    """
    return _rg_phosphor(x, y, lh, rh, H, (65, 255, 0))


def amber_phosphor(x, y, lh, rh, H):
    """
    Colour scheme with amber tint (approximates P3 phosphor).
    """
    return _rg_phosphor(x, y, lh, rh, H, (255, 165, 0))


def orange_phosphor(x, y, lh, rh, H):
    """
    Colour scheme with orange tint (approximates P19 phosphor).
    """
    return _rg_phosphor(x, y, lh, rh, H, (255, 220, 0))


def blue_phosphor(x, y, lh, rh, H):
    """
    Colour scheme with orange tint (approximates P11 phosphor).
    """
    lv = int((0.55 * lh + 0.45 * rh) * (H - 1))
    rv = int((0.45 * lh + 0.55 * rh) * (H - 1))
    v = int((rh + lv) * (H - 1) / 2)
    r = 100 if y < lv else 0
    g = 0
    b = 255 if y < rv else 0
    return r, g, b


def blue_yellow_phosphor(x, y, lh, rh, H):
    """
    Colour scheme with blue and yellow afterimage (approximates P7 phosphor).
    """
    lv = int((0.55 * lh + 0.45 * rh) * (H - 1))
    rv = int((0.45 * lh + 0.55 * rh) * (H - 1))
    v = int(max(rh, lv) * (H - 1))
    h = int(64 * (lh + rh) * (H / 5 - y))
    blue = (60, 0, 255)
    yellow = (105, 128, 0)
    if y < max(lv, rv):
        r, g, b = (int(p * (lv - y)/16 + q * (H-rv+y)/16) for p, q in zip(yellow, blue))
    else:
        r, g, b = 0, 0, 0
    return r, g, b


def fire(x, y, lh, rh, H):
    """
    Colour scheme that looks like fire.
    """
    lv = int(lh * (H - 1))
    rv = int(rh * (H - 1))
    r = 225 if y < lv else 0
    g = 88 if y < lv else 0
    b = int(64 * (lh + rh) * (H / 5 - y))
    return r, g, b


def kitt(x, y, lh, rh, H):
    """
    Colour scheme remeniscent of Kitt from Knight Rider.
    """
    r = int(128 * (lh + rh)) if y == 0 else 0
    g = 0
    b = 0
    return r, g, b


def discreet(x, y, lh, rh, H):
    """
    A discreet scheme based on kitt.
    """
    if y == 0:
        r = int(225 * lh)
        g = int(88 * rh)
        b = int(20 * (lh + rh))
    else:
        r, g, b = 0, 0, 0
    return r, g, b


def split_pulse(x, y, lh, rh, H):
    """
    Colour scheme which pulses from the sides.
    """
    lv = int(lh * (H - 1))
    rv = int(rh * (H - 1))
    r = int(128 * lh * (H / 5 - y))
    g = int(44 * lh * (H / 5 - y))
    b = int(255 * rh * (H / 5 + y - H))
    return r, g, b

