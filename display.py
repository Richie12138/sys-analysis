import pygame
import world
import grids

# TODO cool down mechanism

class LayerStack:
    """
    A stack of layers, to store items with
    different depths.

    It adopts the iterator design pattern.
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

    #
    # Iterator design pattern
    def __iter__(self):
        self.itLayer = iter(self.layersSequence)
        self.itItem = None
        return self

    #
    # Iterator design pattern
    def next(self):
        if self.itItem == None:
            self.curLayer = self.itLayer.next()
            self.itItem = iter(self.layers[self.curLayer])
            self.curItem = self.itItem.next()
            return self.curItem
        try:
            self.curItem = self.itItem.next()
            return self.curItem
        except:
            try:
                self.curLayer = self.itLayer.next()
                self.itItem = iter(self.layers[self.curLayer])
                self.curItem = self.itItem.next()
                return self.curItem
            except:
                raise StopIteration

class ImageFactory:
    """
    A factory of all images/sprites.
    Notice that it should better be a singleton
    """
    
    def __init__(self):
        self.container = {}

    def register(self, appearance, fname, angle=0):
        """
        Link an apperance to an actual image.
        """
        self.container[appearance] = pygame.transform.rotate(pygame.image.load(fname), angle)

    def getImage(self, appearance):
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
        self.window = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

        # should be a constant
        self.blkSize = 20

    def init(self, game):
        # TODO: Bind handlers for gameEvents here.

        # Initialize layer system
        self.layerStack = LayerStack()
        self.layerStack.push_layer('field')
        #self.layerStack.push_layer('items')
        self.layerStack.push_layer('snakes')
        self.layerStack.push_layer('sky')

        # rendering callbacks
        self.renderCallbacks = {}
        self.renderCallbacks['snake'] = self.render_snake
        self.renderCallbacks['field'] = self.render_field

        # All kinds of snakes
        self.snake_appearance = [
            'snake-red',
            'snake-blue',
            'snake-green',
            ]

        # Add field
        self.add_field(game.world.field)

        # Register images for sprites
        self.imageFactory = ImageFactory()
        r = self.imageFactory.register
        r('grid-'+str(grids.BLANK), 'img/grid-blank.png')
        r('grid-'+str(grids.SNAKE), 'img/grid-snake.png')
        r('grid-'+str(grids.FOOD), 'img/grid-food.png')
        r('snake-red-1212', 'img/snake-red.png')
        r('snake-red-1010', 'img/snake-red.png', 0)
        r('snake-red-2121', 'img/snake-red.png', 90)
        r('snake-red-0101', 'img/snake-red.png', 90)

        r('snake-red-2112', 'img/snake-red-turn.png', 180)
        r('snake-red-1221', 'img/snake-red-turn.png', 0)
        r('snake-red-2110', 'img/snake-red-turn.png', 90)
        r('snake-red-1021', 'img/snake-red-turn.png', 270)

        r('snake-red-0110', 'img/snake-red-turn.png', 0)
        r('snake-red-1201', 'img/snake-red-turn.png', 90)
        r('snake-red-1001', 'img/snake-red-turn.png', 180)
        r('snake-red-0112', 'img/snake-red-turn.png', 270)

        r('snake-red-head-10', 'img/snake-red-head.png')
        r('snake-red-head-12', 'img/snake-red-head.png', 180)
        r('snake-red-head-01', 'img/snake-red-head.png', 90)
        r('snake-red-head-21', 'img/snake-red-head.png', 270)

        # TODO: Add panel to sky

        # Initialize stage
        self.fieldX = 80
        self.fieldY = 80

    def render_snake(self, objToRender):
        snake = objToRender
        body_len = len(snake.body)
        body = snake.body

        # magic numbers:
        # 1212 down down
        # 2121 right right
        # 0101 left left
        # 1010 up up

        # 1221 down right
        # 2112 right down
        # 2110 right up
        # 1021 up right
        # 0110 left up
        # 0112 left down
        # 1201 down left
        # 1001 up left

        # Render head
        self.window.blit(
            self.imageFactory.getImage(snake.appearance+'-head-'+ \
                str(snake.direction[0]+1)+str(snake.direction[1]+1)),
            (self.fieldX+snake.body[0].pos[0]*self.blkSize,
                self.fieldY+snake.body[0].pos[1]*self.blkSize))

        # Render body
        i = 1
        while i != body_len-1:
            self.window.blit(
                self.imageFactory.getImage(snake.appearance+'-'+ \
                    str(body[i].pos[0]-body[i+1].pos[0]+1)+\
                    str(body[i].pos[1]-body[i+1].pos[1]+1)+\
                    str(body[i-1].pos[0]-body[i].pos[0]+1)+\
                    str(body[i-1].pos[1]-body[i].pos[1]+1)),
                (self.fieldX+body[i].pos[0]*self.blkSize,
                    self.fieldY+body[i].pos[1]*self.blkSize))
            i += 1

    def render_field(self, objToRender):
        field = objToRender
        for y in range(0, field.height):
            for x in range(0, field.width):
                self.window.blit(
                    self.imageFactory.getImage(
                        'grid-'+str(field.get_grid_at(x, y).type)),
                    (self.fieldX+x*self.blkSize,
                        self.fieldY+y*self.blkSize))

    def add_field(self, field):
        self.layerStack.add_to_layer('field', field)
        field.name = 'field'
        field.appearance = 'field'

    def add_snake(self, snake):
        """
        Add the snake to the corresponding layer
        and assign it a name(for render purpose)
        """
        snake.name = 'snake'
        snake.appearance = self.snake_appearance[self.layerStack.size_of('snakes')]
        self.layerStack.add_to_layer('snakes', snake)

    def render(self, world):
        """
        Render the world.
        
        TODO: So now I need a callback. Where should it
        be?

        @world: world to render
        """
        #
        # reset
        self.window.fill((255, 255, 255))

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
