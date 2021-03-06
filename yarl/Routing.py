
PLANNING = 0
COMPLETE = 1
UNROUTABLE = 2

class Route:
    def __init__(self, start, end, map):
        self.start = start
        self.end = end
        self.map = map
        self.route = None
        self.routeStatus = PLANNING
        router.requestRoute(self)


def h(loc, dest):
    # Use manhattan distances for the moment - probably suboptimal but will do
    return 1.01 * (abs(dest[0]-loc[0]) + abs(dest[1]-loc[1]))

def closer(o, p1, p2):
    d1 = h(o, p1)
    d2 = h(o, p2)
    return cmp(d1, d2)

class Node:
    def __init__(self, loc, g, parent, end, passable):
        self.loc = loc
        self.g = g
        self.parent = parent
        if end != None:
            self.h = h(loc, end)
        else:
            self.h = None
        self.passable = passable

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
    def neighbours(nodemap, node, end):
        deltas = ( (1,0), (0,1), (-1,0), (0,-1) )
        results = set()
        (cx,cy) = node.loc
        (width, height) = ( len(nodemap), len(nodemap[0]) )
        for d in deltas:
            x = cx + d[0]
            y = cy + d[1]
            if x >= 0 and x < width and\
               y >= 0 and y < height and\
               nodemap[x][y].passable:
                   results.add( nodemap[x][y] )
            if end == (x,y):
                results.add( nodemap[x][y] )
        return results

class Router:
    def __init__(self):
        self.map = None
        self.nodemap = None

    # An a* routing algorithm
    # We use a second map of nodes (which I guess could really be part of the main map, but would
    # need resetting after every search, so unless performance is truly terrible, I'm not too
    # worried for now)
    def requestRoute(self, route):
        (startx, starty) = route.start
        open = set()
        closed = set()
       
        (width, height) = route.map.size
        map = route.map.lock()
        if self.nodemap == None:
            self.nodemap = []
            for x in range(width):
                self.nodemap.append([])
                for y in range(height):
                    self.nodemap[x].append(Node( (x,y), -1, None, route.end, map[x][y].isPassable()) )
        else:
            for x in range(len(self.nodemap)):
                for y in range(len(self.nodemap[x])):
                    self.nodemap[x][y].g = -1
                    self.nodemap[x][y].parent = None
                    self.nodemap[x][y].end = route.end
                    self.nodemap[x][y].passable = map[x][y].isPassable()

        route.map.unlock()
        
        self.nodemap[startx][starty].g = 0
        open.add(self.nodemap[startx][starty])

        lowest = Node.findLowest(open)
        if lowest == None:
            route.routeStatus = UNROUTABLE
            return
        
        while lowest.loc != route.end:
            current = lowest
            open.remove(current)
            closed.add(current)
            for neighbour in Node.neighbours(self.nodemap, current, route.end):
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
            if lowest == None:
                route.routeStatus = UNROUTABLE
                return

        route.route = []
        loc = route.end
        while loc != route.start:
            route.route.append(loc)
            (x,y) = loc
            loc = self.nodemap[x][y].parent.loc

        route.route.reverse()
        route.routeStatus = COMPLETE

router = Router()

