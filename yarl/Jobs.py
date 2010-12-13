import Routing
import Imp
import Entity
import Block
from GameComponent import GameComponent

EXCAVATE            = 0x00
ROUGH_WALL          = 0x01

        


class Job:
    def __init__(self, manager, location, type, description, duration):
        self.location = location
        self.type = type
        self.description = description
        self.cancelled = False
        self.duration = duration
        self.manager = manager
        
    def complete(self):
        self.manager.jobComplete(self)
        
class Excavate(Job):
    def __init__(self, manager, location):
        Job.__init__(self, manager, location, EXCAVATE, "excavate", 250)

    def doWork(self, location):
        (x,y) = location
        map = self.manager.game.map
        map.data[x][y] = Block.DirtFloor(map.appearance)
        for dx in range(-3,4):
            for dy in range(-3,4):
                xx = x + dx
                yy = y + dy
                if xx < 0 or xx > map.size[0]\
                 or yy < 0 or yy > map.size[1]:
                    continue
                map.data[xx][yy].visibility = 3
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                xx = x + dx
                yy = y + dy
                if map.data[xx][yy].type == Block.DIRT:
                    buildWall = True
                    for job in self.manager.jobsAt((xx,yy)):
                        if job.type in (EXCAVATE, ROUGH_WALL):
                            buildWall = False
                    if buildWall:
                        self.manager.newJob(ROUGH_WALL, (xx,yy))

class RoughWall(Job):
    def __init__(self, game, location):
        Job.__init__(self, game, location, ROUGH_WALL, "build rough wall", 250)

    def doWork(self, location):
        (x,y) = location
        map = self.manager.game.map
        map.data[x][y] = Block.RoughWall(map.appearance)
        map.data[x][y].visibility = 3

jobFactory = {
        EXCAVATE : Excavate,
        ROUGH_WALL : RoughWall
        }

class Manager(GameComponent):
    def __init__(self, game):
        GameComponent.__init__(self, game)
        self.jobs = set()
        self.inProgressJobs = set()
        self.sparseJobMap = {}

    def update(self, time):
        imps = self.game.entityManager.getEntitiesOfType(Entity.IMP)
        self.assignJobs(imps)

    def buildJobImpPairs(self, imps):
        pairs = [ (imp, job) for imp in imps for job in self.jobs if imp.status == Imp.IDLE]
        pairs.sort( cmp = lambda p1, p2 : cmp( Routing.h(p1[0].location, p1[1].location), 
                                               Routing.h(p2[0].location, p2[1].location)))
        return pairs
    
    def assignJobs(self, imps):
        pairs = self.buildJobImpPairs(imps)
        if not pairs:
            return
        for (imp, job) in pairs:
            if imp.status != Imp.IDLE:
                continue
            if job not in self.inProgressJobs:
                imp.tryAssignJob(job)

    def newJob(self, jobType, location):
        jobClass = jobFactory[jobType]
        location = tuple(location)
        j = jobClass(self, location)
        self.jobs.add(j)
        if not self.sparseJobMap.has_key(location):
            self.sparseJobMap[location] = []
        self.sparseJobMap[location].append(j)
        return j

    def takeJob(self, job):
        if not job in self.jobs:
            return None
        self.jobs.remove(job)
        self.inProgressJobs.add(job)
        return job

    def jobComplete(self,job):
        self.removeJob(job)

    def popJobAt(self, location):
        location = tuple(location)
        j = self.sparseJobMap[location].pop(0)
        if j in self.jobs:
            self.jobs.remove(j)
        if j in self.inProgressJobs:
            self.inProgressJobs.remove(j)
        return j

    def popJobOfTypeAt(self, jobType, location):
        location = tuple(location)
        if not self.sparseJobMap.has_key(location):
            return None
        for job in self.sparseJobMap[location]:
            if job.type == jobType:
                self.removeJob(job)
                return job
        return None

    def removeJob(self, job):
        if job not in self.jobs and job not in self.inProgressJobs:
            return None
        if job in self.jobs:
            self.jobs.remove(job)
        if job in self.inProgressJobs:
            self.inProgressJobs.remove(job)
        self.sparseJobMap[job.location].remove(job)

    def jobsAt(self, location):
        location = tuple(location)
        if not self.sparseJobMap.has_key(location):
            return []
        else:
            return self.sparseJobMap[location]
    def dump(self):
        print "Pending jobs:"
        for job in self.jobs:
            print "  %s at %s" % (job.description, job.location)
