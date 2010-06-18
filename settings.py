tileSet = "Mkv_solidcurses_960x300.png"
screenSizeInTiles = (80, 25)
transparentColor = "#ff00ff"

BLACK=0
WHITE=1
RED=2
GREEN=3
BLUE=4
YELLOW=5
CYAN=6
MAGENTA=7
BROWN=8

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
        (0.8, 0.5, 0.0)
    ]

    brightnessMult = [ 0.66, 0.33, 1.0 ]

    @staticmethod
    def colors():
        c = []
        for brightness in Colors.brightnessMult:
            for color in Colors.baseColors:
                col = [ int(channel * brightness *255) for channel in color ]
                colStr = "#" + "".join(["%02x" % channel for channel in col])
                c.append(colStr)
        return c

    @staticmethod
    def color(brightness, col):
        return brightness * len(Colors.baseColors) + col
