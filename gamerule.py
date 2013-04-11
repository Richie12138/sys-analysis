from events import GameEnd
from debug import dprint

class GameRule(object):
    def __init__(self, world, eventMgr):
        self.world = world
        self.eventMgr = eventMgr
        self.end = False
        self.round = 0

    def set_winner(self, player):
        self.eventMgr.emit(GameEnd(winner=player))
        self.end = True

    def update(self):
        """
        Update the checker
        """
        self.round += 1

class DeathModeRule(GameRule):
    def update(self):
        super(DeathModeRule, self).update()
        if self.end: return
        aliveSnakes = [snake for snake in self.world.snakes if snake.alive]
        if len(aliveSnakes) == 1:
            self.set_winner(aliveSnakes[0].player)

class FixedRoundModeRule(DeathModeRule):
    def __init__(self, world, eventMgr, round):
        super(FixedRoundModeRule, self).__init__(world, eventMgr)
        self.maxRound = round

    def update(self):
        super(FixedRoundModeRule, self).update()
        if self.end: return
        if self.round == self.maxRound:
            self.set_winner(max(self.world.players, 
                    key=lambda p:p.score if p.snake.alive else None))

class ScoringModeRule(GameRule):
    def __init__(self, world, eventMgr, winScore):
        super(ScoringModeRule, self).__init__(world, eventMgr)
        self.winScore = winScore

    def update(self):
        super(ScoringModeRule, self).update()
        if self.end: return
        # dprint(self.world.players)
        player = max(self.world.players, 
                key=lambda p: p.score if p.snake.alive else None)
        if player.score >= self.winScore:
            self.set_winner(player)

