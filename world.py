# Author:
# Description:

import grids
from events import EventTypes, SnakeDie, SnakeEat, SnakeMove
from debug import dprint
import items
import random

random.seed(0)

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

    def update(self, eventMgr):
        """
        Update self.players and self.snakes. Emit events via `@eventMgr`
        @eventMgr: An EventManager object.
        """
        if not self.pause:
            for player in self.players:
                player.update(self)
            if self.pause: return

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

    def test_snake_sync(self):
        snakes = self.snakes
        for snake in snakes:
            # dprint(snake)
            for sec in snake.body:
                grid = self.field.get_grid_at(*sec.pos)
                # dprint(sec)
                assert grid.type == grids.SNAKE
                assert grid.content == sec

if __name__ == '__main__':
    pass
