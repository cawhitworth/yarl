import pygame
import sys
import os
import platform
import random

from settings import *
from Colors import *
import CharMap

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

        self.screenSize = (self.charMap.charSize[0] * screenSizeInTiles[0],
                           self.charMap.charSize[1] * screenSizeInTiles[1])

        self.screen = pygame.display.set_mode(self.screenSize)

        self.characterPos = (0,0)

        self.clock = pygame.time.Clock()

        self.r = random.Random()

        self.running = True
        pygame.key.set_repeat(keyDelay, keyRepeat)

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
            greens = ( Colors.color(DARK, GREEN), Colors.color(NORMAL, GREEN), Colors.color(BRIGHT, GREEN))
            for y in range(0, screenSizeInTiles[1]):
                for x in range(0, screenSizeInTiles[0]):
                    c = greens[(x+y)%3]
                    self.charMap.drawChar(ord('.'), self.screen, gridpos = (x,y), color=c)
            self.charMap.drawChar(ord('@'), self.screen, gridpos=self.characterPos, color=2)

            self.charMap.writeString("FPS %s" % int(fps), self.screen, gridpos=(0,2), blank = True)

            pygame.display.flip()
    
    def moveCharacter(self, direction):
        mods = pygame.key.get_mods()
        multiplier = 1
        if mods & controls["fastmove"]:
            multiplier = 5
        newPos = [ self.characterPos[0] + direction[0] * multiplier, 
                   self.characterPos[1] + direction[1] * multiplier]
        if newPos[0] < 0:
            newPos[0] = 0
        if newPos[0] > screenSizeInTiles[0]-1:
            newPos[0] = screenSizeInTiles[0]-1

        if newPos[1] < 0:
            newPos[1] = 0
        if newPos[1] > screenSizeInTiles[1]-1:
            newPos[1] = screenSizeInTiles[1]-1

        self.characterPos = newPos

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
