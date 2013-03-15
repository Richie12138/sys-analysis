# Author:
# Description:

# import blablab

class Grid(cocos.sprite.Sprite):
    def __init__(self, w, h):
        this.w, this.h = w, h
        this.lock = sync.Lock()

class Field:
    def __init__(self, width, height):
        pass
    def get_grid_at(self, x, y):
        pass
