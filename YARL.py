import pygame
import sys
import numpy
import os
import platform
import random

from settings import *

class CharMap:
    def __init__(self, file, colorKey):
        self.image = pygame.image.load("data/tiles/%s" % file)
        self.size = self.image.get_size()
        self.charSize = (self.size[0]/16, self.size[1]/16)
        self.image.set_colorkey(colorKey)
        tempSurface = pygame.Surface(self.charSize, pygame.HWSURFACE)
        self.black = pygame.Surface(self.charSize, pygame.HWSURFACE)
        self.black.fill(pygame.Color(0,0,0,0))
        self.chars = []

        for char in range(0,255):
            self.chars.append([])
            for color in Colors.colors():
                c = pygame.Color(color)
                mapPos = ( (char % 16) * self.charSize[0],
                           (char / 16) * self.charSize[1] )
                mapRect = pygame.Rect(mapPos, self.charSize)

                tempSurface.fill(pygame.Color(0,0,0,0))
                tempSurface.blit(self.image, (0,0), mapRect)

                surfAr= pygame.surfarray.pixels3d(tempSurface)
                mul = numpy.array( [ float(c.r) / 255.0, float(c.g) / 255.0, float(c.b) / 255.0] )
                surfAr *= mul
                del(surfAr)
                surf = pygame.Surface(self.charSize, pygame.HWSURFACE)
                surf.blit(tempSurface, (0,0))
                surf.set_colorkey(pygame.Color(0,0,0,0))
                self.chars[char].append(surf)

    def drawChar(self, char, surface, gridpos = None, screenpos = None, color=1, blank = False):
        position = (0,0)
        if gridpos:
            position = ( gridpos[0] * self.charSize[0],
                         gridpos[1] * self.charSize[1] )
        else:
            position = screenpos

        if blank:
            surface.blit(self.black, position)
        surface.blit(self.chars[char][color], position)

    def writeString(self, string, surface, gridpos, color = 1, blank = False):
        for char in string:
            self.drawChar(ord(char), surface, gridpos = gridpos, color = color, blank = blank)
            gridpos = ( gridpos[0]+1, gridpos[1] )

pygame.init()

transparentColor = pygame.Color( transparentColor )
charMap = CharMap(tileSet, transparentColor)

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

