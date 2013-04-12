import pygame

def key(name):
    """
    @return: a key constant specified by `@name`
    """
    try:
        if name is None:
            return None
        else:
            return getattr(pygame, 'K_{}'.format(name))
    except:
        raise Exception('unknown key: {}'.format(name))

def key_down_type(keyName=None):
    return (pygame.KEYDOWN, key(keyName))

def key_up_type(keyName=None):
    return (pygame.KEYUP, key(keyName))

class InputManager:
    def __init__(self):
        self._callbacks = {}

    def bind(self, eventType, callback):
        """
        bind the event and the corresponding callback in self._callbacks
        Parameters:
        @ eventType: a hashable tuple, included the event.type and event.key
        @ callback: a callable function
        """
        if eventType not in self._callbacks:
            #if eventType is not in _callbacks, initialize it
            self._callbacks[eventType] = []
        self._callbacks[eventType].append(callback)

    def parse_event_type(self, e):
        """
        parse the event into a hashable object(a tuple)
        Parameters:
        @e: a pygame event(Here I gurantee that event.type was KEYDOWN or KEYUP)
        """
        return (e.type, e.key)

    def update(self):
        """
        Listen to the key event in the pygame.event
        """
        for e in pygame.event.get():
            callbacks = []
            if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                type = self.parse_event_type(e)
                if type in self._callbacks:
                    callbacks += self._callbacks[type]
                    #call the event's corresponding callbacks
                callbacks += self._callbacks.get((e.type, None), [])
            for callback in callbacks:
                callback(e)

# Test
# ================================
if __name__ == "__main__":
    from player import HumanPlayer
    pygame.display.init()
    screen = pygame.display.set_mode((320, 640),0,32)
    clocks = pygame.time.Clock()
    FPS = 30

    mgr = InputManager()
    player1 = HumanPlayer(mgr,[pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d])
    player2 = HumanPlayer(mgr,[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
    while True:
        mgr.update()
        clocks.tick(FPS)
        pygame.display.update()
