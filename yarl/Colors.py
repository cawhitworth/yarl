from settings import *

BLACK=0
WHITE=1
RED=2
GREEN=3
BLUE=4
YELLOW=5
CYAN=6
MAGENTA=7
BROWN=8
GREY=9

NORMAL=0
DARK=1
BRIGHT=2

class Colors:
    baseColors = [
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (1.0, 1.0, 0.0),
        (0.0, 1.0, 1.0),
        (1.0, 0.0, 1.0),
        (0.8, 0.5, 0.0),
        (0.5, 0.5, 0.5)
    ]

    baseColorsBW = [
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0)
    ]

    brightnessMult = [ 0.66, 0.33, 1.0 ]

    @staticmethod
    def colors():
        c = []
        baseColors = Colors.baseColors
        if blackandwhite:
            baseColors = Colors.baseColorsBW
        for brightness in Colors.brightnessMult:
            for color in baseColors:
                col = [ int(channel * brightness *255) for channel in color ]
                colStr = "#" + "".join(["%02x" % channel for channel in col])
                c.append(colStr)
        return c

    @staticmethod
    def color(brightness, col):
        if blackandwhite:
            if col == BLACK:
                return 0
            else:
                return brightness * len(Colors.baseColorsBW) + 1
        return brightness * len(Colors.baseColors) + col

    @staticmethod
    def darken(brightness):
        if brightness == BRIGHT:
            return NORMAL
        elif brightness == NORMAL:
            return DARK
