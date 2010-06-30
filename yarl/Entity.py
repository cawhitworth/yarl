ENTITY_BASE     = 0x10000
CREATURE_BASE   = 0x20000

DUNGEON_HEART   = 0 | ENTITY_BASE

IMP             =0 | CREATURE_BASE

class Manager:
    def __init__(self):
        self.entities = set()

    def register(self, entity):
        self.entities.add(entity)

    def unregister(self, entity):
        self.entities.remove(entity)

    def update(self, time):
        for e in self.entities:
            e.update(time)

manager = Manager()

class Entity:
    def __init__(self, type, description, appearance, map, location, passable = False):
        self.type = type
        self.passable = passable
        self.description = description
        self.appearance = {}
        self.map = map
        self.location = location
        appearance(self)
        manager.register(self)
        self.moveTo(location)

    def moveTo(self, location):
        (x,y) = self.location
        block = self.map.data[x][y]
        if self in block.entities:
            block.entities.remove(self)
        (x,y) = location
        block = self.map.data[x][y]
        block.entities.append(self)
        self.location = location

class DungeonHeart(Entity):
    def __init__(self, appearance, map, location):
        Entity.__init__(self,
                DUNGEON_HEART,
                "dungeon heart",
                appearance,
                map,
                location
        )

    def update(self, time):
        pass

