EXCAVATE            = 0x00

class Job:
    def __init__(self, location, type, description):
        self.location = location
        self.type = type
        self.description = description

class Excavate(Job):
    def __init__(self, location):
        Job.__init__(self, location, EXCAVATE, "excavate")

jobFactory = {
        EXCAVATE : Excavate
        }

class Manager:
    def __init__(self):
        self.jobs = set()
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

    def pullJob(self, job):
        if not job in self.jobs:
            return None
        self.jobs.remove(job)
        self.sparseJobMap[job.location].remove(job)
        return job

    def popJobAt(self, location):
        location = tuple(location)
        j = self.sparseJobMap[location].pop(0)
        self.jobs.remove(j)
        return j

    def popJobOfTypeAt(self, jobType, location):
        location = tuple(location)
        for job in self.sparseJobMap[location]:
            if job.type == jobType:
                self.jobs.remove(job)
                self.sparseJobMap[location].remove(job)
                return job

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
