# Author:
# Description:
from pygame.time import Clock

from snake import Snake, Directions
from world import World
from player import HumanPlayer, AIPlayer, StupidAIPlayer, ProgramedPlayer
from display import Display
from input import InputManager
from events import EventManager, EventTypes
from debug import dprint
from gamerule import DeathModeRule
import gamerule
import random
import input
import events
import pygame
import config

if config.FAKE_RANDOM:
    random.seed(0)

class Game:
    # TODO: doc
    def __init__(self):
        self.inputMgr = InputManager()
        self.eventMgr = EventManager()

    def join_human_player(self, name, keyLayout):
        """
        Join a human player to the game.
        @name: Player name
        @keyLayout: If keyLayout is None, this will be an AIPlayer,
                otherwise use keyLayout as an argument to instantiate a HumanPlayer.
        """
        player = HumanPlayer(name, self.inputMgr, keyLayout)
        self.join_player(player)

    def join_player(self, player):
        """
        Join a player to the game.
        @player: A Player instance.
        """
        playerCount = len(self.world.players)
        # build up a snake
        snakeData = self.snakeDatas[playerCount]
        snake = Snake(self.world, player)
        snake.gen_body(*snakeData)
        player.snake = snake
        # let the snake's name same as the player's name
        snake.name = player.name
        # add snake and player to the world
        self.world.snakes.append(snake)
        self.world.players.append(player)
        # emit a SNAKE_BORN event
        self.eventMgr.emit(events.SnakeBorn(snake))
        # bind gameevent handlers
        def handler(event):
            snake = event.snake
            food = event.food
            if snake is player.snake:
                snake.player.score += food.score
        self.eventMgr.bind(EventTypes.SNAKE_EAT, handler)
        return player

    def setup_stage(self, configData, display):
        """
        Setups the game stage.
        @configData: 
            A dict containing:
            
            * world-size: (width, height)
            * snakes: a list, [SnakeData1, SnakeData2, ...]
            * rule: Optional. A tuple (Rule, args), where `Rule` is GameRule class, 
                    `args` is the arguments to instantiate this Rule.
                    Rule defaluts to DeathModeRule.

            SnakeData: a tuple (headPos, direction, length)
            
        """
        world = World(*configData['world-size'])
        world.gen_food()
        self.snakeDatas = configData['snakes']
        self.world = world
        if 'rule' in configData:
            Rule, args = configData['rule']
            rule = Rule(self.world, self.eventMgr, *args)
        else:
            rule = DeathModeRule(self.world, self.eventMgr)
        self.rule = rule

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

    def pause(self, event):
        self.world.pause = not self.world.pause

    def mainloop(self):
        self._quit = False
        timer = Clock()
        tickCount = 0
        # frame per second
        FPS = config.FPS
        # update per second
        UPS = config.UPS
        while not self._quit:
            # handle input
            self.inputMgr.update()
            # update game state
            if tickCount % (FPS/UPS) == 0:
                # dprint('before update\n'+str(self.world.field))
                self.rule.update()
                self.world.update(self.eventMgr)
            # render using display
            self.display.render(self.world)
            timer.tick(FPS)
            tickCount += 1
        self.display.quit()
        dprint('quit normally')

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
    'rule': (DeathModeRule, ()),
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
        ]}).run(1)

#TODO: add test_scoring_mode
