import Entity
import random
import Jobs
import Block
import Routing

r = random.Random()

IDLE = 0
EN_ROUTE = 1
WORKING = 2
JOB_COMPLETE = 3

class Imp(Entity.Entity):
    def __init__(self, appearance, map, location):
        Entity.Entity.__init__(self, Entity.IMP, "imp", appearance, map, location, passable = True)
        self.t = 0
        self.wanderSpeed = 250
        self.routeSpeed = 100
        self.digSpeed = 250
        self.job = None
        self.route = None
        self.status = IDLE

    def idle(self,time):
        if self.job == None:
            self.findJob()

        if self.job == None:
            self.t += time
            if self.t < self.wanderSpeed:
                return
            self.t -= self.wanderSpeed

            direction = (r.randint(-1,1), r.randint(-1,1))
            (x,y) = map(lambda a,b:a+b, self.location, direction)
            if self.map.data[x][y].isPassable():
                self.moveTo((x,y))

    def update(self, time):
        if self.status == IDLE:
            self.idle(time)
            if self.job == None:
                return
        
        elif self.status == EN_ROUTE:
            if self.job == None:
                self.status = IDLE
                return

            if self.job.cancelled:
                self.job = None
                self.status = IDLE
                return

            if self.route.route == None:
                # Still waiting for the route to be calculated
                return

            if len(self.route.route) > 1:
                self.t += time
                if self.t < self.routeSpeed:
                    return
                self.t -= self.routeSpeed

                self.moveTo(self.route.route[0])
                self.route.route = self.route.route[1:]
            else:
                self.status = WORKING
                self.t = 0
        
        elif self.status == WORKING:
            if self.job.type == Jobs.EXCAVATE:
                self.t += time
                if self.t < self.digSpeed:
                    return
                self.t = 0
                self.excavate(self.route.route[0])
        
        elif self.status == JOB_COMPLETE:
            Jobs.manager.jobComplete(self.job)
            self.job = None
            self.route = None
            self.status = IDLE

    def findJob(self):
        for job in Jobs.manager.jobs:
            if self.map.isRouteable(job.location):
                self.takeJob(job)
                self.t = 0
                break

    def takeJob(self, job):
        self.job = Jobs.manager.takeJob(job)
        self.route = Routing.Route(self.location, self.job.location, self.map)
        self.status = EN_ROUTE
        print "Taking job %s at %s" % (self.job.description, self.job.location)

    def excavate(self, loc):
        (x,y) = loc
        self.map.data[x][y] = Block.DirtFloor(self.map.appearance)
        for dx in range(-3,4):
            for dy in range(-3,4):
                xx = x + dx
                yy = y + dy
                if xx < 0 or xx > self.map.size[0]\
                 or yy < 0 or yy > self.map.size[1]:
                     continue
                self.map.data[xx][yy].visibility = 3
        self.status = JOB_COMPLETE
