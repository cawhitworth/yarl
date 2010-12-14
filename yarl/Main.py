import pygame
import sys
import os
import platform
import random
import logging

from settings import *
from Colors import *
import CharMap
import CharMapAppearance as Appearance
import Map
import Jobs
import Entity
import Imp

class YARL:
    def __init__(self):
        self.gameComponents = []

        self.entityManager = Entity.Manager(self)
        self.map = Map.Map(self, mapSize, Appearance.AddAppearance)        
        self.jobManager = Jobs.Manager(self)
        
        self.gameComponents.append(self.entityManager)
        self.gameComponents.append(self.map)
        self.gameComponents.append(self.jobManager)
        
        
        drivers = [SDL_VIDEODRIVER]
        
        if platform.system() == "Windows":
            drivers.append("windib")
            drivers.append("directx")
        if platform.system() == "Linux":
            drivers.append("x11")
            drivers.append("fbcon")

        driver = self.initPygame(drivers)

        if driver == None:
            logging.error("Unable to initialise a video driver")
            sys.exit()

        if driver != SDL_VIDEODRIVER:
            logging.warn("Unable to initialise video driver '%s' - using '%s' instead", SDL_VIDEODRIVER, driver)

        transparent = pygame.Color( transparentColor )
        self.charMap = CharMap.CharMap(self, tileSet, transparent)

        self.screenSize = map(lambda x,y:x*y, self.charMap.charSize, screenSizeInTiles)
        
        self.screen = pygame.display.set_mode(self.screenSize)

        self.mapOrigin = [ 0, 0 ]

        self.characterPos = tuple(map(lambda x: x/2, screenSizeInTiles))
        self.cursorMapPos = map(lambda a,b:a+b, self.characterPos, self.mapOrigin) 
        self.cursorChar = ord('X')
        self.cursorColor = Colors.color(BRIGHT, RED)
        
        self.clock = pygame.time.Clock()
        self.r = random.Random()

        self.running = True
        pygame.key.set_repeat(keyDelay, keyRepeat)

        self.map.addDungeonHeart((20, 14))
        self.imps = []
        self.imps.append(Imp.Imp(self, Appearance.AddAppearance, self, (20,13)))
        self.imps.append(Imp.Imp(self, Appearance.AddAppearance, self, (20,15)))
        self.imps.append(Imp.Imp(self, Appearance.AddAppearance, self, (19,14)))
        self.imps.append(Imp.Imp(self, Appearance.AddAppearance, self, (21,14)))


    def mapRect(self, origin):
        (x,y) = origin

        return (x, y, x + mapRenderSize[0], y + mapRenderSize[1] )

    def initPygame(self, drivers):
        for driver in drivers:
            os.environ['SDL_VIDEODRIVER'] = driver
            (_,fail) = pygame.init()
            if fail == 0:
                return driver
        return None



    def main(self):
        while self.running:
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.handleKey(event.key)

            for component in self.gameComponents:
                component.update(self.clock.get_time())


            self.screen.fill(pygame.Color(0,0,0,0))
            
            self.charMap.renderMapSegment( self.screen, self.map, (0,0), self.mapRect(self.mapOrigin) )
            self.charMap.drawChar(self.cursorChar, self.screen, gridpos=self.characterPos, color=self.cursorColor)

            self.drawStats()
            
            pygame.display.flip()
    
    def drawStats(self):
        fps = self.clock.get_fps()
        mapx, mapy = map(lambda a, b:a + b, self.characterPos, self.mapOrigin)
        y = 1
        if self.map.data[mapx][mapy].visibility < 2:
            self.charMap.writeString("[hidden]", self.screen, gridpos=(61, y))
            y += 1
        else:
            self.charMap.writeString(self.map.data[mapx][mapy].description, self.screen, gridpos=(61, y))
            y += 1
            for entity in self.map.data[mapx][mapy].entities:
                self.charMap.writeString(entity.description, self.screen, gridpos=(61, y))
                y += 1
        
        self.charMap.writeString("FPS %s" % int(fps), self.screen, gridpos=(61, 24))
        self.charMap.writeString("%s" % self.cursorMapPos, self.screen, gridpos=(61, y))
        y += 1
        for job in self.jobManager.jobsAt(self.cursorMapPos):
            self.charMap.writeString(job.description, self.screen, gridpos=(61, y))
            y += 1

    
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
        self.cursorMapPos = map(lambda a,b:a+b, self.characterPos, self.mapOrigin) 


    def toggleJob(self, jobType, location):
        (x,y) = location
        if not self.map.data[x][y].visibility > 1:
            return

        job = self.jobManager.popJobOfTypeAt(jobType, location)

        if job != None:
            job.cancelled = True
        else:
            self.jobManager.newJob(jobType, location)
            
    def toggleDig(self, position):
        (x,y) = position
        if not self.map.data[x][y].canHaveJob(Jobs.EXCAVATE):
            return
        if not self.map.data[x][y].visibility > 1:
            return

        job = self.jobManager.popJobOfTypeAt(Jobs.EXCAVATE, position)
        if job != None:
            job.cancelled = True
        else:
            self.jobManager.newJob(Jobs.EXCAVATE, position)
        

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
        elif key == controls["excavate"]:
            self.toggleJob(Jobs.EXCAVATE, self.cursorMapPos)
        elif key == controls["smooth"]:
            self.toggleJob(Jobs.SMOOTH, self.cursorMapPos)
        elif key == controls["dumpstatus"]:
            self.jobManager.dump()





def main():
    yarl = YARL()
    yarl.main()
