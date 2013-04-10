import pygame
import world
import grids
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

    def register(self, appearance, fname, angle=0, size=None, cd=0, loop=True):
        """
        Link an apperance to an actual image.

        Warning: If size is not None then it may be
        an animation, and therefore the image is
        assumed to be a squre!
        """
        img = Image(fname, angle, size, cd, loop)
        self.container[appearance] = img

    def get_image(self, appearance):
        """
        Return a surface for an appearance
        """
        return self.container[appearance].get()

class Image:
    """
    A container for image. This class
    also support animation.
    """

    def __init__(self, fname, angle, size, cd, loop):
        self.img = pygame.transform.rotate(
                pygame.image.load(fname).convert_alpha(), angle)
        self.max_cd = cd
        self.loop = loop
        self.cd = 0
        if size != None:
            # 900*80/(100*80)
            self.nCells = self.img.get_width()*size[1]/ \
                (size[0]*self.img.get_height())
            self.size = size
            self.curCell = 0
            self.img = pygame.transform.scale(self.img,
                (self.img.get_width()*size[1]/self.img.get_height(),
                    size[1]))
        else:
            self.size = (self.img.get_width(), self.img.get_height())
            self.nCells, self.curCell = 1, 0

    def get(self):
        val = self.img.subsurface(self.curCell*self.size[0], 0, self.size[0], self.size[1])
        if self.max_cd != 0:
            self.cd = (self.cd + 1) % self.max_cd
            if self.cd == 0:
                if self.loop == False and self.curCell == self.nCells-1:
                    pass
                else: self.curCell = (self.curCell + 1)%self.nCells
        return val

class PlayerStatus:
    def __init__(self, snake, seq, name):
        self.player = snake.player
        self.seq = seq
        self.name = name

class Display:
    def __init__(self, width=600, height=600):
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
        self.snakeAppearance = [
            'snake-red',
            'snake-blue',
            'snake-purple',
            'snake-blue',
            ]

        # Add field
        self.add_field(game.world.field)

        # Register images for sprites
        self.imageFactory = ImageFactory()
        r = self.imageFactory.register
        r('grid-%s'%(grids.BLANK), 'img/grid-blank.png', size=self.blkT)
        r('grid-%s'%(grids.SNAKE), 'img/grid-snake.png', size=self.blkT)
        r('grid-%s'%(grids.FOOD), 'img/grid-food.png', size=self.blkT, cd=5)

        # Add panel to its layer
        self.panel = Panel()
        self.layerStack.add_to_layer('panel', self.panel)
        r('panel', 'img/panel.png')

    def add_snake(self, event):
        """
        A callback to the SNAKE_BORN event.
        Add the snake to the corresponding layer.
        """
        snake = event.snake
        r = self.imageFactory.register
        name = snake.name
        self.renderCallbacks[name] = self.render_snake
        # image path template
        appearance = self.snakeAppearance[self.layerStack.size_of('snakes')]
        self.renderCallbacks[appearance+'-status'] = \
            self.render_status
        self.layerStack.add_to_layer('sky', PlayerStatus(snake, self.layerStack.size_of('snakes'), appearance+'-status'))
        self.layerStack.add_to_layer('snakes', snake)

        # register resources
        imgT = 'img/%s%%s.png' % appearance
        imgTurn = imgT % '-turn'
        imgNormal = imgT % ''
        imgStatus = imgT % '-status'
        # Directions:
        #          0 (0, -1)
        #          ^
        #(-1,0)3 <   > 1 (1, 0)
        #          v
        #          2 (0, 1)
        D = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for d1, angle in zip(D, (180, 90, 0, 270)):
            # d1 = body[1] - head
            r((name, ('head', d1)), imgT % '-head', angle, self.blkT)
            # d1 = tail - body[-2]
            r((name, ('tail', d1)), imgT % '-tail', angle, self.blkT)
        # r((name, (d1, d2)), image, angle)
        # for body[i] or a snake, (d1, d2) = (body[i-1].pos - body[i].pos, body[i+1].pos - body[i].pos)
        r((name, (D[0], D[1])), imgTurn, 0, self.blkT)
        r((name, (D[1], D[2])), imgTurn, -90, self.blkT)
        r((name, (D[2], D[3])), imgTurn, -180, self.blkT)
        r((name, (D[3], D[0])), imgTurn, -270, self.blkT)
        r((name, (D[0], D[2])), imgNormal, 0, self.blkT)
        r((name, (D[1], D[3])), imgNormal, 90, self.blkT)
        # reverse
        r((name, (D[1], D[0])), imgTurn, 0, self.blkT)
        r((name, (D[2], D[1])), imgTurn, -90, self.blkT)
        r((name, (D[3], D[2])), imgTurn, -180, self.blkT)
        r((name, (D[0], D[3])), imgTurn, -270, self.blkT)
        r((name, (D[2], D[0])), imgNormal, 0, self.blkT)
        r((name, (D[3], D[1])), imgNormal, 90, self.blkT)
        # status
        r(appearance+'-status', imgStatus, 0, (100, 80), cd=1, loop=False)

    def handle_snake_die(self, event):
        snake = event.snake
        self.layerStack.delete(snake)

    def blk_to_screen(self, pos):
        return (self.stageX + pos[0] * self.blkSize, 
                self.stageY + pos[1] * self.blkSize)

    def render_status(self, status):
        g = self.imageFactory.get_image
        blit = self.window.blit

        # TODO: hard coded
        blit(g(status.name), (500, 100+status.seq*80))
        blit(pygame.font.SysFont('comic', 25).render(str(status.player.score), True, (0, 0, 0)), (560, 130+status.seq*80))

    def render_snake(self, snake):
        self.game.world.test_snake_sync()
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
        """
        blit = self.window.blit
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
