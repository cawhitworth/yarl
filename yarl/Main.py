import pygame
import sys
import os
import platform
import random

from settings import *
import CharMap

def main():
    pygame.init()

    transparent = pygame.Color( transparentColor )
    charMap = CharMap.CharMap(tileSet, transparent)

    screenSize = (charMap.charSize[0] * screenSizeInTiles[0],
                  charMap.charSize[1] * screenSizeInTiles[1])

    screen = pygame.display.set_mode(screenSize)

    characterPos = (0,0)

    clock = pygame.time.Clock()

    r = random.Random()

    while 1:
        clock.tick()
        fps = clock.get_fps()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(pygame.Color(0,0,0,0))
        greens = ( Colors.color(DARK, GREEN), Colors.color(NORMAL, GREEN), Colors.color(BRIGHT, GREEN))
        for y in range(0, screenSizeInTiles[1]):
            for x in range(0, screenSizeInTiles[0]):
                c = greens[(x+y)%3]
                charMap.drawChar(ord('.'), screen, gridpos = (x,y), color=c)
        charMap.drawChar(ord('@'), screen, gridpos=characterPos, color=2)
    #    charMap.writeString("Hello world!", screen, gridpos=(0,1))

        charMap.writeString("FPS %s" % int(fps),  screen, gridpos=(0,2), blank = True)

        pygame.display.flip()

