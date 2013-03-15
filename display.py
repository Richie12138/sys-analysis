import pygame

class Display:
    pass

class DefaultDisplay(Display):
    def __init__(self, width=500, height=500, blk_size=10):
    """
    Initialize display.
    @width: width of the stage
    @height: height of the stage
    """
        self.window = pygame.display.set_mode(width, height)

    def render(self, world):
    """
    Render the world.
    @world: world to render
    """
    #TODO: Layers system still not implemented.
    field = world.field
    for x in field.w:
        for y in field.h:
            # Display...
            pass

    def quit(self):
        pass
