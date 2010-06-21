


def Map:
    def __init__(self, dimensions):
        self.size = dimensions
        self.data = [ [ DirtBlock() ] * dimension[0] for i in range(dimensions[1]) ]

