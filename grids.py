# -*- coding:utf-8 -*-
"""
Description: 
  Gird is each grid on the field. Field is combined with grids.
  These all are used by display at world. Different items have different displays.

Author: Legend
"""
import sync
from debug import dprint

# represent the grid status
BLANK, SNAKE, FOOD, WALL = 0, 1, 2, 3

class Directions:
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    # for iterating
    all = (LEFT, RIGHT, UP, DOWN)


class Grid:
    def __init__(self, x, y):
        #postion: a turple
        #status: the type
        self.pos = (x, y)
        self.type = BLANK
        self.content = None
        self.lock = sync.Lock()
        self.lock.pos = (x, y)

    @property
    def owner(self):
        return self.lock.owner

    def clear(self):
        self.type = BLANK
        self.content = None
        self.lock.release(self.lock.owner)

    def __repr__(self):
        return 'Grid(pos={}, type={}'.format(self.pos, self.type)

class Field:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = {}
        self.gen_empty_grids()

    def clear_grids(self):
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                self.fields[(x, y)].type = BLANK

    def gen_empty_grids(self):
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                self.fields[(x, y)] = Grid(x, y)

    #generate grids by different snakes
    #TODO: fix the behavior of this method
    def gen_snake_grids(self, snake):
        try:
            for pos in snake.positions:
                self.fields[pos].type = SNAKE
                self.fields[pos].content = snake
        except KeyError:
            print 'KeyError'

    def get_grid_at(self, x, y):
        """
        @x, y: position
        @return: A `Grid` instance at (x, y)
        """
        try:
            return self.fields[(x, y)]
        except KeyError:
            return None

    def __iter__(self):
        for x in xrange(self.width):
            for y in xrange(self.height):
                yield self.fields[x, y]

    # will be added by needs
    def update(self, snake):
        self.clear_grids()
        self.gen_snake_grids(snake)

    def __repr__(self):
        def get_char(grid):
            if grid.type == SNAKE:
                if grid.lock.owner is None:
                    dprint(grid)
                assert grid.lock.owner is not None
                return str(grid.content.secID % 10)
                # return 'SH'[grid.content.secID==0]
            elif grid.type == BLANK:
                # dprint('gird', grid)
                # return u'\u25A1'.encode('utf8')
                assert grid.lock.owner is None
                return '_'
            elif grid.type == FOOD:
                return 'F'
            else:
                return '?'
        lines = []
        lines.append('x ' + ' '.join(str(x%10) for x in range(self.width)))
        for y in xrange(self.height):
            lines.append(str(y%10) + ' ' + ' '.join(
                get_char(self.fields[x,y]) for x in xrange(self.width)))
        return '\n'.join(lines)

# test main function
if __name__ == '__main__':
    test_field = Field(10, 10)
    world = None
    player = None
    import snake
    mysnake = snake.Snake(world, player)
    mysnake.gen_body((3, 1), Directions.LEFT, 3)
    test_field.gen_snake_grids(mysnake)
    test_field.print_self()
    t = test_field.get_grid_at(5,5)
    t.content = mysnake
    print t.content
    if isinstance(t.content, snake.Snake):
        print 'yes'
