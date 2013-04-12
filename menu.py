import config
import re
import pygame
import math
import random
import crayonstroke
import input
import gamerule
from input import InputManager
from grids import Directions
from player import HumanPlayer, AIPlayer, StupidAIPlayer, ProgramedPlayer

pygame.display.init()
pygame.font.init()

class Context(object):
    def __init__(self, root):
        self.root = root
        self.current = root
        self.stack = []

    @property
    def parent(self):
        if self.stack:
            return self.stack[-1]
        else:
            return None

    def handle_key(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.current.update_input('\b')
        elif event.key == pygame.K_RETURN:
            choice = self.current.choice
            if choice:
                self.goto(choice)
            else:
                self.current.back(ctx)
                self.goback()
        elif event.unicode:
            self.current.update_input(event.unicode)

    def goback(self):
        if self.stack:
            self.current = self.stack.pop()
        return self

    def goto(self, menu):
        self.stack.append(self.current)
        self.current = menu
        self.current.enter(self)
        return self

class Menu(object):
    """
    Add cancel automatically
    """
    DeltaT = 1. / config.FPS
    FontSize = 22
    BaseFontSize = 40
    font = pygame.font.SysFont('Comic Sans MS', FontSize, bold=True)
    baseFont = pygame.font.SysFont('Comic Sans MS', BaseFontSize, bold=True)

    def __init__(self, name, subMenus=[], callback=None, cancel=True):
        self.name = name.upper()
        self.callback = callback
        self.subMenus = subMenus[:]
        if cancel and not callback:
            self.subMenus.append(Cancel('cancel'))

        self.string = ''
        self.update_input('')

    @property
    def choice(self):
        if self.matched:
            return self.matched[0][0]
        else:
            return None

    def back(self, ctx):
        pass

    def enter(self, ctx):
        # TODO: some animation
        if self.callback:
            self.callback(ctx)
            ctx.goback()

    def update_input(self, char):
        if char == '\b':
            self.string = self.string[:-1]
        else:
            self.string += char
        try:
            patt = re.compile(self.string, re.I)
        except:
            patt = re.compile(r'T_T\.no match')
        matched = []
        for sm in self.subMenus:
            match = patt.match(sm.name)
            if match:
                matched.append((sm, match))
        self.matched = matched

    def render(self, surface):
        # center
        cx, cy = surface.get_size()[0]/2, 300
        # base radius
        R0 = 190
        # sub radius
        R1 = 30
        # start angle
        a0 = - math.pi / 2
        # fill color
        color = (109, 222, 100, 188)
        colorSub = (221, 158, 164, 188)
        colorText = (50, 43, 67)
        colorMatchedText = (189, 39, 85)
        font = self.font
        # draw base circle
        crayonstroke.circle(surface, (cx, cy), R0 + random.randint(-5, 5), color)
        txt = self.baseFont.render(self.name + ': '+ self.string, 1, colorText)
        w, h = txt.get_size()
        surface.blit(txt, (cx - w/2, cy - h/2))
        # n-sub
        nSub = len(self.matched)
        if nSub:
            # delta angle
            da = math.pi * 2 / nSub
            # draw sub circles
            a = a0
            for sm, match in self.matched:
                x, y = (cx + R0 * math.cos(a),
                        cy + R0 * math.sin(a))
                txtMatched = font.render(
                        match.string[:match.end()], 1, colorMatchedText)
                txtRest = font.render(
                        match.string[match.end():], 1, colorText)
                w, h = self.font.size(match.string)
                R = max(R1, max(w, h)/2 + 10)
                crayonstroke.circle(surface, (x, y), R + random.randint(-2, 2), colorSub)
                surface.blit(txtMatched, (x - w/2, y - h/2))
                surface.blit(txtRest, (x - w/2 + txtMatched.get_size()[0], y - h/2))
                a += da

    def update(self):
        dt = self.DeltaT

class Cancel(Menu):
    def __init__(self, name):
        super(Cancel, self).__init__(name, callback=self.callback)

    def callback(self, ctx):
        ctx.goback().goback()

class InputBox(Menu):
    def __init__(self, name, default=''):
        super(InputBox, self).__init__(name, [], cancel=False)
        self.string = default

    def back(self, ctx):
        pass

class Choices(Menu):
    def __init__(self, name, options):
        super(Choices, self).__init__(name, options)

class Option(Menu):
    def __init__(self, name, callback):
        super(Option, self).__init__(name, callback=callback)

    def enter(self, ctx):
        super(Option, self).enter(ctx)
        ctx.goback().goback()

class ReplayRecord(Menu):
    def __init__(self, name):
        super(ReplayRecord, self).__init__(name, [])

class Help(Menu):
    def __init__(self, name):
        super(Help, self).__init__(name, [])

class RootMenu(Menu):
    def __init__(self, game, display):
        self.game = game
        game.rootMenu = self
        self.display = display
        # setup menu stage
        self.setup_empty_stage()

        self.image = pygame.Surface((config.SCREEN_W, config.SCREEN_H)).convert_alpha()
        self.rect = (0, 0)

        K = input.key

        def record_on(ctx): config.RECORD = 1
        def record_off(ctx): config.RECORD = 0
        def play_human_vs_AI(ctx):
            game.setup_stage({
                'world-size':(16, 16), 
                'snakes': [
                    ((8, 8), Directions.RIGHT, 5), 
                    ((7, 7), Directions.RIGHT, 5), 
                    ],
                'rule': rule[0],
                }, display)
            game.join_human_player("Player", [K('w'), K('s'), K('a'), K('d')])
            game.join_player(AIPlayer("AI Player"))
            game.start()

        def play_human_vs_human(ctx):
            game.setup_stage({
                'world-size':(16, 16), 
                'snakes': [
                    ((8, 8), Directions.RIGHT, 5), 
                    ((7, 7), Directions.RIGHT, 5), 
                    ],
                'rule': rule[0],
                }, display)
            game.join_human_player("Foo", [K('w'), K('s'), K('a'), K('d')])
            game.join_human_player("Bar", [K('i'), K('k'), K('j'), K('l')])
            game.start()

        play_4_AI = play_AI_vs_AI = play_human_vs_human

        # def play_AI_vs_AI(ctx):
        #     pass

        # def play_4_AI(ctx):
        #     pass

        rule = [(gamerule.DeathModeRule, ())]
        def mode_set(mode, args):
            def setter(ctx):
                rule[0] = (mode, args)
            return setter
                
        super(RootMenu, self).__init__('$>', [
            Menu('play', [
                Menu('1: human v.s. AI', [], callback=play_human_vs_AI),
                Menu('2: human v.s. human', [], callback=play_human_vs_human),
                Menu('3: AI v.s. AI', [], callback=play_AI_vs_AI),
                Menu('4: 4 AI', [], callback=play_4_AI),
                ]),
            Choices('game rule', [
                Option('death mode', callback=mode_set(gamerule.DeathModeRule, ())),
                Option('scoring mode', callback=mode_set(gamerule.ScoringModeRule, (30,))),
                Option('fixed round mode', callback=mode_set(gamerule.FixedRoundModeRule, (128,))),
                ]),
            Help('help'),
            Choices('set record', [
                Option('record on', callback=record_on),
                Option('record off', callback=record_off),
                ]),
            InputBox('record'),
            ReplayRecord('replays'),
            Choices('quit', [
                Option('confirm', callback=lambda ctx: exit(0)),
                ])
        ], cancel=False)
        self.ctx = Context(self)
        # bind keys
        inputMgr = InputManager.get_instance()
        def handle_key(event):
            if game.state == game.ST_MENU:
                self.ctx.handle_key(event)

        inputMgr.bind(input.key_down_type(), handle_key)
        def escape(event):
            if game.state != game.ST_MENU:
                game.quit()
            else:
                exit(0)

        inputMgr.bind(input.key_down_type('ESCAPE'), escape)
        def back_to_menu(event):
            self.setup_empty_stage()

        inputMgr.bind(input.key_down_type('HOME'), back_to_menu)

    def setup_empty_stage(self):
        game = self.game
        display = self.display
        game.state = game.ST_MENU
        game.setup_stage({
            'world-size':(20, 20), 
            'snakes': [
                ]
            }, display)
        display.layerStack.add_to_layer('universe', self)
        display.imageFactory.register('menu-bg', 'img/menu-bg.png')
        background = display.imageFactory.container['menu-bg']
        background.name = 'menu-bg'
        background.renderX, background.renderY = 0, 0
        display.layerStack.add_to_layer('sky', background)

    def game_update(self):
        if self.game.state != self.game.ST_MENU:
            return
        self.ctx.current.update()
        self.image.fill((0xff, 0xff, 0xff, 0))
        self.ctx.current.render(self.image)

if __name__ == '__main__':
    import input
    import os
    screen = pygame.display.set_mode((600, 600))

    callback = lambda ctx: 0
    inputMgr = input.InputManager()
    root = RootMenu(None)

    tm = pygame.time.Clock()
    while 1:
        inputMgr.update()
        # os.system('clear')
        screen.fill((0xff, 0xff, 0xff))
        ctx.current.render(screen)
        pygame.display.update()
        tm.tick(10)
