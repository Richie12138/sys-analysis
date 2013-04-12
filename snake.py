"""
This module contains different types of snakes. Some are game logic only while 
some can be used to display.

Author: Ray
"""
from debug import dprint
from grids import Directions
import grids
from events import EventTypes, SnakeDie, SnakeEat, SnakeMove

class BodySection(object):
    def __init__(self, pos):
        self.pos = pos
        self.secID = None

    def __repr__(self):
        return "BodySection(pos={self.pos})".format(self=self)

class Snake(object):
    """
    members:
    @direction: A value from `Directions`
    @body: A list of body sections
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
        self.name = None

        self.lastTail = None
        self.body = []
        self.direction = None
        self.alive = True
        self._mark_die = False

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
        # return "Snake(name={self.player.name}, head={self.head})".format(self=self)
        return "Snake(name={self.player.name}, body={self.body})".format(self=self)

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
            if grid.lock.owner is self:
                grid.clear()
        self.body = []
        for pos in positions:
            bsec = BodySection(pos)
            grid = self.world.field.get_grid_at(*bsec.pos)
            bsec.secID = len(self.body)
            self.body.append(bsec)
            grid.type = grids.SNAKE
            grid.content = bsec
            grid.lock.acquire(self, None, None)
            grid.lock.update()

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

    def eat(self, grid):
        """
        Eat the food on the grid. Clear the grid and place the new head there.

        @grid: The grid containing food
        """
        grid.type = grids.BLANK
        grid.content = self.head
        # create the tail section
        tail = BodySection(self.body[-1].pos)
        tail.secID = len(self.body)
        self.move_forward(eat=True)
        self.body.append(tail)
        # allocate a grid for the tail
        tailGrid = self.world.field.get_grid_at(*tail.pos)
        tailGrid.type = grids.SNAKE
        tailGrid.content = tail
        dprint('eat')
        self.world.gen_food()

    def move_forward(self, eat=False):
        # dprint(self.name, 'move forward')
        # update all bsec.pos by swapping
        #  before: [n] | [0] [1] [2] [3]
        #  swap 1: [0] | [n] [1] [2] [3]
        #  swap 2: [1] | [n] [0] [2] [3]
        #  swap 3: [2] | [n] [0] [1] [3]
        # finish : [3] | [n] [0] [1] [2]
        # where [i] means the self.body[i].pos before swapping.

        get_grid_at = self.world.field.get_grid_at
        nextPos = self.next_head_pos()
        grid = get_grid_at(*nextPos)
        self.lastTail = self.body[-1]
        for bsec in self.body:
            grid = get_grid_at(*bsec.pos)
            if grid.lock.owner is self:
                # the grid may not own by self, due to breaking loop manually
                # see: world.py -> World.update
                grid.type = grids.BLANK
                grid.content = None

        for bsec in self.body:
            nextPos, bsec.pos = bsec.pos, nextPos
            grid = get_grid_at(*bsec.pos)
            grid.type = grids.SNAKE
            grid.content = bsec
        # now nextPos is the original tail pos
        if not eat:
            grid = get_grid_at(*nextPos)
            if grid.lock.owner is self:
                grid.clear()

    def on_acquire_succeed(self):
        # dprint('before update:', self.positions)
        grid = self._nextGrid
        nextPos = grid.pos
        # test if the grid contains food
        if grid.type == grids.FOOD:
            self.eventMgr.emit(SnakeEat(snake=self, food=grid.content, pos=nextPos))
            self.eat(grid)
        else:
            self.eventMgr.emit(SnakeMove(snake=self, from_=self.head.pos, to_=nextPos))
            self.move_forward()

    def on_acquire_fail(self, reason, pos):
        def func():
            self.eventMgr.emit(SnakeDie(
                reason=reason,
                snake=self,
                pos=pos,
                ))
            self.die()
        return func

    def update(self, eventMgr):
        """
        Update the snake's body. During the update:

        * If the movement succeed, emit a SNAKE_MOVE GameEvent. 
        * If the snake eats a food, emit a SNAKE_EAT GameEvent.
        * If the snake dies, emit a SNAKE_DIE GameEvent.

        @eventMgr: A eventMgr for emitting events.

        """
        if self._mark_die:
            dprint('die. "Uuuuaaahhhh!!"'.format(self=self), "length: ", len(self.body))
            self.set_body([])
            self._mark_die = False
            self.alive = False
        if not self.alive: 
            return
        nextPos = self.next_head_pos()
        grid = self.world.field.get_grid_at(*nextPos)
        if grid is None:
            eventMgr.emit(SnakeDie(
                reason="block by field border",
                snake=self,
                pos=nextPos,
                ))
            self.die()
        else:
            self._nextGrid = grid
            self.eventMgr = eventMgr
            # dprint('try go forward')
            grid.lock.acquire(self, self.on_acquire_succeed, 
                    self.on_acquire_fail('blocked by others', grid.pos))

    def die(self):
        self._mark_die = True
