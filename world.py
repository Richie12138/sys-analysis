# Author:
# Description:

class World:
    def __init__(self, width, height):
        self.field = grids.Field(width, height)
        self.players = []
        self.snakes = []

    # We don't need getter and setter in python
    # def get_field(self):
    #     return self.field

    def add_player(self, player):
        """
        Add the player into the world.
        """
        pass
