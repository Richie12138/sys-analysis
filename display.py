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
        self.layersSequence += layerName
        self.layers[layername] = []

    def add_to_layer(self, layerName, item):
        self.layers[layerName].append(item)

    def size_of(self, layerName):
        return len(self.layers[layerName])

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
        # TODO
        pass

    def getImage(self, appearance)
    """
    Return a surface for an appearance
    """
        # TODO
        pass

class Display:
    def __init__(self, width=500, height=500):
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
        self.renderCallbacks['snake'] = self.render_for_snake
        self.renderCallbacks['field'] = self.render_for_field

        # All kinds of snakes
        self.snake_apperance = [
            'snake-red',
            'snake-blue',
            'snake-green',
            ]

        # Add field
        self.add_field(game.world.field)

        # TODO: Add panel to sky

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
    world = world.World(10, 10)
    display = Display(blkSize=10)
    while True:
        display.render(world)
