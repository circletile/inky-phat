from . import il91874
from . import fonts

try:
    from PIL import Image, ImageFont, ImageDraw
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")


__version__ = "0.0.1"

WHITE = 0
BLACK = 1
RED = 2

WIDTH = 212
HEIGHT = 104

_image = Image.new('P', (WIDTH, HEIGHT))

_draw = ImageDraw.Draw(_image)

_panel = il91874.IL91874(resolution=(HEIGHT, WIDTH), h_flip=False, v_flip=True)

_panel.set_palette((il91874.WHITE, il91874.BLACK, il91874.RED))

# Export drawing methods into the module namespace
for method in ["arc", "bitmap", "chord", "draw", "ellipse", "fill", "font", "fontmode", "getfont", "im", "ink", "line", "mode", "palette", "pieslice", "point", "polygon", "rectangle", "setfill", "setfont", "setink", "shape", "text", "textsize"]:
    globals()[method] = getattr(_draw, method)

# Selectively export image methods into the module namespace
for method in ["paste", "putpixel", "getpixel"]:
    globals()[method] = getattr(_image, method)

def set_partial_mode(x1,x2,y1,y2):
    _panel.set_partial_mode(y1,y2,x1,x2)

clear_partial_mode = _panel.clear_partial_mode

def create_mask(source, mask=(WHITE, BLACK, RED)):
    """Create a transparency mask.

    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.

    :param mask: Optional list of Inky pHAT colours to allow.

    """

    # Create a new 1bpp (on/off) mask image
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            # Mask out just the inkyphat colours we want to show
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image

def set_rotation(r):
    """Set rotation.

    :param r: Rotation in degrees, can be either 0 or 180

    """
    if r == 180:
        _panel.h_flip = True
        _panel.v_flip = False
    else:
        _panel.h_flip = False
        _panel.v_flip = True

def set_border(col):
    """Set panel border colour.

    :param col: Colour to set, should be one of WHITE, BLACK or RED.

    """

    _panel.set_border(col)

def set_image(image):
    """Replace buffer with an image.

    :param image: A valid PIL image, or an image filename

    """

    if isinstance(image, str):
        image = Image.open(image)

    if hasattr(image, 'getpixel'):
        _image.paste(image)

def get_image():
    """Get the image buffer."""

    return _image

def show():
    """Display the current buffy on Inky pHAT."""

    for y in range(WIDTH):
        for x in range(HEIGHT):
            _panel.set_pixel(x, y, _image.getpixel((y, x)))

    _panel.update()


