import math
import Block
import Entity
import Imp

def h(loc, dest):
    # Use manhattan distances for the moment - probably suboptimal but will do
    return 1.01 * (abs(dest[0]-loc[0]) + abs(dest[1]-loc[1]))

class Map:
    def __init__(self, dimensions, appearance):
        self.size = dimensions
        self.data = [ ]
        self.appearance = appearance
        for x in range(dimensions[0]):
            self.data.append( [] )
            for y in range(dimensions[1]):
                self.data[x].append(Block.Dirt(appearance))

        self.addDungeonHeart((20, 14))
        self.imps = []
        self.imps.append(Imp.Imp(appearance, self, (20,13)))
        self.imps.append(Imp.Imp(appearance, self, (20,15)))
        self.imps.append(Imp.Imp(appearance, self, (19,14)))
        self.imps.append(Imp.Imp(appearance, self, (21,14)))


    def addDungeonHeart(self, location):
        self.dungeonHeart = Entity.DungeonHeart(self.appearance, self, location)
        
        (cx,cy) = location

        for x in range(cx-20, cx+20):
            if x < 0 or x > self.size[0]:
                continue
            for y in range(cy-20, cy+20):
                if y < 0 or y > self.size[1]:
                    continue
                d = int(math.sqrt(math.pow(float(x - cx), 2.0) +
                                  math.pow(float(y - cy), 2.0)))
                if x != cx and y != cy and (d == 2 or d == 3):
                    self.data[x][y] = Block.LavaMoat(self.appearance)
                elif d < 4:
                    self.data[x][y] = Block.StoneFloor(self.appearance)
                elif d < 6:
                    self.data[x][y] = Block.DirtFloor(self.appearance)
                elif d == 6:
                    self.data[x][y] = Block.RoughWall(self.appearance)

                if d > 10 and d < 15:
                    self.data[x][y].visibility = 1
                elif d > 3 and d <= 10:
                    self.data[x][y].visibility = 2
                elif d <= 3:
                    self.data[x][y].visibility = 3

        self.data[cx][cy].entities.append(self.dungeonHeart)

    # This function works on the basis that our entire map must be connected
    # Thus, if any square has empty space next to it, it must be routeable from
    # any other point on the map

    def isRouteable(self, loc):
        (cx,cy) = loc
        for dy in (-1,0,1):
            y = cy + dy
            if y < 0 or y >= self.size[1]:
                continue
            for dx in (-1,0,1):
                x = cx + dx
                if x < 0 or x >= self.size[0]:
                    continue
                if dx != 0 and dy != 0: # This can change once I lift the manhattan movement restriction
                    continue
                if dx == 0 and dy == 0:
                    continue
                if self.data[x][y].isPassable():
                    return True
        return False


    # An a* routing algorithm
    # We use a second map of nodes (which I guess could really be part of the main map, but would
    # need resetting after every search, so unless performance is truly terrible, I'm not too
    # worried for now)
    def route(self, start, end):
        class Node:
            def __init__(self, loc, g, parent, end):
                self.loc = loc
                self.g = g
                self.parent = parent
                if end != None:
                    self.h = h(loc, end)
                else:
                    self.h = None
                self.passable = True
                self.explored = False
                self.onRoute = False

            def f(self):
                return self.g + self.h

            @staticmethod
            def findLowest(openset):
                lowest = 1000000000
                lowestNode = None
                for n in openset:
                    if n.f() < lowest:
                        lowest = n.f()
                        lowestNode = n
                return lowestNode

            @staticmethod
            def neighbours(nodemap, node, map, end):
                deltas = ( (1,0), (0,1), (-1,0), (0,-1) )
                results = set()
                (cx,cy) = node.loc
                (width, height) = ( len(nodemap), len(nodemap[0]) )
                for d in deltas:
                    x = cx + d[0]
                    y = cy + d[1]
                    if x >= 0 and x < width and\
                       y >= 0 and y < height and\
                       map[x][y].isPassable():
                           results.add( nodemap[x][y] )
                    if end == (x,y):
                        results.add( nodemap[x][y] )
                return results

        (startx, starty) = start
        open = set()
        closed = set()
        nodemap = []
        for x in range(self.size[0]):
            nodemap.append([])
            for y in range(self.size[1]):
                nodemap[x].append(Node( (x,y), -1, None, end) )

        nodemap[startx][starty].g = 0
        open.add(nodemap[startx][starty])

        lowest = Node.findLowest(open)
        while lowest.loc != end:
            current = lowest
            open.remove(current)
            closed.add(current)
            for neighbour in Node.neighbours(nodemap, current, self.data, end):
                cost = current.g + 1

                if neighbour in open and cost < neighbour.g:
                    open.remove(neighbour)
                if neighbour in closed and cost < neighbour.g:
                    closed.remove(neighbour)
                if neighbour not in open and neighbour not in closed:
                    neighbour.g = cost
                    open.add(neighbour)
                    neighbour.parent = current

            lowest = Node.findLowest(open)

        route = []
        loc = end
        while loc != start:
            route.append(loc)
            (x,y) = loc
            loc = nodemap[x][y].parent.loc

        route.reverse()
        return route
