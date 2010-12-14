import Block
import Entity
from Colors import *
import random
import logging

colors = 0
characters = 1

r = random.Random()

appearances = {
        Block.DIRT : { 
            colors : 
                ( (NORMAL, BROWN),
                  (DARK, BROWN),
                  (BRIGHT, BROWN) ),
            characters :
                ( "*" )
        },
        Block.DIRT_FLOOR : {
            colors :
                ( (NORMAL, BROWN),
                  (DARK, BROWN),
                  (BRIGHT, BROWN) ),
            characters : 
                ( ",", ".", "`" )
        },
        Block.STONE_FLOOR : {
            colors :
                ( (NORMAL, GREY),
                  (DARK, GREY),
                  (BRIGHT, GREY) ),
            characters :
                ( "." )
        },
        Block.ROUGH_WALL : {
            colors :
                ( (NORMAL, BROWN), ),
            characters :
                ( "#" )
        },
        Block.SMOOTH_WALL : {
            colors :
                ( (NORMAL, GREY), ),
            characters :
                ( "#" )
        },
        Block.LAVA_MOAT : {
            colors:
                ( (DARK, RED), (NORMAL, RED), (BRIGHT, RED),
                  (NORMAL, YELLOW), (BRIGHT, YELLOW) ),
            characters:
                ( "~" )
        },
        Entity.DUNGEON_HEART : {
            colors:
                ( (BRIGHT, RED), ),
            characters:
                ( "H" )
        },
        Entity.IMP : {
            colors:
                ( (DARK, GREEN), (NORMAL, GREEN), (BRIGHT, GREEN) ),
            characters:
                ( "i" )
        }
    }

def AddAppearance(renderable):
    if not renderable.type in appearances.keys():
        logging.warn("Appearance not available for '%s'" % (renderable.description))
        return
    appearance = appearances[renderable.type]
    cols = appearance[colors]
    chars = appearance[characters]
    color = cols[ r.randint(0, len(cols)-1) ]
    character = chars[ r.randint(0, len(chars)-1) ]
    renderable.appearance["color"] = color
    renderable.appearance["character"] = ord(character)
