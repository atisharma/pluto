"""
Return an image of the current time.
"""

from datetime import datetime

from display import Image, text


def now(font, size=6, fmt="%H%M"):
    """
    The current time as an image.
    """
    timestr = datetime.now().strftime(fmt)
    t = text(timestr, font, size) 
    return t

