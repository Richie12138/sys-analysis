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
from record import Recorder
import gamerule
import random
import input
import events
import pygame
import menu
import config

if config.FAKE_RANDOM:
    random.seed(0)

class Game:
    # TODO: doc
    ST_MENU = 'menu'
    ST_GAMEPLAY = 'gameplay'
    ST_PAUSE = 'pause'

    def __init__(self):
        self.inputMgr = InputManager.get_instance()
        self.eventMgr = EventManager()
        self.recorder = None

        self.state = self.ST_MENU
        self.rootMenu = None

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
            * n-food: Integer, how many food should the world have at a time.
                    Default to 2.

            SnakeData: a tuple (headPos, direction, length)
            
        """
        assert self.state in self.ST_MENU
        self.configData = configData
        world = World(*configData['world-size'], eventMgr=self.eventMgr)
        self.nFood = configData.get('n-food', config.DEFAULT_FOOD_NUM)
        self.snakeDatas = configData['snakes']
        self.world = world
        # round count
        self.round = 0
        # setup rule
        if 'rule' in configData:
            Rule, args = configData['rule']
            rule = Rule(self.world, self.eventMgr, *args)
        else:
            rule = DeathModeRule(self.world, self.eventMgr)
        self.rule = rule
        # setup display
        self.display = display
        # In display, the display should bind callbacks
        # to some game events.
        display.init(self)

        self._needReset = True

    def bind_event(self, eventType, callback):
        """
        Bind the callback to events specified by `eventType`
        @eventType: The event type.
        @callback: A callable, accepting one argument, the event.
        """
        self.eventMgr.bind(eventType, callback)

    def quit(self, *args):
        self._quit = True
        self.state = self.ST_MENU

    def pause(self, event):
        pause = self.world.pause = not self.world.pause
        if self.state == self.ST_GAMEPLAY:
            self.state = self.ST_PAUSE
        elif self.state == self.ST_PAUSE:
            self.state = self.ST_GAMEPLAY

    def start(self):
        assert self.state in self.ST_MENU
        for i in xrange(self.nFood):
            self.world.gen_food()
        self.end_prepare()

    def mainloop(self):
        self._quit = False
        timer = Clock()
        tickCount = 0
        # frame per second
        FPS = config.FPS
        # update per second
        UPS = config.UPS

        # generate food
        while not self._quit:
            # handle input
            self.inputMgr.update()
            if self._quit: break
            if self.state == self.ST_GAMEPLAY:
                # update game state
                if tickCount % (FPS/UPS) == 0:
                    dprint('before update\n'+str(self.world.field))
                    if self.recorder: 
                        self.recorder.update()
                    self.rule.update()
                    self.world.update(self.eventMgr)
                    self.round += 1
            elif self.state == self.ST_MENU:
                if self.rootMenu: self.rootMenu.game_update()
            # render using display
            self.display.render(self.world)
            timer.tick(FPS)
            tickCount += 1
        # stop recorder 
        if self.recorder: 
            self.recorder.stop()
            self.recorder.quit()
        self.display.quit()
        dprint('quit normally')

    def end_prepare(self):
        assert self.state == self.ST_MENU
        self.state = self.ST_GAMEPLAY

if __name__ == '__main__':
    display = Display()
    game = Game()
    rootMenu = menu.RootMenu(game, display)
    game.mainloop()
