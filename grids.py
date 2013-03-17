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
        self.content = None

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

    #generate grids by different snakes
    def gen_snake_grids(self, snake):
        for pos in snake.positions:
            self.fields[pos].status = SNAKE
            self.fields[pos].content = snake

    def gen_food_grids(self, x, y):
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
    t = test_field.get_grid_at(5,5)
    t.set_content(mysnake)
    print t.content
    if isinstance(t.content, snake.Snake):
        print 'yes'
