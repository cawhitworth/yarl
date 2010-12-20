import Routing
import Imp
import Entity
import Block
from GameComponent import GameComponent
import logging

EXCAVATE            = 0x00
ROUGH_WALL          = 0x01
SMOOTH              = 0x02

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
    validBlocks = ( Block.DIRT, Block.SMOOTH_WALL, Block.ROUGH_WALL )
    
    digTimes = { Block.DIRT : 250,
                 Block.SMOOTH_WALL : 2000,
                 Block.ROUGH_WALL : 1000 }
    
    def __init__(self, manager, location):
        block = manager.game.map.block(location)
        Job.__init__(self, manager, location, EXCAVATE, "excavate", self.digTimes[block.type])

    def doWork(self, location):
        (x,y) = location
        (width, height) = self.manager.game.map.size
        map = self.manager.game.map
        
        block = Block.DirtFloor(self.manager.game.map.appearance)
        block.visibility = 3
        map.setBlock(location, block)
                
        for dx in range(-3,4):
            for dy in range(-3,4):
                xx = x + dx
                yy = y + dy
                if xx < 0 or xx > width or yy < 0 or yy > height:
                    continue
                map.setVisibility( (xx, yy), 3)
                
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                xx = x + dx
                yy = y + dy
                if map.block( (xx,yy) ).type == Block.DIRT:
                    buildWall = True
                    for job in self.manager.jobsAt((xx,yy)):
                        if job.type in (EXCAVATE, ROUGH_WALL):
                            buildWall = False
                    if buildWall:
                        self.manager.newJob(ROUGH_WALL, (xx,yy))
                        

class RoughWall(Job):
    validBlocks = ( Block.DIRT, )

    def __init__(self, manager, location):
        Job.__init__(self, manager, location, ROUGH_WALL, "build rough wall", 1000)

    def doWork(self, location):
        map = self.manager.game.map
        block = Block.RoughWall(map.appearance)
        block.visibility = 3

        map.setBlock(location, block)


class Smooth(Job):
    validBlocks = ( Block.ROUGH_WALL, Block.DIRT_FLOOR )
    smoothedBlock = {
                     Block.ROUGH_WALL : ( "smooth wall", Block.SMOOTH_WALL ),
                     Block.DIRT_FLOOR : ( "smooth floor", Block.STONE_FLOOR ) }

    def __init__(self, manager, location):
        block = manager.game.map.block(location)

        if block.type not in self.smoothedBlock:
            manager.jobComplete()
        else:
            (name, self.finalBlock) = self.smoothedBlock[block.type]
            Job.__init__(self, manager, location, SMOOTH, name, 1000)

    def doWork(self, location):
        (x,y) = location
        map = self.manager.game.map
        block = Block.factory[self.finalBlock](map.appearance)
        block.visibility = 3
        
        map.setBlock(location, block)

jobFactory = {
        EXCAVATE : Excavate,
        ROUGH_WALL : RoughWall,
        SMOOTH : Smooth
        }

class Manager(GameComponent):
    def __init__(self, game):
        GameComponent.__init__(self, game)
        self.jobs = set()
        self.inProgressJobs = set()
        self.sparseJobMap = {}

    def update(self, time):
        imps = self.game.entityManager.getEntitiesOfType(Entity.IMP)
        self._assignJobs(imps)

    def _buildJobImpPairs(self, imps):
        pairs = [ (imp, job) for imp in imps for job in self.jobs if imp.status == Imp.IDLE]
        pairs.sort( cmp = lambda p1, p2 : cmp( Routing.h(p1[0].location, p1[1].location), 
                                               Routing.h(p2[0].location, p2[1].location)))
        return pairs
    
    def _assignJobs(self, imps):
        pairs = self._buildJobImpPairs(imps)
        if not pairs:
            return
        for (imp, job) in pairs:
            if imp.status != Imp.IDLE:
                continue
            if job not in self.inProgressJobs:
                imp.tryAssignJob(job)

    def newJob(self, jobType, location):
        jobClass = jobFactory[jobType]
        if self.game.map.block(location).type not in jobClass.validBlocks:
            return None
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
        logging.info("Pending jobs:")
        for job in self.jobs:
            logging.info("  %s at %s", job.description, job.location)
