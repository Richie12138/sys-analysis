# Author: Legend

# Description: 
#   Gird is each grid on the field. Field is combined with grids.
#   These all are used by display at world. Different items have different displays.

# represent the grid status
BLANK, SNAKE, FOOD = 0, 1, 2

class Grid:
    def __init__(self, x, y):
        #postion: a turple
        #status: the type
        self.position = (x, y)
        self.type = BLANK
        self.content = None

    def print_self(self):
        print "Grid position: %s \nGrid status: %d \n" % (self.position, self.status)

class Field:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fields = {}
        self.gen_empty_grids(width, height)

    def gen_empty_grids(self, width, height):
        for x in xrange(0, width):
            for y in xrange(0, height):
                self.fields[(x, y)] = Grid(x, y)

    #generate grids by different snakes
    def gen_snake_grids(self, snake):
        for pos in snake.positions:
            self.fields[pos].type = SNAKE
            self.fields[pos].content = snake

    def gen_food_grids(self, x, y):
        pass

    # get grid
    def get_grid_at(self, x, y):
        try:
            return self.fields[(x, y)]
        except KeyError:
            return None

    # will be added by needs
    def update(self):
        pass

    #test print
    def print_self(self):
        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                print self.fields[(x, y)].type,
            print ''

# test main function
if __name__ == '__main__':
    test_field = Field(10, 10)
    world = None
    player = None
    import snake
    mysnake = snake.Snake(world, player)
    mysnake.gen_body((3, 1), snake.Directions.LEFT, 3)
    test_field.gen_snake_grids(mysnake)
    test_field.print_self()
    t = test_field.get_grid_at(5,5)
    t.content = mysnake
    print t.content
    if isinstance(t.content, snake.Snake):
        print 'yes'
