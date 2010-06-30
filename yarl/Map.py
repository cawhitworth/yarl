import math
import Block
import Entity
import Imp

class Map:
    def __init__(self, dimensions, appearance):
        self.size = dimensions
        self.data = [ ]
        self.appearance = appearance
        for x in range(dimensions[0]):
            self.data.append( [] )
            for y in range(dimensions[1]):
                self.data[x].append(Block.Dirt(appearance))

        self.addDungeonHeart((20, 14))
        self.imps = []
        self.imps.append(Imp.Imp(appearance, self, (20,13)))
        self.imps.append(Imp.Imp(appearance, self, (20,15)))
        self.imps.append(Imp.Imp(appearance, self, (19,14)))
        self.imps.append(Imp.Imp(appearance, self, (21,14)))


    def addDungeonHeart(self, location):
        self.dungeonHeart = Entity.DungeonHeart(self.appearance, self, location)
        
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
