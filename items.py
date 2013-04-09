# Author:
# Description:

class Item(object):
    def __hash__(self):
        return hash(self.pos)

class Food(Item):
    def __init__(self, pos, score=5):
        self.score = score
        self.pos = pos

class Wall(Item):
    def __init__(self, pos):
        self.pos = pos
