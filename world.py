# Author:
# Description:

import grids
from events import EventTypes, SnakeDie, SnakeEat, SnakeMove
from debug import dprint

class World:
    def __init__(self, width, height):
        self.field = grids.Field(width, height)
        self.players = []
        self.snakes = []
        self.foods = []

    def __repr__(self):
        return "World(foods={self.foods}, snakes={self.snakes},\
                \nfield=\n{self.field}".format(self=self)

    def update(self, eventMgr):
        """
        Update self.players and self.snakes. Emit events via `@eventMgr`
        @eventMgr: An EventManager object.
        """
        for player in self.players:
            player.update()

        field = self.field
        for snake in self.snakes:
            snake.update(eventMgr)

        isStatic = False
        while not isStatic:
            isStatic = True
            blockingLocks = []
            for grid in self.field:
                lock = grid.lock
                if lock.update():
                    isStatic = False
                elif lock.waitingList:
                    blockingLocks.append(lock)
        #TODO: handle the circle situation
        for lock in blockingLocks:
            lock.fail()

        self.snakes = [snake for snake in self.snakes if snake.alive]

if __name__ == '__main__':
    pass
