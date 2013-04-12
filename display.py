import pygame
import world
import grids
import imageUtils
import random
import config
from snake import Snake
from events import EventTypes
from debug import dprint

class LayerStack:
    """
    A stack of layers, to store items with
    different depths.

    """
    def __init__(self):
        self.layersSequence = []
        self.layers = {}

    def push_layer(self, layerName):
        self.layersSequence += [layerName]
        self.layers[layerName] = []

    def add_to_layer(self, layerName, item):
        self.layers[layerName].append(item)

    def size_of(self, layerName):
        return len(self.layers[layerName])

    def delete(self, item_to_del):
        for layerName in self.layersSequence:
            try:
                self.layers[layerName].remove(item_to_del)
                return
            except: pass

    def __iter__(self):
        for layerName in self.layersSequence:
            for item in self.layers[layerName]:
                yield item

class ImageFactory:
    """
    A factory of all images/sprites.
    Notice that it should better be a singleton
    """
    
    def __init__(self):
        self.container = {}

    def register(self, appearance, fname, angle=0, size=None, cd=0, loop=True, hue=0):
        """
        Link an apperance to an actual image.
        """
        img = imageUtils.Image(fname, angle, size, cd, loop, hue)
        self.container[appearance] = img

    def get_image(self, appearance):
        """
        Return a surface for an appearance
        """
        return self.container[appearance].get()

class PlayerStatus:
    def __init__(self, snake, seq, name, game):
        self.player = snake.player
        self.snake = snake
        self.seq = seq
        self.name = name
        self.game = game
        game.bind_event(EventTypes.SNAKE_DIE, self.handle_snake_die)
        game.bind_event(EventTypes.SNAKE_EAT, self.handle_snake_eat)
        game.bind_event(EventTypes.GAME_END, self.handle_snake_win)

    def handle_snake_die(self, event):
        if event.snake == self.snake:
            self.name = self.name+'-dead'
            x, y = 400, 80+self.seq*80
            effect = Effect('effect-die', x, y, 50)
            self.game.display.layerStack.add_to_layer('universe', effect)

    def handle_snake_eat(self, event):
        if event.snake == self.snake:
            x, y = 400, 80+self.seq*80
            effect = Effect('effect-eat', x, y, 30)
            self.game.display.layerStack.add_to_layer('universe', effect)

    def handle_snake_win(self, event):
        if event.winner == self.player:
            x, y = 320, 50+self.seq*80
            effect = Effect('effect-win', x, y, 100)
            self.game.display.layerStack.add_to_layer('universe', effect)

class Effect:
    def __init__(self, name, renderX, renderY, cd):
        self.name, self.renderX, self.renderY, self.cd= \
            name, renderX, renderY, cd
    
    def update_cd(self, layerStack):
        """
        @layerStack: needed in order to delete itself.
        """
        self.cd -= 1
        if self.cd <= 0: layerStack.delete(self)

class Display:
    def __init__(self, width=config.SCREEN_W, height=config.SCREEN_H):
        """
        Initialize display.
        @width: width of the stage
        @height: height of the stage
        """
        pygame.display.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((width, height), 0, 32)
        self.width = width
        self.height = height

    def init(self, game):
        self.game = game
        # TODO: Bind handlers for gameEvents here. 
        #   Interested events: SnakeBorn, SnakeEat, SnakeDie, FoodGen, FoodDisappear
        game.bind_event(EventTypes.SNAKE_BORN, self.add_snake)
        game.bind_event(EventTypes.SNAKE_DIE, self.handle_snake_die)

        # Initialize stage
        self.stageSize = 405
        self.blkSize = self.stageSize/game.world.field.height
        self.blkT = (self.blkSize, self.blkSize)
        self.stageX = 40
        self.stageY = 80

        # Initialize layer system
        self.layerStack = LayerStack()
        self.layerStack.push_layer('field')
        self.layerStack.push_layer('snakes')
        self.layerStack.push_layer('panel')
        self.layerStack.push_layer('sky')
        self.layerStack.push_layer('universe')

        # rendering callbacks
        self.renderCallbacks = {}

        # All kinds of snakes
        self.snakeHue = [
            0, 40, 100, 199, 289, 250
            ]

        # Add field
        self.add_field(game.world.field)

        # Register images for sprites
        self.imageFactory = ImageFactory()
        r = self.imageFactory.register
        r('grid-%s'%(grids.BLANK), 'img/grid-blank.png', size=self.blkT)
        r('grid-%s'%(grids.SNAKE), 'img/grid-snake.png', size=self.blkT)
        r('grid-%s'%(grids.FOOD), 'img/grid-food.png', size=self.blkT, cd=5)
        r('effect-eat', 'img/eat.png')
        r('effect-die', 'img/die.png')
        r('effect-win', 'img/win.png')

        # Add panel to its layer
        self.panel = Panel()
        self.layerStack.add_to_layer('panel', self.panel)
        r('panel', 'img/panel.png')

        # handle effects. TODO: too long
        self.renderCallbacks['effect-eat'] = self.render_effect
        self.renderCallbacks['effect-die'] = self.render_effect
        self.renderCallbacks['effect-win'] = self.render_effect

    def add_snake(self, event):
        """
        A callback to the SNAKE_BORN event.
        Add the snake to the corresponding layer.
        """
        snake = event.snake
        r = self.imageFactory.register
        name = snake.name
        self.renderCallbacks[name] = self.render_snake
        hue = self.snakeHue[self.layerStack.size_of('snakes')]
        appearance = 'snake-red'
        self.renderCallbacks[name+'-status'] = \
            self.render_status
        self.renderCallbacks[name+'-status-dead'] = \
            self.render_status
        self.layerStack.add_to_layer('sky', PlayerStatus(snake, self.layerStack.size_of('snakes'), name+'-status', self.game))
        self.layerStack.add_to_layer('snakes', snake)

        # register resources
        imgT = 'img/%s%%s.png' % appearance
        imgTurn = imgT % '-turn'
        imgNormal = imgT % ''
        imgStatus = imgT % '-status'
        imgStatusDead = imgT % '-status-dead'
        # Directions:
        #          0 (0, -1)
        #          ^
        #(-1,0)3 <   > 1 (1, 0)
        #          v
        #          2 (0, 1)
        D = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for d1, angle in zip(D, (180, 90, 0, 270)):
            # d1 = body[1] - head
            r((name, ('head', d1)), imgT % '-head', angle, self.blkT, hue=hue)
            # d1 = tail - body[-2]
            r((name, ('tail', d1)), imgT % '-tail', angle, self.blkT, hue=hue)
        # r((name, (d1, d2)), image, angle)
        # for body[i] or a snake, (d1, d2) = (body[i-1].pos - body[i].pos, body[i+1].pos - body[i].pos)
        r((name, (D[0], D[1])), imgTurn, 0, self.blkT, hue=hue)
        r((name, (D[1], D[2])), imgTurn, -90, self.blkT, hue=hue)
        r((name, (D[2], D[3])), imgTurn, -180, self.blkT, hue=hue)
        r((name, (D[3], D[0])), imgTurn, -270, self.blkT, hue=hue)
        r((name, (D[0], D[2])), imgNormal, 0, self.blkT, hue=hue)
        r((name, (D[1], D[3])), imgNormal, 90, self.blkT, hue=hue)
        # reverse
        r((name, (D[1], D[0])), imgTurn, 0, self.blkT, hue=hue)
        r((name, (D[2], D[1])), imgTurn, -90, self.blkT, hue=hue)
        r((name, (D[3], D[2])), imgTurn, -180, self.blkT, hue=hue)
        r((name, (D[0], D[3])), imgTurn, -270, self.blkT, hue=hue)
        r((name, (D[2], D[0])), imgNormal, 0, self.blkT, hue=hue)
        r((name, (D[3], D[1])), imgNormal, 90, self.blkT, hue=hue)
        # status
        r(name+'-status', imgStatus, 0, (100, 80), cd=1, loop=False, hue=hue)
        r(name+'-status-dead', imgStatusDead, hue=hue)

    def handle_snake_die(self, event):
        snake = event.snake
        self.layerStack.delete(snake)

    def blk_to_screen(self, pos):
        return (self.stageX + pos[0] * self.blkSize, 
                self.stageY + pos[1] * self.blkSize)

    def add_field(self, field):
        self.layerStack.add_to_layer('field', field)
        field.name = 'field'
        self.renderCallbacks[field.name] = self.render_field
        field.appearance = 'field'

    def render(self, world):
        """
        Render the world. This will be called at each update in main loop.
        
        @world: world to render
        """
        #
        # reset
        self.window.fill((255, 255, 255, 255))

        for item in self.layerStack:
            if self.renderCallbacks.has_key(item.name):
                self.renderCallbacks[item.name](item)
            else: self.render_fallback(item)

        pygame.display.flip()

    def quit(self):
        pass

    """
    The following are render callbacks.
    """
    def render_effect(self, objToRender):
        effect = objToRender
        self.render_fallback(effect)
        effect.update_cd(self.layerStack)

    def render_status(self, objToRender):
        status = objToRender
        g = self.imageFactory.get_image
        blit = self.window.blit

        # TODO: hard coded
        blit(g(status.name), (500, 100+status.seq*80))
        blit(pygame.font.SysFont('comic', 25).render(str(status.player.score), True, (0, 0, 0)), (560, 130+status.seq*80))

    def render_snake(self, snake):
        #self.game.world.test_snake_sync()
        body_len = len(snake.body)
        body = snake.body

        g = self.imageFactory.get_image
        blit = self.window.blit
        def diff(i, j):
            (xj, yj) = snake.body[j].pos
            (xi, yi) = snake.body[i].pos
            return (xi - xj, yi - yj)
        # Render head
        blit(g((snake.name, ('head', diff(1, 0)))), 
                self.blk_to_screen(snake.head.pos))
        # Render inner body
        for i in xrange(1, len(snake.body)-1):
            blit(g((snake.name, (diff(i-1, i), diff(i+1, i)))), 
                self.blk_to_screen(snake.body[i].pos))
        # Render tail
        blit(g((snake.name, ('tail', diff(-1, -2)))), 
            self.blk_to_screen(snake.body[-1].pos))

    def render_fallback(self, objToRender):
        """
        The default callback for rendering objects.
        The object should provide renderX and renderY.
        """
        blit = self.window.blit
        if hasattr(objToRender, 'image') and hasattr(objToRender, 'rect'):
            blit(objToRender.image, objToRender.rect)
        else:
            g = self.imageFactory.get_image
            blit(g(objToRender.name),
                (objToRender.renderX, objToRender.renderY))

    def render_field(self, objToRender):
        """
        TODO: reduce unnecessary grid rendering
        """
        field = objToRender
        for y in range(0, field.height):
            for x in range(0, field.width):
                self.window.blit(
                    self.imageFactory.get_image(
                        'grid-'+str(field.get_grid_at(x, y).type)),
                    (self.stageX+x*self.blkSize,
                        self.stageY+y*self.blkSize))


class Panel:
    def __init__(self):
        self.name = 'panel'
        self.renderX, self.renderY = 0, 0

if __name__ == "__main__":
    """
    Unit test
    """
    ls = LayerStack()
    ls.push_layer('ground')
    ls.push_layer('sky')

    print ls.layers
    print ls.layersSequence

    ls.add_to_layer('sky', 'eagle')
    ls.add_to_layer('ground', 'cow')
    ls.add_to_layer('sky', 'bird')
    ls.add_to_layer('ground', 'monkey')
    for animal in ls:
        print animal
