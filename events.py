# types of events
DEFAULT_EVENT = 'default-event'
GAME_EVENT = 'game-event'
SNAKE_DIE = "snake-die"
SNAKE_EAT = "snake-eat"
SNAKE_MOVE = "snake-move"
HIGH_SCORE = "high-score"
FOOD_GEN = "food-gen"
FOOD_DISAPPEAR = "food-disappear"
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
    type = DEFAULT_EVENT
    def __init__(self, *args, **kwargs):
        for key, val in kwargs.iteritems():
            setattr(self, key, val)

    def __repr__(self):
        return '{self.__class__.__name__}(type={self.type!r}, {desc})'.format(
                self=self, 
                desc=', '.join('{}={!r}'.format(k, v) 
                    for (k, v) in self.__dict__.iteritems() if k != 'type'),
                )

class GameEvent(Event):
    pass

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

class SnakeMove(GameEvent):
    type = SNAKE_MOVE
    def __init__(self, snake):
        self.snake = snake

class FoodGen(GameEvent):
    type = FOOD_GEN
    def __init__(self, food, pos):
        self.food = food
        self.pos = pos

class FoodDisappear(GameEvent):
    type = FOOD_DISAPPEAR
    def __init__(self, food, pos):
        self.food = food
        self.pos = pos

class EventManager:
    def __init__(self):
        self._eventHandlers = {}

    def bind(self, eventType, handler):
        if eventType not in self._eventHandlers:
            self._eventHandlers[eventType] = set()
        self._eventHandlers[eventType].add(handler)

    def unbind(self, eventType, handler):
        self._eventHandlers[eventType].remove(handler)

    def emit(self, event):
        eventType = event.type
        for handler in self._eventHandlers[eventType]:
            handler(event)

    # @staticmethod
    # def test():
    #     menuManager = EventManager()
    #     menuManager.bind(KeyDownEvent('q'), game.quit)
    #     menuManager.bind(KeyDownEvent('up'), menu.select_previous)
    #     menuManager.bind(KeyDownEvent('down'), menu.select_next)
    #     def finish(event):
    #         game.eventManager = gamingManager
    #     menuManager.bind(KeyDownEvent('enter'), finish)

    #     gamingManager = EventManager()
    #     gamingManager.bind(KeyDownEvent('up'), lambda e: player1.up)
    #     gamingManager.bind(KeyDownEvent('down'), lambda e: player1.down)

    #     game.eventManager = menuManager
    #     game.main_loop()

if __name__ == '__main__':
    def barker(msg):
        def func(event):
            print 'barker:', msg, event
        return func

    def test_bind():
        print '=' * 80
        mgr = EventManager()
        mgr.bind(GameEvent.type, barker("game event!"))

    def test_emit():
        print '=' * 80
        mgr = EventManager()
        mgr.bind(GameEvent.type, barker("game event!"))
        print 'emit'
        mgr.emit(GameEvent(foo="bar"))

    def test_unbind():
        print '=' * 80
        mgr = EventManager()
        handler = barker("game event!")
        mgr.bind(GameEvent.type, handler)
        print 'emit'
        mgr.emit(GameEvent(foo="bar"))
        mgr.unbind(GameEvent.type, handler)
        print 'emit'
        mgr.emit(GameEvent(foo="bar"))

    test_bind()
    test_emit()
    test_unbind()
