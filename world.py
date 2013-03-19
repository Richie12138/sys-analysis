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
        racing = {}
        # block all snakes that racing for a same position or hitting walls
        nextPositions = [(snake, snake.next_positions()) for snake in self.snakes]
        for snake, ps in nextPositions:
            nextPos = ps[0]
            grid = field.get_grid_at(*nextPos)
            if grid:
                racing[nextPos] = racing.get(nextPos, 0) + 1
            else:
                snake.blocked = True
        for snake, ps in nextPositions:
            if not snake.blocked and racing[ps[0]] > 1:
                snake.blocked = True
        isStatic = False
        while not isStatic:
            isStatic = True
            # block all snakes that will hit other snakes
            nextPositions = [(snake, snake.next_positions()) for snake in self.snakes]
            for snake, ps in nextPositions:
                nextPos = ps[0]
                if nextPos in ps[1:]:
                    dprint('{} block by {}'.format(snake, 'self'), 'headPos', headPos, 'poss[1:]', poss[1:])
                    snake.blocked = True
                    isStatic = False
                    break
                for snake1, ps1 in nextPositions:
                    if snake1 is not snake and nextPos in ps1:
                        dprint('{} block by {}'.format(snake, snake1))
                        snake.blocked = True
                        isStatic = False
                        break
                if not isStatic: break
        # handle collisions
        for snake in self.snakes:
            if snake.blocked:
                nextHead = snake.next_head_pos()
                grid = field.get_grid_at(*nextHead)
                if grid and grid.type == grids.FOOD:
                    eatCount = eatings[grid.position]
                    if eatCount > 1:
                        # the snake will die, since it race for food with other
                        # snake
                        eventMgr.emit(SnakeDie(
                            reason="racing for food",
                            snake=snake,
                            pos=nextHead,
                            ))
                        snake.die()
                    else:
                        # the snake cat eat the food
                        snake.blocked = False
                        snake.update()
                        eventMgr.emit(SnakeMove(snake))
                        eventMgr.emit(FoodDisappear(
                            food=grid.content, 
                            pos=grid.position,
                            ))
                elif grid:
                    # the snake will die, since it's blocked by thing other 
                    # than food
                    if grid.type == grids.SNAKE:
                        reason = "blocked by other snake"
                    elif grid.type == grids.BLANK:
                        reason = "race for a position"
                    eventMgr.emit(SnakeDie(reason=reason, snake=snake, pos=nextHead))
                    snake.die()
                elif grid is None:
                    eventMgr.emit(SnakeDie(
                        reason="blocked by field border",
                        snake=snake,
                        pos=nextHead,
                        ))
                    snake.die()
            else:
                # the snake can move
                snake.update()
                eventMgr.emit(SnakeMove(snake))
        self.snakes = [snake for snake in self.snakes if snake.alive]

if __name__ == '__main__':
    pass
