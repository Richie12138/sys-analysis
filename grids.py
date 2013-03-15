# Author: Legend

# Description: 
#   Gird is each grid on the field. Field is combined with grids.
#   These all are used by display at world. Different items have different displays.

"""
represent the grid status
"""
BLANK   =   0
SNAKE   =   1
FOOD    =   2 

class Grid:
    def __init__(self, x, y):
        """ 
        @postion: a turple
        @status: the type
        """
        self.position = (x, y)
        self.status = BLANK

    # return position turple
    def get_position(self):
        return self.position

    """
    status detect. maybe some are not neccessary
    """
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
    def set_position(self, x, y):
        # assume that 0 <= x <= width && 0 <= y <= height
        self.position = (x, y)

    def set_status(self, status):
        # assume that 0 <= status <= 2 
        if status >= 0 and status <= 2:
            self.status = status
            return True
        else:
            return False

    def get_status(self):
        return self.status

    def print_self(self):
        print "Grid position: %s \nGrid status: %d \n" % (self.position, self.status)

class Field:
    """
    @grids: mapping for the field
    """
    fields = {}
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gen_empty_grids(width, height)

    def gen_empty_grids(self, width, height):
        for x in xrange(0, width):
            for y in xrange(0, height):
                self.fields[(x, y)] = Grid(x, y)

    def gen_snake_grids(self):
        pass

    def gen_food_grids(self):
        pass

    def get_grid_at(self, x, y):
        return self.fields[(x, y)]


if __name__ == '__main__':
    test_field = Field(10, 10)
    test_field.get_grid_at(5, 5).print_self()
