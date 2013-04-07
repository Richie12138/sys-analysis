# Author:
# Description:
from pygame.time import Clock

from snake import Snake, Directions
from world import World
from player import HumanPlayer, AIPlayer
from display import Display
from input import InputManager
from events import EventManager
from debug import dprint
import input
import events

class Game:
    # TODO: doc
    def __init__(self):
        self.inputMgr = InputManager()
        self.eventMgr = EventManager()

    def join_player(self, name, keyLayout=None):
        """
        Join a player to the game.
        @name: Player name
        @keyLayout: If keyLayout is None, this will be an AIPlayer,
                otherwise use keyLayout as an argument to instantiate a HumanPlayer.
        """
        playerCount = len(self.world.players)
        if keyLayout:
            player = HumanPlayer(name, self.inputMgr, keyLayout)
        else:
            player = AIPlayer(name)
        # build up a snake
        snakeData = self.snakeDatas[playerCount]
        snake = Snake(self.world, player)
        snake.gen_body(*snakeData)
        player.snake = snake
        # let the snake's name same as the player's name
        snake.name = name
        # add snake and player to the world
        self.world.snakes.append(snake)
        self.world.players.append(player)
        # emit a SNAKE_BORN event
        self.eventMgr.emit(events.SnakeBorn(snake))

    def setup_stage(self, configData, display):
        """
        Setups the game stage.
        @configData: 
            A dict containing:
            
            * world-size: (width, height)
            * snakes: a list, [SnakeData1, SnakeData2, ...]

            SnakeData: a tuple (headPos, direction, length)
            
        """
        world = World(*configData['world-size'])
        self.snakeDatas = configData['snakes']
        self.world = world

        self.display = display
        # In display, the display should bind callbacks
        # to some game events.
        display.init(self)

    def bind_event(self, eventType, callback):
        """
        Bind the callback to events specified by `eventType`
        @eventType: The event type.
        @callback: A callable, accepting one argument, the event.
        """
        self.eventMgr.bind(eventType, callback)

    def quit(self, *args):
        self._quit = True

    def mainloop(self):
        self._quit = False
        timer = Clock()
        tickCount = 0
        # TODO: move things like FPS to configure module
        # frame per second
        FPS = 30
        # update per second
        UPS = 2
        while not self._quit:
            # handle input
            self.inputMgr.update()
            # update game state
            if tickCount % (FPS/UPS) == 0:
                dprint('before update\n'+str(self.world.field))
                self.world.update(self.eventMgr)
            # render using display
            self.display.render(self.world)
            timer.tick(FPS)
            tickCount += 1
        self.display.quit()
        dprint('quit normally')

if __name__ == '__main__':
    cfgSingle = {
            'world-size': (20, 20),
            'snakes':[
                ((10, 10), Directions.RIGHT, 8),
                ]
            }
    cfgDouble = {
            'world-size': (20, 20),
            'snakes':[
                ((10, 5), Directions.RIGHT, 8),
                ((10, 15), Directions.LEFT, 8),
                ]
            }
    cfgHitting = {
            'world-size':(20, 20),
            'snakes': [
                ((6, 4), Directions.RIGHT, 6),
                ((12, 4), Directions.LEFT, 5),
                ]
            }
    cfgHitting3 = {
            'world-size':(20, 20),
            'snakes': [
                ((6, 4), Directions.RIGHT, 6),
                ((7, 6), Directions.RIGHT, 6),
                ((8, 8), Directions.RIGHT, 6),
                ]
            }
    cfgCircle4 = {
            'world-size':(20, 20),
            'snakes': [
                ((12, 11), Directions.LEFT, 4),
                ((11, 14), Directions.DOWN, 4),
                ((14, 15), Directions.RIGHT, 4),
                ((15, 12), Directions.UP, 4),
                ]
            }
    K = input.key
    dsp = Display()
    def test(configData):
        game = Game()
        game.inputMgr.bind(input.key_down_type('q'), game.quit)
        game.setup_stage(configData, dsp)
        snakes = configData['snakes']
        game.join_player("Foo", [K('w'), K('s'), K('a'), K('d')])
        if len(snakes) > 1:
            game.join_player("Bar", [K('UP'), K('DOWN'), K('LEFT'), K('RIGHT')])
        for i in xrange(2, len(snakes)):
            game.join_player("Player#{}".format(i))
        game.mainloop()

    # test(cfgCircle4)
    # test(cfgHitting)
    #test(cfgHitting3)
    # test(cfgSingle)
    test(cfgDouble)
