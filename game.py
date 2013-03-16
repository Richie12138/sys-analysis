# Author:
# Description:

from snake import Snake
from world import World
from player import Player
from display import Display

class Game:
    """
    TODO
    """
    def __init__(self, configData):
        """
        Setups the game stage.
        @configData: 
            A dict containing:
            
            * world-size: (width, height)
            * players: a list, [PlayerData1, PlayerData2, ..]

            PlayerData: a tuple, as keyLayout
            
        """
        world = World(*configData['world-size'])
        for playerData in configData['players']:
            player = Player(playerData)
            snake = Snake(world, player)
            world.add_player(player)
        self.world = world

    def bind_event(self, eventType, callback):
        """
        Bind the callback to events specified by `eventType`
        @eventType: The event type.
        @callback: A callable, accepting one argument, the event.
        """
        pass


    def mainloop(self, display):
        self.display = display
        # In display, the display should bind callbacks
        # to some game events.
        # display.init(self)

        self._quit = False
        while not self._quit:
            # handle input
            # update game state

            # render using display
            display.render(self.world)
        display.quit()

if __name__ == "__main__":
    configData = {"world-size":(10,10),
                    "players":[]}
    game = Game(configData)
    game.mainloop(Display())
