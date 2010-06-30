import Entity
import random

r = random.Random()

class Imp(Entity.Entity):
    def __init__(self, appearance, map, location):
        Entity.Entity.__init__(self, Entity.IMP, "imp", appearance, map, location, passable = True)
        self.t = 0
        self.speed = 250
    
    def update(self, time):
        self.t += time
        if self.t < self.speed:
            return
        self.t -= self.speed
        direction = (r.randint(-1,1), r.randint(-1,1))
        (x,y) = map(lambda a,b:a+b, self.location, direction)
        if self.map.data[x][y].isPassable():
            self.moveTo((x,y))



