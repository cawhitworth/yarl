import Block
from Colors import *
import random

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
        }
    }

def AddAppearance(block):
    if not block.type in appearances.keys():
        print "Appearance not available for '%s'" % (block.description)
    appearance = appearances[block.type]
    cols = appearance[colors]
    chars = appearance[characters]
    color = cols[ r.randint(0, len(cols)-1) ]
    character = chars[ r.randint(0, len(chars)-1) ]
    block.appearance["color"] = color
    block.appearance["character"] = ord(character)
