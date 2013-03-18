"""
This module contains different types of snakes. Some are game logic only while 
some can be used to display.

Author: Ray
"""
from debug import dprint
from grids import Directions
import grids

class BodySection(object):
    def __init__(self, pos):
        self.pos = pos

    def __repr__(self):
        return "BodySection(pos={self.pos})".format(self=self)

class Snake(object):
    """
    members:
    @direction: A value from `Directions`
    @body: A list of body sections
    @blocked: Telling if the snake is blocked in next move
    @alive: Telling if the snake is alive.
    """
    def __init__(self, world, player):
        """
        Snake in the game logic. 
        parameters:
        @world: the world (`world.World`) object where the snake lies
        @player: the player (`player.Player`) controlling the snake
        """
        self.world = world
        self.player = player

        self.body = []
        self.direction = None
        self.blocked = False
        self.alive = True

    @property
    def head(self):
        """
        The head of the snake.
        """
        return self.body[0]

    def gen_body(self, headPos, direction, length):
        """
        Generate and set a body for the snake.
        @headPos: head position, an (x, y) tuple.
        @direction: direction tuple, (dx, dy). 
                For example, Directions.RIGHT makes the snake lies right to left.
        @length: length of the generated body.

        @return: None
        """
        self.direction = direction
        dx, dy = direction
        positions = [headPos]
        x, y = headPos
        for i in xrange(1, length):
            x, y = x - dx, y - dy
            positions.append((x, y))
        self.set_body(positions)

    def __repr__(self):
        return "Snake(blocked={self.blocked}, positions={self.positions})".format(self=self)

    def set_body(self, positions):
        """
        Set the snake body by a list of positions
        @positions: a list of (x, y) tuples, indicating each section of the body.
                    positions[0] will be the head position.
        
        @return: None
        """
        # clear previous grids
        for bsec in self.body:
            grid = self.world.field.get_grid_at(*bsec.pos)
            grid.type = grids.BLANK
            grid.content = None
        self.body = []
        for pos in positions:
            bsec = BodySection(pos)
            self.world.field.get_grid_at(*pos).content = bsec
            self.body.append(bsec)

    def next_positions(self):
        """
        @return: the positions of the snake's body sections after next move.
                Note that the snake wouldn't move actually.
        """
        if not self.blocked:
            nextPositions = [self.next_head_pos()]
            nextPositions.extend(self.positions[:-1])
            return nextPositions
        else:
            return self.positions

    @property
    def positions(self):
        """
        Current position of the body.
        """
        return [bsec.pos for bsec in self.body]

    def next_head_pos(self):
        """
        @return: Next head position according to self.direction.
        """
        dx, dy = self.direction
        x0, y0 = self.head.pos
        newHead = x0 + dx, y0 + dy
        return newHead

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
        return cmd

    def update(self):
        """
        Update the snake's body. During the update:

        * If the movement succeed, emit a SNAKE_MOVE GameEvent. 
        * If the snake eats a food, emit a SNAKE_EAT GameEvent.

        @return a list of emitted events during the update.
        """
        # print 'direction:', self.direction
        nextPos = self.next_head_pos()
        # update all bsec.pos by swapping
        #  before: [n] | [0] [1] [2] [3]
        #  swap 1: [0] | [n] [1] [2] [3]
        #  swap 2: [1] | [n] [0] [2] [3]
        #  swap 3: [2] | [n] [0] [1] [3]
        # finish : [3] | [n] [0] [1] [2]
        # where [i] means the self.body[i].pos before swapping.

        # dprint('before update:', self.positions)
        get_grid_at = self.world.field.get_grid_at
        for bsec in self.body:
            grid = get_grid_at(*bsec.pos)
            grid.type = grids.BLANK
            grid.content = None
            nextPos, bsec.pos = bsec.pos, nextPos
        for bsec in self.body:
            grid = get_grid_at(*bsec.pos)
            grid.type = grids.SNAKE
            grid.content = bsec
        # dprint('after update:', self.positions)

    def die(self):
        dprint('die. "Uuuuaaahhhh!!"'.format(self=self))
        self.alive = False
        self.set_body([])

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
