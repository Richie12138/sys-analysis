import pygame
import world
import grids

class Display:
    def __init__(self, width=500, height=500, blkSize=10):
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
        self.blkSize = blkSize
        # XXX: see comment near self.clock.tick
        # self.clock = pygame.time.Clock()

    def init(self, game):
        # TODO: Bind handlers for gameEvents here.
        pass

    def render(self, world):
        """
        Render the world.
        @world: world to render
        """
        #
        # reset
        self.window.fill((255, 255, 255))

        #TODO: Layers system still not implemented.
        field = world.field
        #
        # Place the field in the screen
        # The field should be smaller than the screen
        self.fieldX = (self.width-field.width*self.blkSize)/2
        self.fieldY = (self.height-field.height*self.blkSize)/2

        for x in xrange(field.width):
            for y in xrange(field.height):
                #
                # grey for blank grids
                if field.get_grid_at(x, y).type == grids.BLANK:
                    pygame.draw.rect(self.window,
                                (200, 200, 200),
                                (self.fieldX+x*self.blkSize,
                                    self.fieldY+y*self.blkSize,
                                    self.blkSize-1,
                                    self.blkSize-1))
                #
                # yellow for snake
                elif field.get_grid_at(x, y).type == grids.SNAKE:
                    pygame.draw.rect(self.window,
                                (255, 255, 0),
                                (self.fieldX+x*self.blkSize,
                                    self.fieldY+y*self.blkSize,
                                    self.blkSize-1,
                                    self.blkSize-1))
                #
                # red for food
                elif field.get_grid_at(x, y).type == grids.FOOD:
                    pygame.draw.rect(self.window,
                                (255, 255, 0),
                                (self.fieldX+x*self.blkSize,
                                    self.fieldY+y*self.blkSize,
                                    self.blkSize-1,
                                    self.blkSize-1))
                    print x, y
                    
        # XXX: tick was migrated to game.py
        # self.clock.tick(1)
        pygame.display.flip()

    def quit(self):
        pass

if __name__ == "__main__":
    world = world.World(10, 10)
    display = Display(blkSize=10)
    while True:
        display.render(world)
