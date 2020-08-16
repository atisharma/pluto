"""
Return an image of the current time.

A S Sharma 2020.
"""

from datetime import datetime

import display


def now(font, size=6, fmt="%H%M", tint=(255, 255, 255)):
    """
    The current time as an image.
    """
    timestr = datetime.now().strftime(fmt)
    image = display.text(timestr, font, size) 
    image = display.tint(image, tint)
    image = display.add(display.blank(), image, dy=13 - size)
    return image

