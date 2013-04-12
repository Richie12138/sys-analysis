import input
import events
import gamerule
import config
from game import Game
from grids import Directions
from display import Display
from player import HumanPlayer, AIPlayer, StupidAIPlayer, ProgramedPlayer
from debug import dprint

RUN_ALL = 1

class TestBase(object):
    def __init__(self, configData):
        self.configData = configData

    def extra_config(self):
        """
        Slot, this will be called by self.mainloop before the mainloop start.
        """
        pass

    def run(self, isRun):
        if not (isRun or RUN_ALL): return
        game = self.game = Game()
        game.inputMgr.bind(input.key_down_type('q'), game.quit)
        game.inputMgr.bind(input.key_down_type('z'), lambda e: exit(0))
        game.inputMgr.bind(input.key_down_type('p'), game.pause)
        self.display = Display()
        game.setup_stage(self.configData, self.display)

        self.extra_config()
        game.start()
        game.mainloop()

##################################################################
config.UPS = 60
class test_one_AI(TestBase):
    def extra_config(self):
        self.game.join_player(AIPlayer("Alice"))
test_one_AI({
    'world-size': (10, 10), 'snakes':[
            ((5, 5), Directions.RIGHT, 5), 
        ]}).run(1)
