DIRT = 0
DIRT_FLOOR = 1
STONE_FLOOR = 2
ROUGH_WALL = 3
SMOOTH_WALL = 4

class Block:
    def __init__(self, type, description, appearance, passable = False):
        self.type = type
        self.passable = passable
        self.description = description
        self.appearance = {}
        appearance(self)

class Dirt(Block):
    def __init__(self, appearance):
        Block.__init__(self,
                DIRT,
                "dirt",
                appearance
        )

class DirtFloor(Block):
    def __init__(self):
        Block.__init__(self,
                DIRT_FLOOR, 
                "dirt floor",
                appearance,
                passable = True
        )

class StoneFloor(Block):
    def __init__(self):
        Block.__init__(self,
                STONE_FLOOR,
                "stone floor",
                appearance,
                passable = True
        )

class RoughWall(Block):
    def __init__(self):
        Block.__init__(self,
                ROUGH_WALL,
                "rough wall",
                appearance,
                passable = True
        )

class SmoothWall(Block):
    def __init__(self):
        Block.__init__(self,
                SMOOTH_WALL,
                "smooth wall",
                appearance,
                passable = True
        )
