ENTITY_BASE = 0x10000

DUNGEON_HEART = 0 | ENTITY_BASE

class Entity:
    def __init__(self, type, description, appearance, passable = False):
        self.type = type
        self.passable = passable
        self.description = description
        self.appearance = {}
        appearance(self)
       
class DungeonHeart(Entity):
    def __init__(self, appearance):
        Entity.__init__(self,
                DUNGEON_HEART,
                "dungeon heart",
                appearance
        )

    def update(self, time):
        pass

class Manager:
    def __init__(self):
        self.entities = []

    def construct(self, entityType, appearance):
        e = entityType(appearance)
        self.entities.append(e)
        return e

    def update(self, time):
        for e in self.entities:
            e.update(time)

manager = Manager()
