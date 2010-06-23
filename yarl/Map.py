import math
import Block

class Map:
    def __init__(self, dimensions, appearance):
        self.size = dimensions
        self.data = [ ]
        for x in range(dimensions[0]):
            self.data.append( [] )
            for y in range(dimensions[1]):
                self.data[x].append(Block.Dirt(appearance))

        (cx,cy) = (40, 14)
        for x in range(30, 50):
            for y in range(4,24):
                d = int(math.sqrt(math.pow(float(x - cx), 2.0) +
                                  math.pow(float(y - cy), 2.0)))
                if d > 6 and d < 10:
                    self.data[x][y].visibility = 1
                elif d > 3 and d <= 6:
                    self.data[x][y].visibility = 2
                elif d <= 3:
                    self.data[x][y].visibility = 3

