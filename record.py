import events
import config
import cPickle
import grids
import items
from config import RECORDER_DUMP_PATH
from events import EventTypes
from collections import OrderedDict
from player import Player
from debug import dprint

class Clip(object):
    def __init__(self, name):
        self.name = name
        self.datas = {}

    @property
    def max_round(self):
        try:
            return max(self.datas.iterkeys())
        except:
            return -1

    def add_data(self, round, data):
        if round not in self.datas:
            self.datas[round] = []
        print 'data', round, data
        self.datas[round].append(data)

    def get_datas_at(self, round):
        return self.datas.get(round, [])

class RecorderPlayer(Player):
    def __init__(self, name, clip):
        super(RecorderPlayer, self).__init__(name)
        self.clip = clip
        self.round = 0

    def update(self, world):
        for data in self.clip.get_datas_at(self.round):
            if data['type'] == EventTypes.SNAKE_MOVE and data['name'] == self.name:
                direction = data['direction']
                self.currentMove = direction
                self.snake.update_direction(direction)
                print self.round, data
                break
        self.round += 1

class Recorder(object):
    ST_PLAYING = 'playing'
    ST_RECORDING = 'recording'
    ST_STOP = 'stop'

    def __init__(self, game):
        self.game = game
        self.load()
        game.bind_event(EventTypes.SNAKE_BORN, self.handle_snake_born)
        game.bind_event(EventTypes.SNAKE_MOVE, self.handle_snake_move)
        game.bind_event(EventTypes.FOOD_GEN, self.handle_food_gen)
        game.bind_event(EventTypes.GAME_END, self.handle_game_end)
        self.bind_keys()
        self.state = self.ST_STOP
        self.clip = None

    def handle_snake_born(self, event):
        if self.state != self.ST_RECORDING: return
        snake = event.snake
        data = {'type': event.type,
                'name': snake.name,
                'body': snake.positions,
                'direction': snake.direction,
                }
        self.clip.add_data(self.game.round, data)

    def handle_snake_move(self, event):
        if self.state != self.ST_RECORDING: return
        snake = event.snake
        direction = event.to_[0] - event.from_[0], event.to_[1] - event.from_[1]
        data = {'type': event.type,
                'name': snake.name,
                'direction': direction,
                }
        self.clip.add_data(self.game.round, data)

    def handle_game_end(self, event):
        dprint('game end', event)
        self.stop()

    def handle_food_gen(self, event):
        if self.state != self.ST_RECORDING: return
        data = {'type': event.type,
                'pos': event.food.pos,
                'score': event.food.score,
                }
        self.clip.add_data(self.game.round, data)

    def play(self, clipName=None):
        self.state = self.ST_PLAYING
        if not clipName:
            clip = self.clip
        else:
            clip = self.clips[clipName]

        # TODO: test if game and display restart normally
        game = self.game
        display = game.display
        configData = self.clip.configData
        game.setup_stage(configData, display)
        game.world.forbidGenFood = True
        # game.mainloop()
        dprint('recorder play')

    def update(self):
        if self.state != self.ST_PLAYING: return

        round = self.game.round
        game = self.game
        if round > self.clip.max_round:
            self.stop()
            return
        for data in self.clip.get_datas_at(round):
            if data['type'] == EventTypes.FOOD_GEN:
                grid = game.world.field.get_grid_at(*data['pos'])
                food = items.Food(data['pos'], data['score'])
                grid.type = grids.FOOD
                grid.content = food
            elif data['type'] == EventTypes.SNAKE_BORN:
                player = RecorderPlayer(data['name'], self.clip)
                game.join_player(player)

    def record(self, clipName='default'):
        self.state = self.ST_RECORDING
        self.clip = Clip(clipName)
        self.clip.configData = self.game.configData.copy()

        dprint('record')

    def stop(self):
        if self.state == self.ST_RECORDING:
            self.clips[self.clip.name] = self.clip
        elif self.state == self.ST_PLAYING:
            game = self.game
            # player = game.world.players[0] if game.world.players else None
            # game.eventMgr.emit(events.GameEnd(player))
            game.quit()
        self.state = self.ST_STOP
        dprint('recorder stopped')

    def save(self):
        cPickle.dump(self.clips, open(RECORDER_DUMP_PATH, 'wb'), -1)

    def load(self):
        try:
            self.clips = cPickle.load(open(RECORDER_DUMP_PATH, 'rb'))
        except IOError:
            self.clips = OrderedDict()

    def bind_keys(self):
        import input
        game = self.game
        def stop(event):
            self.stop()
            game.quit(event)
        game.inputMgr.bind(input.key_down_type('q'), stop)
        # game.inputMgr.bind(input.key_down_type('q'), game.quit)
        game.inputMgr.bind(input.key_down_type('z'), lambda e: exit(0))

    def quit(self):
        self.save()

if __name__ == '__main__':
    from game import Game
    from grids import Directions
    from display import Display
    from player import HumanPlayer, AIPlayer, StupidAIPlayer, ProgramedPlayer
    import gamerule
    import input
    assert config.RECORD
    game = Game()
    display = Display()
    recorder = game.recorder = Recorder(game)
    game.setup_stage({
        'world-size': (15, 15), 
        'snakes':[ 
            ((8, 8), Directions.RIGHT, 8), 
            ((8, 11), Directions.RIGHT, 8), 
            ((8, 12), Directions.RIGHT, 8), 
            ],
        'rule': (gamerule.ScoringModeRule, (100, )),
        }, display)
    recorder.record()
    game.join_player(ProgramedPlayer('S1', 'rrrdd'))
    game.join_player(ProgramedPlayer('S2', 'rrruu'))
    # game.join_player(StupidAIPlayer('John'))
    # game.join_player(StupidAIPlayer('Kate'))
    # K = input.key
    # game.join_human_player("Fooo", [K('w'), K('s'), K('a'), K('d')])
    while 1:
        game.mainloop()
        recorder.play()
