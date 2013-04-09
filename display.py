import pygame
import world
import grids
from snake import Snake
from events import EventTypes

# TODO cool down mechanism

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

    def register(self, appearance, fname, angle=0, size=None):
        """
        Link an apperance to an actual image.
        """
        img = pygame.transform.rotate(
                pygame.image.load(fname).convert_alpha(), angle)
        if size != None:
            img = pygame.transform.scale(img, size)
        self.container[appearance] = img

    def get_image(self, appearance):
        """
        Return a surface for an appearance
        """
        return self.container[appearance]

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
        # TODO: Bind handlers for gameEvents here. 
        #   Interested events: SnakeBorn, SnakeEat, SnakeDie, FoodGen, FoodDisappear
        game.bind_event(EventTypes.SNAKE_BORN, self.add_snake)
        game.bind_event(EventTypes.SNAKE_DIE, self.handle_snake_die)

        # Initialize stage
        self.stageSize = 400
        self.blkSize = self.stageSize/game.world.field.height
        self.blkT = (self.blkSize, self.blkSize)
        self.stageX = 80
        self.stageY = 80

        # Initialize layer system
        self.layerStack = LayerStack()
        self.layerStack.push_layer('field')
        self.layerStack.push_layer('items')
        self.layerStack.push_layer('snakes')
        self.layerStack.push_layer('sky')

        # rendering callbacks
        self.renderCallbacks = {}

        # All kinds of snakes
        self.snakeAppearance = [
            'snake-red',
            'snake-red',
            'snake-blue',
            'snake-green',
            ]

        # Add field
        self.add_field(game.world.field)

        # Register images for sprites
        self.imageFactory = ImageFactory()
        r = self.imageFactory.register
        r('grid-%s'%(grids.BLANK), 'img/grid-blank.png', size=self.blkT)
        r('grid-%s'%(grids.SNAKE), 'img/grid-snake.png', size=self.blkT)
        r('grid-%s'%(grids.FOOD), 'img/grid-food.png', size=self.blkT)

        # TODO: Add panel to sky


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
        self.layerStack.add_to_layer('snakes', snake)

        # register resources
        imgT = 'img/%s%%s.png' % appearance
        imgTurn = imgT % '-turn'
        imgNormal = imgT % ''
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

    def handle_snake_die(self, event):
        snake = event.snake
        self.layerStack.delete(snake)

    def blk_to_screen(self, pos):
        return (self.stageX + pos[0] * self.blkSize, 
                self.stageY + pos[1] * self.blkSize)

    def render_snake(self, snake):
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

    def render_field(self, objToRender):
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
            self.renderCallbacks[item.name](item)

        pygame.display.flip()

    def quit(self):
        pass

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
