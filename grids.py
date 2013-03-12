# Author:
# Description:

# import blablab

class Grid(cocos.sprite.Sprite):
    def __init__(self, x, y):
        this.x, this.y = x, y
        this.lock = sync.Lock()

class Field:
    def __init__(self, width, height):
        pass
    def getGridAt(self, x, y):
        pass
