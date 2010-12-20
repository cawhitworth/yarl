import Entity
import random
import Jobs
import Routing
import logging

r = random.Random()

IDLE = 0
EN_ROUTE = 1
WORKING = 2
JOB_COMPLETE = 3

class Imp(Entity.Entity):
    def __init__(self, game, appearance, map, location):
        Entity.Entity.__init__(self, game, Entity.IMP, "imp", appearance, location, passable = True)
        self.t = 0
        self.wanderSpeed = 250
        self.routeSpeed = 100
        self.job = None
        self.route = None
        self.status = IDLE

    def idle(self,time):
        if self.job == None:
            pass
#            self.findJob()

        if self.job == None:
            self.t += time
            if self.t < self.wanderSpeed:
                return
            self.t -= self.wanderSpeed

            direction = (r.randint(-1,1), r.randint(-1,1))
            (x,y) = map(lambda a,b:a+b, self.location, direction)
            if self.game.map.isPassable( (x,y) ):
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
            
            if self.route.routeStatus == Routing.UNROUTABLE:
                self.job = None
                self.status = IDLE
                return

            if self.route.routeStatus == Routing.PLANNING:
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
            self.t += time
            if self.t < self.job.duration:
                return
            self.t = 0
            self.job.doWork(self.route.route[0])
            self.job.complete()
            self.job = None
            self.route = None
            self.status = IDLE

    def tryAssignJob(self, job):
        if self.game.map.isRouteable(job.location):
            self.takeJob(job)
            self.t = 0
            return True
        return False

    def findJob(self):
        jobs = [ job for job in Jobs.manager.jobs ]
        jobs.sort( cmp=lambda job1, job2 : Routing.closer(self.location, job1.location, job2.location) )                
        for job in jobs:
            if self.tryAssignJob(job):
                break

    def takeJob(self, job):
        self.job = self.game.jobManager.takeJob(job)
        self.route = Routing.Route(self.location, self.job.location, self.game.map)
        self.status = EN_ROUTE
        logging.info( "Taking job %s at %s" % (self.job.description, self.job.location))