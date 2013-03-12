# Author:
# Description:

import player

INITIAL_LEN = 5

class Snake(cocos.sprite.Sprite): # subclass this one?
    def __init__(self, world, player)
        this.world = world
        this.field = world.get_field()
        this.player = player

        # body is a list of (x, y) tuple, 
        # with this.body[0] represent its
        # head.
        this.body = world.get_body()

        this.has_food = False

    def update(self, world):
        # get direction
        cmd = this.player.getCmd()

        # then try to obtain a lock

        # A special case should be noticed:
        #
        # ----\
        # ^   |
        # \---/
        #
        # this situation may need specially
        # handling?
