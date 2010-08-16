EXCAVATE            = 0x00
ROUGH_WALL          = 0x01

class Job:
    def __init__(self, location, type, description):
        self.location = location
        self.type = type
        self.description = description
        self.cancelled = False

class Excavate(Job):
    def __init__(self, location):
        Job.__init__(self, location, EXCAVATE, "excavate")

class RoughWall(Job):
    def __init__(self, location):
        Job.__init__(self, location, ROUGH_WALL, "build rough wall")

jobFactory = {
        EXCAVATE : Excavate,
        ROUGH_WALL : RoughWall
        }

class Manager:
    def __init__(self):
        self.jobs = set()
        self.inProgressJobs = set()
        self.sparseJobMap = {}

    def newJob(self, jobType, location):
        jobClass = jobFactory[jobType]
        location = tuple(location)
        j = jobClass(location)
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

manager = Manager()
