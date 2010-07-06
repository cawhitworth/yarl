# A* search

import random
import time

def h(loc, dest):
    return 1.01 * (abs( dest[0] - loc[0] ) + abs( dest[1] - loc[1] ))

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

def findLowest(open):
    lowest = 10000000
    lowestNode = None
    for n in open:
        if n.f() < lowest:
            lowest = n.f()
            lowestNode = n
    return lowestNode 

def neighbours(node, map):
    deltas = ( (1,0), (0,1), (-1,0), (0,-1))
    result = set()
    (cx,cy) = node.loc
    (width, height) = (len(map), len(map[0]))
    for d in deltas:
        x = cx + d[0]
        y = cy + d[1]
        if x >= 0 and x < width and y>= 0 and y < height and map[x][y].passable == True:
            result.add( map[x][y] )
    return result

width = 200 
height = 200

mapBuild = 0
routeFound = 0
iters = 100
for iter in range(iters):
    startTime = time.time()

    map = []
    start = (0,0)
    (sx,sy) = start 
    end = (width-1, height-1)

    for x in range(width):
        map.append([])
        for y in range(height):
            map[x].append(Node( (x,y), -1, None, end) )

    r = random.Random()

    for i in range((width + height) / 4):
        x = r.randint(0,width-1)
        y = r.randint(0,height-1)
        map[x][y].passable = False
    map[width-1][height-1].passable = True
    open = set()
    closed = set()

    map[sx][sy].g = 0

    open.add(map[sx][sy])

    lowest = findLowest(open)

    mapBuild += time.time() - startTime

    while lowest.loc != end:
        current = lowest
        open.remove(current)
        closed.add(current)
        for neighbour in neighbours(current, map):
            neighbour.explored = True
            cost = current.g + 1
            if neighbour in open and cost < neighbour.g:
                open.remove(neighbour)
            if neighbour in closed and cost < neighbour.g:
                closed.remove(neighbour)
            if neighbour not in open and neighbour not in closed:
                neighbour.g = cost
                open.add(neighbour)
                neighbour.parent = current

        lowest = findLowest(open)

    loc = end
    while loc != start:
        (x,y) = loc
        map[x][y].onRoute = True
        loc = map[x][y].parent.loc

    routeFound += time.time() - startTime

#
#for y in range(height):
#    print
#    for x in range(width):
#        if map[x][y].onRoute:
#            print "*",
#        elif map[x][y].explored:
#            print ":",
#        elif map[x][y].passable:
#            print ".",
#        else:
#            print "X",

print "Map build: %ss" % (mapBuild*1000 / iters)
print "Route find: %ss" % (routeFound*1000 / iters)
