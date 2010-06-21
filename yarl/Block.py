import random

r = random.Random()

DIRT = 0
DIRT_FLOOR = 1
STONE_FLOOR = 2
ROUGH_WALL = 3

class Block:
    def __init__(self, type, passable, description, variant=0):
        self.type = type
        self.passable = passable
        self.description = description
        self.variant = variant

class Dirt(Block):
    def __init__(self):
        self.Block.__init__(DIRT, false, "dirt", variant = r.randint(0,2))

class DirtFloor(Block):
    def __init__(self):
        self.Block.__init__(DIRT_FLOOR, true, "dirt floor", variant = r.randint(0,2))

