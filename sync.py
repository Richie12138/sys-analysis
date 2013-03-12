# Author:
# Description:

# import blablab

class Lock(cocos.sprite.Sprite): # better alternative?
    def __init__(self):
        self.sema = 0
        self.waiting_list = []
        self.owner = None

    def aquire(self, target):
        pass

    def release(self, target)
        pass
