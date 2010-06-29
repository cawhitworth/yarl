import Jobs

BLOCK_BASE = 0

DIRT            = 0x00 | BLOCK_BASE
DIRT_FLOOR      = 0x01 | BLOCK_BASE
STONE_FLOOR     = 0x02 | BLOCK_BASE
ROUGH_WALL      = 0x03 | BLOCK_BASE
SMOOTH_WALL     = 0x04 | BLOCK_BASE

LAVA_MOAT       = 0x80 | BLOCK_BASE

class Block:
    def __init__(self, type, description, appearance, passable = False, jobs = []):
        self.type = type
        self.passable = passable
        self.description = description
        self.appearance = {}
        self.visibility = 0
        self.highlight = False
        self.entities = []
        self.jobsAllowed = jobs
        appearance(self)

    def isPassable(self):
        # A block is only passable if it and all the entities on it are passable
        passable = self.passable
        for entity in self.entities:
            passable = passable & entity.passable
        return passable

    def canHaveJob(self, jobType):
        return jobType in self.jobsAllowed

class Dirt(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                DIRT,
                "dirt",
                appearance,
                jobs = ( Jobs.EXCAVATE, )
        )

class DirtFloor(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                DIRT_FLOOR, 
                "dirt floor",
                appearance,
                passable = True
        )

class StoneFloor(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                STONE_FLOOR,
                "stone floor",
                appearance,
                passable = True
        )

class RoughWall(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                ROUGH_WALL,
                "rough wall",
                appearance,
                jobs = ( Jobs.EXCAVATE, )
        )

class SmoothWall(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                SMOOTH_WALL,
                "smooth wall",
                appearance,
                jobs = ( Jobs.EXCAVATE, )
        )

class LavaMoat(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                LAVA_MOAT,
                "lava",
                appearance,
                passable = False
        )
