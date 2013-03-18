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
            if player.snake.alive:
                player.snake.update_direction(player.currentMove)

        field = self.field
        isStatic = False
        eatings = {}
        while not isStatic:
            nextPositions = []
            isStatic = True
            # test if some snake blocked by food or wall
            for snake in self.snakes:
                poss = snake.next_positions()
                headPos = poss[0]
                grid = field.get_grid_at(*headPos)
                if grid is None:
                    snake.blocked = True
                    dprint('block by field border')
                    isStatic = False
                elif grid.type == grids.FOOD:
                    # block by food
                    dprint('block by food')
                    snake.blocked = True
                    eatings[grid.position] = eatings.get(grid.position, 0) + 1
                    isStatic = False
                nextPositions.append((snake, poss))
            # dprint('nextPositions:', nextPositions)
            if not isStatic: continue
            # test if some snake block by other snake in next move
            for snake, poss in nextPositions:
                headPos = poss[0]
                if headPos in poss[1:]:
                    dprint('block by {}'.format(snake), 'headPos', headPos, 'poss[1:]', poss[1:])
                    snake.blocked = True
                    isStatic = False
                    break
                for snake1, poss1 in nextPositions:
                    if snake1 is not snake and headPos in poss1:
                        dprint('block by {}'.format(snake1))
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
                    eventMgr.emit(SnakeDie( reason=reason, snake=snake))
                    snake.die()
                elif grid is None:
                    eventMgr.emit(SnakeDie(
                        reason="blocked by field border",
                        snake=snake,
                        ))
                    snake.die()
            else:
                # the snake can move
                snake.update()
                eventMgr.emit(SnakeMove(snake))
        self.snakes = [snake for snake in self.snakes if snake.alive]

if __name__ == '__main__':
    pass
