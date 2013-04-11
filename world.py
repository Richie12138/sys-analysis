# Author:
# Description:

import grids
from events import EventTypes, SnakeDie, SnakeEat, SnakeMove, FoodGen
from debug import dprint
import config
import items
import random

if config.FAKE_RANDOM:
    random.seed(0)

class World:
    def __init__(self, width, height, eventMgr):
        self.field = grids.Field(width, height)
        self.players = []
        self.snakes = []
        self.eventMgr = eventMgr

        self.pause = False
        self.forbidGenFood = False

    @property
    def foods(self):
        return [g for g in self.field if g.type == grids.FOOD]

    def __repr__(self):
        return "World(foods={self.foods}, snakes={self.snakes},\
                \nfield=\n{self.field}".format(self=self)

    def gen_food(self):
        if self.forbidGenFood: return
        availGrids = [g for g in self.field if g.type == grids.BLANK]
        if availGrids:
            grid = random.choice(availGrids)
            food = items.Food(pos=grid.pos)
            grid.type = grids.FOOD
            grid.content = food
            self.eventMgr.emit(FoodGen(food, grid.pos))
        else:
            # TODO: handle this
            pass

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
        self.eventMgr = eventMgr

        for player in self.players:
            player.update(self)

        field = self.field
        for snake in self.snakes:
            snake.update(eventMgr)

        while 1:
            blockingLocks = self._update_until_blocking()
            if not blockingLocks: 
                break
            if config.PRINT_SYNC: dprint('blockings:', blockingLocks)
            static = True
            for lock in blockingLocks:
                if lock.owner.body[-1].pos != lock.pos:
                    # the lock's pos is not a tail pos
                    lock.fail()
                    static = False
            if static:
                # break loop manually
                lock = blockingLocks[0]
                if config.PRINT_SYNC: dprint('break loop', lock)
                lock.release(lock.owner)
                grid = self.field.get_grid_at(*lock.pos)
                grid.type = grids.BLANK
                grid.content = None

        for lock in blockingLocks:
            if config.PRINT_SYNC: dprint(lock, 'fail')
            lock.fail()
        blockingLocks = self._update_until_blocking()
        assert not blockingLocks

        self.snakes = [snake for snake in self.snakes if snake.alive]

if __name__ == '__main__':
    pass
