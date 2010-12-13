import math
import Block
import Entity
import Imp
from GameComponent import GameComponent

class Map(GameComponent):
    def __init__(self, game, dimensions, appearance):
        GameComponent.__init__(self, game)
        self.size = dimensions
        self.data = [ ]
        self.appearance = appearance
        for x in range(dimensions[0]):
            self.data.append( [] )
            for y in range(dimensions[1]):
                self.data[x].append(Block.Dirt(appearance))

    def update(self, time):
        pass
    
    def addDungeonHeart(self, location):
        self.dungeonHeart = Entity.DungeonHeart(self.game, self.appearance, location)
        
        (cx,cy) = location

        for x in range(cx-20, cx+20):
            if x < 0 or x > self.size[0]:
                continue
            for y in range(cy-20, cy+20):
                if y < 0 or y > self.size[1]:
                    continue
                d = int(math.sqrt(math.pow(float(x - cx), 2.0) +
                                  math.pow(float(y - cy), 2.0)))
                if x != cx and y != cy and (d == 2 or d == 3):
                    self.data[x][y] = Block.LavaMoat(self.appearance)
                elif d < 4:
                    self.data[x][y] = Block.StoneFloor(self.appearance)
                elif d < 6:
                    self.data[x][y] = Block.DirtFloor(self.appearance)
                elif d == 6:
                    self.data[x][y] = Block.RoughWall(self.appearance)

                if d > 10 and d < 15:
                    self.data[x][y].visibility = 1
                elif d > 3 and d <= 10:
                    self.data[x][y].visibility = 2
                elif d <= 3:
                    self.data[x][y].visibility = 3

        self.data[cx][cy].entities.append(self.dungeonHeart)

    # This function works on the basis that our entire map must be connected
    # Thus, if any square has empty space next to it, it must be routeable from
    # any other point on the map

    def isRouteable(self, loc):
        (cx,cy) = loc
        for dy in (-1,0,1):
            y = cy + dy
            if y < 0 or y >= self.size[1]:
                continue
            for dx in (-1,0,1):
                x = cx + dx
                if x < 0 or x >= self.size[0]:
                    continue
                if dx != 0 and dy != 0: # This can change once I lift the manhattan movement restriction
                    continue
                if dx == 0 and dy == 0:
                    continue
                if self.data[x][y].isPassable():
                    return True
        return False


