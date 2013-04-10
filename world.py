# Author:
# Description:

import grids
from events import EventTypes, SnakeDie, SnakeEat, SnakeMove
from debug import dprint
import items
import random

class World:
    def __init__(self, width, height):
        self.field = grids.Field(width, height)
        self.players = []
        self.snakes = []

        self.pause = False

    @property
    def foods(self):
        return [g for g in self.field if g.type == grids.FOOD]

    def __repr__(self):
        return "World(foods={self.foods}, snakes={self.snakes},\
                \nfield=\n{self.field}".format(self=self)

    def gen_food(self):
        availGrids = [g for g in self.field if g.type == grids.BLANK]
        grid = random.choice(availGrids)
        food = items.Food(pos=grid.pos)
        grid.type = grids.FOOD
        grid.content = food

    def _update_until_blocking(self):
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
        return blockingLocks

    def update(self, eventMgr):
        """
        Update self.players and self.snakes. Emit events via `@eventMgr`
        @eventMgr: An EventManager object.
        """
        if self.pause: return

        for player in self.players:
            player.update(self)

        field = self.field
        for snake in self.snakes:
            snake.update(eventMgr)

        while 1:
            blockingLocks = self._update_until_blocking()
            if not blockingLocks: 
                break
            for lock in blockingLocks:
                if lock.owner.body[-1].pos != lock.pos:
                    # the lock's pos is not a tail pos
                    lock.fail()
                    break
            else:
                lock.release(lock.owner)

        for lock in blockingLocks:
            lock.fail()

        self.snakes = [snake for snake in self.snakes if snake.alive]

if __name__ == '__main__':
    pass
