# Author:
# Description:

import grids

class World:
    def __init__(self, width, height):
        self.field = grids.Field(width, height)
        self.players = []
        self.snakes = []

    def update(self):
        for player in self.players:
            player.update()

        # TODO synchronization problem
        for snake in self.snakes:
            snake.update()

        self.field.update()
