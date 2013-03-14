# types of events
SNAKE_DIE = "snake-die"
SNAKE_EAT = "snake-eat"
SNAKE_MOVE = "snake-move"
HIGH_SCORE = "high-score"
# etc ..

# mapping
link_dict = {}

def bound(evt, callback):
    # the mapping should finally look like:
    # evt -> [callback1, callback2, ...]
    #
    # a callback currently takes `world` as its parameter.
    pass

class Event(object):
    def __init__(self, target, evt_type):
        this.target = target
        this.evt_type = evt_types

class GameEvent(Event):
    def __init__(self, type, *args, **kwargs):
        self.type = type
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

# maybe subclassing will be better
class SnakeDie(GameEvent):
    type = SNAKE_DIE
    def __init__(self, reason, snake):
        self.reason = reason
        self.snake = snake
        self.pos = snake.headPos
        super(SnakeDie, self).__init__()

class SnakeEat(GameEvent):
    type = SNAKE_EAT
    def __init__(self, snake, food):
        self.pos = snake.headPos
        self.food = food
        self.snake = snake
