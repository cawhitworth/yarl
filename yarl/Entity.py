from GameComponent import GameComponent

ENTITY_BASE     = 0x10000
CREATURE_BASE   = 0x20000

DUNGEON_HEART   = 0 | ENTITY_BASE

IMP             =0 | CREATURE_BASE

class Manager(GameComponent):
    def __init__(self, game):
        GameComponent.__init__(self, game)
        self.entities = set()

    def register(self, entity):
        self.entities.add(entity)

    def unregister(self, entity):
        self.entities.remove(entity)

    def update(self, time):
        for e in self.entities:
            e.update(time)
            
    def getEntitiesOfType(self, type):
        return [e for e in self.entities if e.type == type]

class Entity:
    def __init__(self, game, type, description, appearance, location, passable = False):
        self.type = type
        self.passable = passable
        self.description = description
        self.appearance = {}
        
        self.location = location
        self.game = game
        self.game.entityManager.register(self)
        
        appearance(self)
        self.moveTo(location)

    def moveTo(self, location):
        (x,y) = self.location
        map = self.game.map
        block = map.data[x][y]
        if self in block.entities:
            block.entities.remove(self)
        (x,y) = location
        block = map.data[x][y]
        block.entities.append(self)
        self.location = location

class DungeonHeart(Entity):
    def __init__(self, game, appearance, location):
        Entity.__init__(self, game,
                DUNGEON_HEART,
                "dungeon heart",
                appearance,
                location
        )

    def update(self, time):
        pass

