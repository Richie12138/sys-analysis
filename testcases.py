import input
import events
import gamerule
from game import Game
from grids import Directions
from display import Display
from player import HumanPlayer, AIPlayer, StupidAIPlayer, ProgramedPlayer

class TestBase(object):
    def __init__(self, configData):
        self.configData = configData

    def extra_config(self):
        """
        Slot, this will be called by self.mainloop before the mainloop start.
        """
        pass

    def run(self, isRun):
        if not isRun: return
        game = self.game = Game()
        game.inputMgr.bind(input.key_down_type('q'), game.quit)
        game.inputMgr.bind(input.key_down_type('p'), game.pause)
        self.display = Display()
        game.setup_stage(self.configData, self.display)

        self.extra_config()
        game.mainloop()


##################################################################
class test_human(TestBase):
    def extra_config(self):
        K = input.key
        self.game.join_human_player("Fooo", [K('w'), K('s'), K('a'), K('d')])
test_human({
    'world-size': (15, 15), 'snakes':[ ((8, 8), Directions.RIGHT, 8), 
        ]}).run(0)
##################################################################
class test_self_looping(TestBase):
    def extra_config(self):
        player = ProgramedPlayer("Foo", 'rrddlluu')
        self.game.join_player(player)
test_self_looping({
    'world-size': (15, 15), 'snakes':[ ((8, 8), Directions.RIGHT, 8),
        ]}).run(0)

##################################################################
class test_two_looping(TestBase):
    def extra_config(self):
        self.game.join_player(ProgramedPlayer("Foo", 'rrrddllluu'))
        self.game.join_player(ProgramedPlayer("Bar", 'rrrddllluu'))
test_two_looping({
    'world-size': (20, 20), 'snakes':[
        ((10, 5), Directions.RIGHT, 11),
        ((10, 15), Directions.RIGHT, 10),
        ]}).run(0)

##################################################################
class test_two_looping2(TestBase):
    def extra_config(self):
        self.game.join_player(ProgramedPlayer("Foo", 'dddllluuurrr'))
        self.game.join_player(ProgramedPlayer("Bar", 'uuurrrdddlll'))
test_two_looping2({
    'world-size':(10, 10), 'snakes': [
        ((5, 1), Directions.RIGHT, 6),
        ((2, 4), Directions.LEFT, 6),
        ]}).run(0)

##################################################################
class test_four_looping(TestBase):
    def extra_config(self):
        self.game.join_player(ProgramedPlayer("Foo", 'lddddrrrruuuulll'))
        self.game.join_player(ProgramedPlayer("Bar", 'drrrruuuullllddd'))
        self.game.join_player(ProgramedPlayer("Jax", 'ruuuullllddddrrr'))
        self.game.join_player(ProgramedPlayer("Cot", 'ullllddddrrrruuu'))
test_four_looping({
    'world-size':(20, 20), 'snakes': [
        ((12, 11), Directions.LEFT, 4),
        ((11, 14), Directions.DOWN, 4),
        ((14, 15), Directions.RIGHT, 4),
        ((15, 12), Directions.UP, 4),
        ]}).run(0)

##################################################################
class test_deathmode(TestBase):
    def bark(self, gameEnd):
        print gameEnd
        self.game.quit()
    def extra_config(self):
        self.game.join_player(ProgramedPlayer("Foo", 'l'))
        self.game.join_player(ProgramedPlayer("Bar", 'drrrruuuullllddd'))
        self.game.eventMgr.bind(events.GameEnd.type, self.bark)
test_deathmode({
    'rule': (gamerule.DeathModeRule, ()),
    'world-size':(20, 20), 'snakes': [
        ((12, 11), Directions.LEFT, 4),
        ((11, 14), Directions.DOWN, 4),
        ]}).run(0)

##################################################################
class test_fixed_round_mode(test_deathmode):
    def extra_config(self):
        self.game.join_player(ProgramedPlayer("Foo", 'lddddrrrruuuulll'))
        self.game.join_player(ProgramedPlayer("Bar", 'drrrruuuullllddd'))
        self.game.eventMgr.bind(events.GameEnd.type, self.bark)
test_fixed_round_mode({
    'rule': (gamerule.FixedRoundModeRule, (100,)),
    'world-size':(20, 20), 'snakes': [
        ((12, 11), Directions.LEFT, 4),
        ((11, 14), Directions.DOWN, 4),
        ]}).run(0)
##################################################################
class test_two_AI(TestBase):
    def extra_config(self):
        self.game.join_player(AIPlayer("Alice"))
        self.game.join_player(AIPlayer("Bob"))
test_two_AI({
    'world-size': (15, 15), 'snakes':[
            ((10, 10), Directions.RIGHT, 5), 
            ((9, 9), Directions.RIGHT, 5), 
        ]}).run(1)

#TODO: add test_scoring_mode
