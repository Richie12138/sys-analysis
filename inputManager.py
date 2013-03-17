import pygame
from player import Player


class InputManager:
    '''InputManager maintains a list of current-pressed keys as a stack
    and guarantee there's no duplicate
    '''
    def __init__(self):
        self.currentKeyPressed = []

    def update(self):
        '''
        Listen to the key event in the pygame.event.
        '''
        self.currentKeyPressed = []

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #duplicate are n)ot allowed
                if event.unicode not in self.currentKeyPressed:
                    self.currentKeyPressed = \
                        [event.unicode]+self.currentKeyPressed

# Test
# ===============================
# if __name__ == "__main__":
#   FPS = 30
#   pygame.display.init()
#   screen = pygame.display.set_mode((320, 640),0,32)
#   clocks = pygame.time.Clock()
# 
#   player1 = Player((K_w, K_s, K_a, K_d))
#   player2 = Player((K_UP, K_DOWN, K_LEFT, K_RIGHT))
# 
#   players = [player1, player2]
#   input_manager = inputManager()
# 
#   while True:
#       input_manager.key_listener()
#       pygame.font.init()
#       screen.fill((255,255,255,255))  
#       xy = [5,5]
#       fontr = pygame.font.SysFont("arial", 12)
#       for i in xrange(0, len(players)):
#           players[i].update(input_manager.currentKeyPressed)
#       for i in xrange(0, len(players)):
#           players[i].test(screen,i, xy, fontr)
#           xy[1] += 35
# 
#       # clocks.tick(FPS)
#       pygame.display.update()
# 
