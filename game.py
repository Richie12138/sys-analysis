# Author:
# Description:

from snake import Snake, Directions
from world import World
from player import HumanPlayer
from display import Display
from inputManager import InputManager

class Game:
    """
    TODO
    """
    def __init__(self):
        self.inputManager = InputManager()

    def setup_stage(self, configData):
        """
        Setups the game stage.
        @configData: 
            A dict containing:
            
            * world-size: (width, height)
            * players: a list, [PlayerData1, PlayerData2, ..]

            PlayerData: a tuple, as keyLayout
            
        """
        world = World(*configData['world-size'])
        for playerData in configData['human-players']:
            player = HumanPlayer(*playerData, 
                inputManager=self.inputManager)
            snake = Snake(world, player)
            snake.gen_body((3, 1), Directions.RIGHT, 3)
            world.field.gen_snake_grids(snake)
            world.players += [player]
            world.snakes += [snake]

        for playerData in configData['ai-players']:
            player = AIPlayer(*playerData)
            snake = Snake(world, player)
            snake.gen_body((0, 0), Directions.RIGHT, 3)
            world.field.gen_snake_grids(snake)
            world.players += [player]
            world.snakes += [snake]

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
            self.inputManager.update()

            # update game state
            self.world.update()

            # render using display
            display.render(self.world)
        display.quit()

if __name__ == "__main__":
    configData = {"world-size":(10,10),
                    "human-players":[[['W','S','A','D']]],
                    "ai-players":[]}
    game = Game()
    game.setup_stage(configData)
    game.mainloop(Display())
