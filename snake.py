"""
This module contains different types of snakes. Some are game logic only while 
some can be used to display.

Author: Ray
"""
import events

class Directions:
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    # for iterating
    all = (LEFT, RIGHT, UP, DOWN)

class BodySection(object):
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return "BodySection(pos={self.pos})".format(self=self)

class Snake(object):
    def __init__(self, world, player):
        """
        Snake in the game logic. 
        parameters:
        @world: the World (world.World) object where the snake lies
        @player: the player (player.Player) controling the snake
        """
        self.world = world
        self.player = player

        self.body = []
        self.direction = None

    @property
    def head(self):
        """
        The head position of the snake.
        """
        try:
            return self.body[0]
        except IndexError:
            return None

    def gen_body(self, headPos, direction, length):
        """
        Generate and set a body for the snake.
        @headPos: head position, an (x, y) tuple.
        @direction: direction tuple, (dx, dy). For example, (-1, 0) makes the
                    snake lies right to left.
        @length: length of the generated body.

        @return: None
        """
        dx, dy = direction
        positions = [headPos]
        x, y = headPos
        for i in xrange(1, length):
            x, y = x + dx, y + dy
            positions.append((x, y))
        self.set_body(positions)

    def __repr__(self):
        return "Snake(head={self.head}, positions={self.positions})".format(self=self)

    def set_body(self, positions):
        """
        Set the snake body by a list of positions
        @positions: a list of (x, y) tuples, indicating each section of the body.
                    positions[0] will be the head position.
        
        @return: None
        """
        self.body = [BodySection(p) for p in positions]

    def next_positions(self):
        """
        @return: the positions of the snake's body sections after next move.
                Note that the snake wouldn't move actually.
        """
        dx, dy = self.direction
        x0, y0 = self.head.pos
        newHead = x0 + dx, y0 + dy
        nextPositions = [newHead]
        nextPositions.extend(self.positions[:-1])
        return nextPositions

    @property
    def positions(self):
        """
        Current position of the body.
        """
        return [sec.pos for sec in self.body]

    def update_direction(self, cmd):
        """
        Update to next direction according to the player command.
        If the command is invalid, keep current direction.

        @return: True if update is a success else False.
        """
        if cmd is not None:
            dir = dx, dy = self._parse_command(cmd)
            x0, y0 = self.head.pos
            newPos = x0 + dx, y0 + dy
            # avoid going back directly, which is not allowed.
            if len(self.body) == 1 or self.body[1].pos != newPos:
                self.direction = dir
                return True
        return False

    def _parse_command(self, cmd):
        """
        Parse the command from the player
        @cmd: command returned by Player.get_cmd()

        @return: a direction tuple
        """
        # XXX: wait for the document of Player.get_cmd
        return cmd

    def update(self):
        """
        Update the snake's body. During the update:

        * If the movement succeed, emit a SNAKE_MOVE GameEvent. 
        * If the snake eats a food, emit a SNAKE_EAT GameEvent.

        @return a list of emitted events during the update.
        """
        dx, dy = self.direction
        x0, y0 = self.head.pos
        nextPos = x0 + dx, y0 + dy
        for sec in self.body:
            nextPos, sec.pos = self.pos, nextPos
        # snake moved
        headPos = self.head.pos
        grid = self.world.field.get_grid_at(headPos)
        # test if the grid is empty
        gameEvents = []
        if grid.is_empty():
            gameEvents.append(GameEvent(
                type=SNAKE_MOVE, 
                target=self,
                ))
        # test if the grid has food
        elif grid.get_food():
            gameEvents.append(GameEvent(
                type=SNAKE_EAT,
                target=self,
                food=grid.get_food(),
                pos=headPos,
                ))
        return gameEvents

if __name__ == '__main__':
    def sep(title):
        print('='*80)
        print(title)
        print('-'*80)
    world = None
    player = None

    sep('test __init__')
    snake = Snake(world, player)
    print(snake)

    sep('test gen body')
    snake.gen_body((3, 0), Directions.LEFT, 3)
    print(snake)

    sep('test moving')
    snake.update_direction(Directions.RIGHT)
    print('direction:', snake.direction)
    print('cur positions:', snake.positions)
    print('next positions:', snake.next_positions())
    snake.update_direction(Directions.DOWN)
    print('direction:', snake.direction)
    print('cur positions:', snake.positions)
    print('next positions:', snake.next_positions())
