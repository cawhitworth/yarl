import pygame
from Colors import *
import Jobs

surfArrayAvailable = True
try:
    import numpy
except:
    surfArrayAvailable = False
    print "Warning: numpy not installed; startup speed may be very slow"

from settings import *

class CharMap:
    def __init__(self, game, file, colorKey):
        self.game = game
        self.image = pygame.image.load("data/tiles/%s" % file)
        self.size = self.image.get_size()
        self.charSize = (self.size[0]/16, self.size[1]/16)
        self.image.set_colorkey(colorKey)
        tempSurface = pygame.Surface(self.charSize, pygame.HWSURFACE)
        self.black = pygame.Surface(self.charSize, pygame.HWSURFACE)
        self.black.fill(pygame.Color(0,0,0,0))
        self.highlight = pygame.Surface(self.charSize, pygame.HWSURFACE)
        self.highlight.fill(pygame.Color(200,200,0,0))
        self.chars = []
        self.renderRegion = None
        self.frame = 0
        self.drawFlashing = True

        count = 10
        print "Building tiles: ",
        for char in range(0,256):
            self.chars.append([])
            if char % 25 == 0:
                print "%s... " % count,
                count -= 1
            for color in Colors.colors():
                c = pygame.Color(color)
                mapPos = ( (char % 16) * self.charSize[0],
                           (char / 16) * self.charSize[1] )
                mapRect = pygame.Rect(mapPos, self.charSize)

                tempSurface.fill(pygame.Color(0,0,0,0))
                tempSurface.blit(self.image, (0,0), mapRect)

                if char >= 32 and char < 128:
                    if surfArrayAvailable:
                        surfAr= pygame.surfarray.pixels3d(tempSurface)
                        mul = numpy.array( [ float(c.r) / 255.0, float(c.g) / 255.0, float(c.b) / 255.0] )
                        surfAr *= mul
                        del(surfAr)
                    
                    else:
                        tempSurface.lock()
                        mul = ( float(c.r) / 255.0, float(c.g) / 255.0, float(c.b) / 255.0 )
                        for y in range(0, self.charSize[0]):
                            for x in range(0, self.charSize[1]):
                                pixel = tempSurface.get_at((x,y))
                                cl = (float(pixel.r), float(pixel.g), float(pixel.b))
                                pixel = [ int( cl[ch] * mul[ch] ) for ch in range(0,3) ]
                                tempSurface.set_at((x,y), pygame.Color(pixel[0], pixel[1], pixel[2], 0))
                        tempSurface.unlock()

                surf = pygame.Surface(self.charSize, pygame.HWSURFACE)
                surf.blit(tempSurface, (0,0))
                surf.set_colorkey(pygame.Color(0,0,0,0))
                self.chars[char].append(surf)

    def drawHighlight(self, surface, gridpos = None, screenpos = None):
        position = (0,0)
        if gridpos:
            position = ( gridpos[0] * self.charSize[0],
                         gridpos[1] * self.charSize[1] )
        else:
            position = screenpos
        
        surface.blit(self.highlight, position)

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

    def renderMapSegment(self, surface, map, origin, region):
        self.frame += 1
        if self.frame == 10:
            self.frame = 0
            self.drawFlashing = not self.drawFlashing

        (screenX,screenY) = origin
        if self.renderRegion != region:
            print region
            self.renderRegion = region
        for y in range(region[1], region[3]):
            screenX = origin[0]
            for x in range(region[0], region[2]):
                block = map.block( (x,y), False )

                if self.game.jobManager.sparseJobMap.has_key((x,y)):
                    highlight = 0
                    for job in self.game.jobManager.sparseJobMap[(x,y)]:
                        if job in self.game.jobManager.jobs:
                            highlight = 1
                        elif job in self.game.jobManager.inProgressJobs:
                            highlight = 2

                    if highlight == 1:
                        self.drawHighlight(surface, gridpos = (screenX, screenY))
                    elif highlight == 2 and self.drawFlashing:
                        self.drawHighlight(surface, gridpos = (screenX, screenY))


                if len(block.entities) > 0:
                    entity = block.entities[-1]
                    col = list(entity.appearance["color"])
                    char = entity.appearance["character"]
                    self.drawChar( char, surface, gridpos = (screenX, screenY),
                                   color = Colors.color(col[0], col[1]))
                else:
                    color = list(block.appearance["color"])
                    char = block.appearance["character"]

                    if block.visibility == 0:
                        screenX += 1
                        continue
                    elif block.visibility == 1:
                        color[0] = DARK
                        char = ord('.')
                    elif block.visibility == 2:
                        if color[0] == DARK:
                            screenX += 1
                            continue
                        color[0] = Colors.darken(color[0])

                    col = Colors.color(color[0], color[1])

                    self.drawChar( char, surface, gridpos = (screenX, screenY), 
                                   color = col )

                screenX += 1
            screenY += 1
