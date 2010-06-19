from pygame import *

# Graphics settings

tileSet = "Mkv_solidcurses_960x300.png"
screenSizeInTiles = (80, 40)
transparentColor = "#ff00ff"

SDL_VIDEODRIVER = "windib"

# Keyboard configuration

controls = {
      "quit"    : K_ESCAPE,
      "left"    : K_LEFT,
      "right"   : K_RIGHT,
      "up"      : K_UP,
      "down"    : K_DOWN,
      "select"  : K_RETURN,

      "fastmove": KMOD_LSHIFT
    }

keyDelay = 250
keyRepeat = 100
