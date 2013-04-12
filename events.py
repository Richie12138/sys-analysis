# An enumerate class.
from debug import dprint

class EventTypes:
    DEFAULT_EVENT = 'default-event'
    GAME_EVENT = 'game-event'
    SNAKE_BORN = 'snake-born'
    SNAKE_DIE = 'snake-die'
    SNAKE_EAT = 'snake-eat'
    SNAKE_MOVE = 'snake-move'
    HIGH_SCORE = 'high-score'
    GAME_END = 'game-end'
    FOOD_GEN = 'food-gen'
    FOOD_DISAPPEAR = 'food-disappear'

class Event(object):
    """
    members:

    @type: value from EventTypes
    """
    type = EventTypes.DEFAULT_EVENT
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
class SnakeBorn(GameEvent):
    type = EventTypes.SNAKE_BORN
    def __init__(self, snake):
        self.snake = snake
        super(SnakeBorn, self).__init__()

class SnakeDie(GameEvent):
    type = EventTypes.SNAKE_DIE
    def __init__(self, reason, snake, pos):
        self.reason = reason
        self.snake = snake
        self.pos = pos
        super(SnakeDie, self).__init__()

class SnakeEat(GameEvent):
    type = EventTypes.SNAKE_EAT
    def __init__(self, snake, food, pos):
        self.pos = pos
        self.food = food
        self.snake = snake

class SnakeMove(GameEvent):
    type = EventTypes.SNAKE_MOVE
    def __init__(self, snake, from_, to_):
        self.snake = snake
        self.from_ = from_
        self.to_ = to_

class FoodGen(GameEvent):
    type = EventTypes.FOOD_GEN
    def __init__(self, food, pos):
        self.food = food
        self.pos = pos

class FoodDisappear(GameEvent):
    type = EventTypes.FOOD_DISAPPEAR
    def __init__(self, food, pos):
        self.food = food
        self.pos = pos

class GameEnd(GameEvent):
    type = EventTypes.GAME_END
    def __init__(self, winner):
        """
        @winner: A Player instance
        """
        self.winner = winner

class EventManager:
    def __init__(self):
        self._eventHandlers = {}

    def bind(self, eventType, handler):
        """
        @eventType: Value from EventTypes
        @handler: A callable with one parameter. Prototype:
                
                def handler(event): pass
        """
        if eventType not in self._eventHandlers:
            self._eventHandlers[eventType] = set()
        self._eventHandlers[eventType].add(handler)

    def unbind(self, eventType, handler):
        self._eventHandlers[eventType].remove(handler)

    def emit(self, event):
        eventType = event.type
        # dprint('emit', event)
        for handler in self._eventHandlers.get(eventType, []):
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
