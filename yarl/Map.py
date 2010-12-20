import math
import Block
import Entity
import Imp
from GameComponent import GameComponent
from threading import Lock

class Map(GameComponent):
    def __init__(self, game, dimensions, appearance):
        GameComponent.__init__(self, game)
        self.size = dimensions
        self._data = [ ]
        self.appearance = appearance
        for x in range(dimensions[0]):
            self._data.append( [] )
            for y in range(dimensions[1]):
                self._data[x].append(Block.Dirt(appearance))

        self._datalock = Lock()

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
                    self._data[x][y] = Block.LavaMoat(self.appearance)
                elif d < 4:
                    self._data[x][y] = Block.StoneFloor(self.appearance)
                elif d < 6:
                    self._data[x][y] = Block.DirtFloor(self.appearance)
                elif d == 6:
                    self._data[x][y] = Block.RoughWall(self.appearance)

                if d > 10 and d < 15:
                    self._data[x][y].visibility = 1
                elif d > 3 and d <= 10:
                    self._data[x][y].visibility = 2
                elif d <= 3:
                    self._data[x][y].visibility = 3

        self._data[cx][cy].entities.append(self.dungeonHeart)

    # This function works on the basis that our entire map must be connected
    # Thus, if any square has empty space next to it, it must be routeable from
    # any other point on the map

    def lock(self, blocking = True):
        acquired = self._datalock.acquire(blocking)
        if acquired:
            return self._data
        else:
            return None
    
    def unlock(self):
        self._datalock.release()
    
    def isPassable(self, loc):
        return self.block(loc).isPassable()
    
    def moveEntity(self, entity, to):
        map = self.lock()
        (x,y) = entity.location
        block = map[x][y]
        if entity in block.entities:
            block.entities.remove(entity)
        (x,y) = to
        block = map[x][y]
        block.entities.append(entity)
        self.unlock()
        
        entity.location = to

    def block(self, loc, lock = True):
        (x,y) = loc
        if lock:
            map = self.lock()
            block = map[x][y]
            self.unlock()
            return block
        else:
            return self._data[x][y]

    def setBlock(self, loc, block):
        (x,y) = loc
        map = self.lock()
        map[x][y] = block
        self.unlock()
        
    def setVisibility(self, loc, vis):
        (x,y) = loc
        map = self.lock()
        map[x][y].visibility = vis
        self.unlock()        

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
                if self.isPassable( (x,y) ):
                    return True
        return False


