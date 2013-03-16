import pygame
import world
import grids

class Display:
    def __init__(self, width=500, height=500, blk_size=10):
        """
        Initialize display.
        @width: width of the stage
        @height: height of the stage
        """
        self.window = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.blk_size = blk_size

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
        self.field_x = (self.width-field.width*self.blk_size)/2
        self.field_y = (self.height-field.height*self.blk_size)/2

        for x in range(field.width):
            for y in range(field.height):
                #
                # grey for blank grids
                if field.get_grid_at(x, y).type == grids.BLANK:
                    pygame.draw.rect(self.window,
                                (200, 200, 200),
                                (self.field_x+x*self.blk_size,
                                    self.field_y+y*self.blk_size,
                                    self.blk_size-1,
                                    self.blk_size-1))
                #
                # yellow for snake
                elif field.get_grid_at(x, y).type == grids.SNAKE:
                    pygame.draw.rect(self.window,
                                (255, 255, 0),
                                (self.field_x+x*self.blk_size,
                                    self.field_y+y*self.blk_size,
                                    self.blk_size-1,
                                    self.blk_size-1))
                #
                # red for food
                elif field.get_grid_at(x, y).type == grids.FOOD:
                    pygame.draw.rect(self.window,
                                (255, 255, 0),
                                (self.field_x+x*self.blk_size,
                                    self.field_y+y*self.blk_size,
                                    self.blk_size-1,
                                    self.blk_size-1))
                    print x, y
                    
                pass
        pygame.display.flip()

    def quit(self):
        pass

if __name__ == "__main__":
    world = world.World(10, 10)
    display = Display(blk_size=10)
    while True:
        display.render(world)
