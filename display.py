import pygame
import world
import grids

# TODO build a factory for sprites

class LayerStack:
    """
    A stack of layers, to store items with
    different depths.

    TODO: make it iteratable
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

    def __iter__(self):
        self.itLayer = iter(self.layersSequence)
        self.itItem = None
        return self

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

    def register(self, appearance, fname):
        """
        Link an apperance to an actual image.
        """
        self.container[appearance] = pygame.image.load(fname)

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
        self.layerStack.push_layer('items')
        self.layerStack.push_layer('snakes')
        self.layerStack.push_layer('sky')

        # rendering callbacks
        self.renderCallbacks = {}
        self.renderCallbacks['snake'] = self.render_snake
        self.renderCallbacks['field'] = self.render_field

        # All kinds of snakes
        self.snake_apperance = [
            'snake-red',
            'snake-blue',
            'snake-green',
            ]

        # Add field
        self.add_field(game.world.field)

        # Init images
        self.imageFactory = ImageFactory()
        self.imageFactory.register('grid-'+str(grids.BLANK), 'img/grid-blank.png')
        self.imageFactory.register('grid-'+str(grids.SNAKE), 'img/grid-snake.png')
        self.imageFactory.register('grid-'+str(grids.FOOD), 'img/grid-food.png')

        # TODO: Add panel to sky

        # Initialize stage
        self.fieldX = 80
        self.fieldY = 80

    def render_snake(self, objToRender):
        # TODO: render a snake
        snake = objToRender
        body_len = len(snake.body)

    def render_field(self, objToRender):
        # TODO: render a field
        field = objToRender
        for y in range(0, field.height):
            for x in range(0, field.width):
                self.window.blit(
                    self.imageFactory.get_image(
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
        self.layerStack.add_to_layer('snakes', snake)
        snake.name = 'snake'
        snake.apperance = self.snake_apperance[self.layerStack.size_of('snakes')]

    def render(self, world):
        """
        Render the world. This will be called at each update in main loop.
        
        @world: world to render
        """
        #
        # reset
        self.window.fill((255, 255, 255))

        # XXX: Why renderCallbacks? Things should be rendered layer by layer.
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
