import pygame

class Player:
    pass

class HumanPlayer(Player):
    def __init__(self, mgr, keyLayout):
        """
        Initialize the player, including his keyboard layout
        Parameters:
        @keyLayout: a list of keys for up, down, left, right,
                    respectively
        @mgr: a instance of InputManager
        """
        self.mgr = mgr
        direction = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.keyLayout = {i:j for i, j in zip(keyLayout, direction)}
        self.currentMove = None
        self.bind_keys(keyLayout) #bind its key event to the inputmanager
        self.historyKeyPressed = [] #used to record the history of the currentKeypressed

    def move(self, event):
        """
        The callback of a player key event
        Used to update the player's currentMove
        Parameters:
        @event: the event corresponding to the callback function
        """
        if event.type == pygame.KEYDOWN:
            self.currentMove = self.keyLayout[event.key]
            self.historyKeyPressed.append(event.key)

        elif event.type == pygame.KEYUP:
            #If it's a KEYUP, the withdraw a key from historyKeyPressed
            self.historyKeyPressed.pop()
            if len(self.historyKeyPressed):
                self.currentMove = self.keyLayout[self.historyKeyPressed[-1]]
            else:
                self.currentMove = None

        print self.currentMove

    def bind_keys(self, keyLayout):
        """
        Blind its keyLayout to the inputManager
        Parameters:
        @keyLayout: a list of keys for up, down, left, right,
            respectively
            eg: keyLayout = [K_w, K_s, K_a, K_d]
        """
        for key in keyLayout:
            self.mgr.bind((pygame.KEYDOWN, key), self.move)
            self.mgr.bind((pygame.KEYUP, key), self.move)


class AIPlayer(Player):
    pass
