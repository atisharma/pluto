"""
Update the PHAT with rendered text or cava data.
The PHAT state is stored as a PIL image, with im[x, y] = (R, G, B).
The image size is accessed as im.size = (w, h).
Images can be superposed.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
import unicornhathd as uh


# hack the update frequency, otherwise we can't keep up with cava.
# this is safe since sys.stdin.readline() is blocking.
uh._DELAY = 0.0


def blank():
    """
    A blank image of the right size for the display.
    """
    w, h = uh.get_shape()
    image = Image.new("RGB", (w, h), color=0)
    return image


def brightness(b):
    """
    Set display brightness in [0, 1].
    """
    uh.brightness(b)


def text(text, font, height):
    """
    Render text to an image in a given font.
    """
    # Create font
    pil_font = ImageFont.truetype(font, size=height, encoding="unic")
    text_width, text_height = pil_font.getsize(text)
    width = text_width
    # create a blank canvas with extra space between lines
    image = Image.new("RGB", [width, height], (255, 255, 255))
    # draw the text onto the canvas
    draw = ImageDraw.Draw(image)
    offset = ((width - text_width) // 2, (height - text_height) // 2 - 1)
    bg = "#000000"
    draw.text(offset, text, font=pil_font, fill=bg)
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    return ImageOps.invert(image)


def tint(image, color):
    """
    Apply a tint to an image.
    """
    return ImageChops.multiply(image, Image.new('RGB', image.size, color))


def add(image, overlay, dx=0, dy=0):
    """
    Overlay an image over another one.
    """
    ow, oh = overlay.size
    iw, ih = image.size
    pixels = image.load()
    ov = overlay.load()
    for ox in range(ow):
        for oy in range(oh):
            ix, iy = ox + dx, oy + dy
            if 0 <= ix < iw and 0 <= iy < ih:
                o = ov[ox, oy]
                p = pixels[ix, iy]
                pixels[ix, iy] = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
    return image


def peak(image):
    """
    Return the peak brightness of all pixels.
    """
    r, g, b = image.split()
    rlow, rhigh = r.getextrema()
    glow, ghigh = g.getextrema()
    blow, bhigh = b.getextrema()
    return max(rhigh, ghigh, bhigh)


def render(image):
    """
    Update the display with a new image.
    The buffer is a 16x16x3 numpy array, uh._buf.
    """
    xm, ym = uh.get_shape()
    for xy, pixel in zip(range(xm * ym), image.getdata()):
        x = xy // xm
        y = xy % xm
        uh.set_pixel(x, y, pixel[0], pixel[1], pixel[2])
    uh.show()


def render_changes(image, old_image):
    """
    Update the display only where it has changed.
    """
    xm, ym = uh.get_shape()
    for xy, pixel, old_pixel in zip(range(xm * ym), image.getdata(), old_image.getdata()):
        x = xy // xm
        y = xy % xm
        if pixel != old_pixel:
            uh.set_pixel(x, y, pixel[0], pixel[1], pixel[2])
    uh.show()
