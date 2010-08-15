import Entity
import random
import Jobs
import Block
import Routing

r = random.Random()

IDLE = 0

class Imp(Entity.Entity):
    def __init__(self, appearance, map, location):
        Entity.Entity.__init__(self, Entity.IMP, "imp", appearance, map, location, passable = True)
        self.t = 0
        self.wanderSpeed = 250
        self.routeSpeed = 100
        self.job = None
        self.route = None

    def update(self, time):

        if self.job == None:
            self.t += time
            if self.t < self.wanderSpeed:
                return
            self.t -= self.wanderSpeed
            
            self.findJob()

        if self.job == None:
            direction = (r.randint(-1,1), r.randint(-1,1))
            (x,y) = map(lambda a,b:a+b, self.location, direction)
            if self.map.data[x][y].isPassable():
                self.moveTo((x,y))

        if self.job != None:
            if self.job.cancelled:
                self.job = None

            self.t += time
            if self.t < self.routeSpeed:
                return
            self.t -= self.routeSpeed

            if self.route.route == None:
                # Still waiting for the route to be calculated
                return

            if len(self.route.route) > 1:
                self.moveTo(self.route.route[0])
                self.route.route = self.route.route[1:]
            else:
                if self.job.type == Jobs.EXCAVATE:
                    (x,y) = self.route.route[0]
                    self.map.data[x][y] = Block.DirtFloor(self.map.appearance)
                    for dx in range(-3,4):
                        for dy in range(-3,4):
                            xx = x + dx
                            yy = y + dy
                            if xx < 0 or xx > self.map.size[0]\
                             or yy < 0 or yy > self.map.size[1]:
                                 continue
                            self.map.data[xx][yy].visibility = 3
                Jobs.manager.jobComplete(self.job)
                self.job = None
                self.route = None

    def findJob(self):
        for job in Jobs.manager.jobs:
            if self.map.isRouteable(job.location):
                self.takeJob(job)
                self.t = 0
                break

    def takeJob(self, job):
        self.job = Jobs.manager.takeJob(job)
        self.route = Routing.Route(self.location, self.job.location, self.map)
        print "Taking job %s at %s" % (self.job.description, self.job.location)

