# Author:
# Description:

class World:
    def __init__(self, width, height):
        self.field = grids.Field(width, height)

    def get_field(self):
        return self.field

    def get_body(self)
        # return a list of (x, y) with length snake.INITIAL_LEN
        pass
