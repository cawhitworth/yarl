import Block

class Map:
    def __init__(self, dimensions, appearance):
        self.size = dimensions
        self.data = [ [ Block.Dirt(appearance) for j in range(dimensions[1]) ] for i in range(dimensions[0]) ]

