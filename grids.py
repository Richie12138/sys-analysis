# Author: Legend

# Description: 
#   Gird is each grid on the field. Field is combined with grids.
#   These all are used by display at world. Different items have different displays.

import snake

# represent the grid status
BLANK   =   0
SNAKE   =   1
FOOD    =   2 

class Grid:
    def __init__(self, x, y):
        #postion: a turple
        #status: the type
        self.position = (x, y)
        self.status = BLANK

    # status detect. maybe some are not neccessary
    def set_empty(self):
        self.status = BLANK

    def is_empty(self):
        return self.status == BLANK 

    def set_snake(self):
        self.status = SNAKE

    def is_snake(self):
        return self.status == SNAKE

    def set_food(self):
        self.status = FOOD

    def is_food(self):
        return self.status == FOOD

    # test functions

    def set_status(self, status):
        # assume that 0 <= status <= 2 
        if status >= 0 and status <= 2:
            self.status = status
            return True
        else:
            return False

    def print_self(self):
        print "Grid position: %s \nGrid status: %d \n" % (self.position, self.status)

class Field:
    #grids: mapping for the field
    fields = {}

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gen_empty_grids(width, height)

    def gen_empty_grids(self, width, height):
        for x in xrange(0, width):
            for y in xrange(0, height):
                self.fields[(x, y)] = Grid(x, y)

    #generate grids by different roles
    def gen_snake_grids(self, snake):
        for pos in snake.positions:
            self.fields[pos].set_snake()

    def gen_food_grids(self):
        pass

    # get grid
    def get_grid_at(self, x, y):
        return self.fields[(x, y)]

    # will be added by needs
    def update(self):
        pass

    #test print
    def print_self(self):
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                print self.fields[(x, y)].status,
            print ''

# test main function
if __name__ == '__main__':
    test_field = Field(10, 10)
    world = None
    player = None
    mysnake = snake.Snake(world, player)
    mysnake.gen_body((3, 1), snake.Directions.LEFT, 3)
    test_field.gen_snake_grids(mysnake)
    test_field.print_self()
