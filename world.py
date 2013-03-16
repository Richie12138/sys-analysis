# Author:
# Description:

import grids

class World:
    def __init__(self, width, height):
        self.field = grids.Field(width, height)
        self.players = []
        self.snakes = []

    def add_player(self, player):
        """
        Add the player into the world.
        """
        pass
