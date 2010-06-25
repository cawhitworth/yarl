import pygame
import sys
import os
import platform
import random

from settings import *
from Colors import *
import CharMap
import CharMapAppearance as Appearance
import Map

class YARL:
    def __init__(self):

        drivers = [SDL_VIDEODRIVER]
        
        if platform.system() == "Windows":
            drivers.append("directx")
            drivers.append("windib")

        driver = self.initPygame(drivers)

        if driver == None:
            print "Unable to initialise a video driver"
            sys.exit()

        if driver != SDL_VIDEODRIVER:
            print "Unable to initialise video driver '%s' - using '%s' instead" % (SDL_VIDEODRIVER, driver)

        transparent = pygame.Color( transparentColor )
        self.charMap = CharMap.CharMap(tileSet, transparent)

        self.screenSize = map(lambda x,y:x*y, self.charMap.charSize, screenSizeInTiles)
        
        self.screen = pygame.display.set_mode(self.screenSize)

        self.characterPos = tuple(map(lambda x: x/2, screenSizeInTiles))
        self.map = Map.Map(mapSize, Appearance.AddAppearance)

        self.mapOrigin = [ 0, 0 ]
        self.clock = pygame.time.Clock()

        self.r = random.Random()

        self.cursorChar = ord('X')
        self.cursorColor = Colors.color(BRIGHT, RED)
        self.running = True
        pygame.key.set_repeat(keyDelay, keyRepeat)

    def mapRect(self, origin):
        (x,y) = origin

        return (x, y, x + mapRenderSize[0], y + mapRenderSize[1] )

    def initPygame(self, drivers):
        for driver in drivers:
            os.environ['SDL_VIDEODRIVER'] = driver
            (ok,fail) = pygame.init()
            if fail == 0:
                return driver
        return None

    def main(self):
        while self.running:
            self.clock.tick()
            fps = self.clock.get_fps()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handleKey(event.key)

            self.screen.fill(pygame.Color(0,0,0,0))
            
            self.charMap.renderMapSegment( self.screen, self.map, (0,0), self.mapRect(self.mapOrigin) )
            self.charMap.drawChar(self.cursorChar, self.screen, gridpos=self.characterPos, color=self.cursorColor)

            self.charMap.writeString("FPS %s" % int(fps), self.screen, gridpos=(0,2), blank = True)
            self.charMap.writeString("Cursor %s" % ( map(lambda a,b:a+b, self.characterPos, self.mapOrigin) ), self.screen, gridpos=(0,3), blank=True)
            pygame.display.flip()
    
    def moveCharacter(self, direction):
        # Oh gods this is awful
        mods = pygame.key.get_mods()
        multiplier = 1
        if mods & controls["fastmove"]:
            multiplier = 5

        # So, if we're in the centre of the map, we can just move the cursor

        offset = [ d * multiplier for d in direction ]
        newPos = map(lambda x,y: x + y, self.characterPos, offset)

        if newPos[0] >= mapBorder and newPos[0] < mapRenderSize[0] - mapBorder and\
           newPos[1] >= mapBorder and newPos[1] < mapRenderSize[1] - mapBorder:
            self.moveTo(newPos)
        else:
            # If we're going to end up in the border, we try and move the map view by 
            # how much we're the border and bounce the cursor to the border edge

            mapShift = [0,0]

            # In left border
            if newPos[0] < mapBorder:
                if newPos[0] < self.characterPos[0]: # Only bump if we're moving left
                    self.mapOrigin[0] += offset[0]
                    if self.mapOrigin[0] < 0:
                        newPos[0] = self.characterPos[0] + self.mapOrigin[0]
                        self.mapOrigin[0] = 0
                    else:
                        newPos[0] = self.characterPos[0]

            # In right border
            if newPos[0] > mapRenderSize[0] - mapBorder:
                if newPos[0] > self.characterPos[0]: # Only bump if we're moving right
                    self.mapOrigin[0] += offset[0]
                    overspill = (self.mapOrigin[0] + mapRenderSize[0]) - mapSize[0]
                    if overspill > 0:
                        newPos[0] = self.characterPos[0] + overspill
                        self.mapOrigin[0] = mapSize[0] - mapRenderSize[0]
                    else:
                        newPos[0] = self.characterPos[0]

            # In top border
            if newPos[1] < mapBorder:
                if newPos[1] < self.characterPos[1]: # Only bump if we're moving up
                    self.mapOrigin[1] += offset[1]
                    if self.mapOrigin[1] < 0:
                        newPos[1] = self.characterPos[1] + self.mapOrigin[1]
                        self.mapOrigin[1] = 0
                    else:
                        newPos[1] = self.characterPos[1]

            # In bottom border
            if newPos[1] > mapRenderSize[1] - mapBorder:
                if newPos[1] > self.characterPos[1]: # Only bump if we're moving down
                    self.mapOrigin[1] += offset[1]
                    overspill = (self.mapOrigin[1] + mapRenderSize[1]) - mapSize[1]
                    if overspill > 0:
                        newPos[1] = self.characterPos[1] + overspill
                        self.mapOrigin[1] = mapSize[1] - mapRenderSize[1]
                    else:
                        newPos[1] = self.characterPos[1]

            self.moveTo(newPos)
                    
    def moveTo(self, destination):
        if destination[0] < 0:
            destination[0] = 0
        if destination[0] > mapRenderSize[0]-1:
            destination[0] = mapRenderSize[0]-1

        if destination[1] < 0:
            destination[1] = 0
        if destination[1] > mapRenderSize[1]-1:
            destination[1] = mapRenderSize[1]-1

        self.characterPos = destination


    def handleKey(self, key):
        if key == controls["quit"]:
            self.running = False
        elif key == controls["up"]:
            self.moveCharacter((0,-1))
        elif key == controls["down"]:
            self.moveCharacter((0,1))
        elif key == controls["left"]:
            self.moveCharacter((-1,0))
        elif key == controls["right"]:
            self.moveCharacter((1,0))



def main():
    yarl = YARL()
    yarl.main()
