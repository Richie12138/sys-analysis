import pygame
from grids import Directions
import grids
from debug import dprint
import copy

class Player(object):
    def __init__(self, name):
        self.name = name
        self.snake = None
        self.currentMove = None
        self.score = 0

    def update(self, world):
        pass

    def __repr__(self):
        return '{self.__class__.__name__}({self.name}, currentMove={self.currentMove}'.format(
                self=self)

class HumanPlayer(Player):
    def __init__(self, name, mgr, keyLayout):
        """
        Initialize the player, including his keyboard layout
        Parameters:
        @keyLayout: a list of keys for up, down, left, right,
                    respectively. You can get these values by `input.key`.
        @mgr: a instance of InputManager

        self Paramater:
        @self.currentMove:
            A string corresponding to 'UP', 'DOWN', 'LEFT', 'RIGHT'
            refer to the Player currentMove direction
        @self keyLayout:
            A dict, which key its the key layout of the player
            and the corresponding value is the direction to the key layout
            eg:
            { K_w: 'UP',
              K_s: 'DOWN',
              K_a: 'LEFT',
              K_d: 'RIGHT'
            }

        @self.historyKeyPressed
            A list used to record the history of the key still being pressed
        """
        super(HumanPlayer, self).__init__(name)
        self.mgr = mgr
        direction = [Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]
        self.keyLayout = {i:j for i, j in zip(keyLayout, direction)}
        self.bind_keys(keyLayout) #bind its key event to the inputmanager
        self.historyKeyPressed = [] 

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
            # dprint('KEYDOWN:', event.key)

        elif event.type == pygame.KEYUP:
            #If it's a KEYUP, the withdraw a key from historyKeyPressed
            # self.historyKeyPressed.pop()
            self.historyKeyPressed.remove(event.key)
            if len(self.historyKeyPressed):
                self.currentMove = self.keyLayout[self.historyKeyPressed[-1]]
            else:
                self.currentMove = None
        if self.currentMove and self.snake.alive:
            self.snake.update_direction(self.currentMove)
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
    def __init__(self,name ):
        super(AIPlayer, self).__init__(name)

    def get_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_current_moveable_grid(self, head, depth, visited):
        currentMoveableGrid = [] 
        for dir in Directions.all:
            nextStep = (head.pos[0] + dir[0], head.pos[1] + dir[1])
            grid = self.world.field.get_grid_at(*nextStep)
            if grid != None and grid.pos not in visited:
                for i in self.enemySnake:
                    if self.get_distance(i.head.pos, grid.pos) != 1:
                        if grid.type == grids.BLANK and grid.content == None:
                            currentMoveableGrid.append(grid)
                        elif grid.type == grids.FOOD:
                            currentMoveableGrid.append(grid)
                # elif depth != 0:
                #     if depth > len(self.snake.body):
                #         depth = 0
                #     for i in self.snake.body[-1*depth ::]:
                #         if i.pos == grid.pos:
                #             currentMoveableGrid.append(grid)

        return currentMoveableGrid

    def seed_fill(self, grid):
        fillNum = 0
        visited = {grid.pos}
        depth = 0
        stack = [grid]
        while stack:
            myGrid = stack.pop()
            depth += 1
            fillNum +=1
            currentMoveableGrid = self.get_current_moveable_grid(myGrid, depth, visited)
            # print "currentMoveableGrid", len(currentMoveableGrid)
            if len(currentMoveableGrid):
                for i in currentMoveableGrid:
                    visited.add(i.pos)
                    stack.append(i)
            else:
                depth -=1
        
        # count the fillNum was equal to the blank grid or not
        # blankNum = self.world.field.height * self.world.field.width - len(self.snake.body)
        blankNum = len(self.world.field.fields)
        blankNum = blankNum - len(self.snake.body)

        if fillNum == blankNum:
            return fillNum, True
        else:
            dir = (grid.pos[0] - self.snake.head.pos[0], grid.pos[1] - self.snake.head.pos[1], )
            print "expect: %d but got %d,  dir in %s" %(blankNum, fillNum, str(dir))
            currentMoveableGrid = self.get_current_moveable_grid(self.snake.head, 0, set())
            print "currentMoveableGrid: ", currentMoveableGrid
            print 'grid', grid
            #self.world.test_snake_sync()
            #print self.world
            return fillNum, False

    def update(self, world):
        if not self.snake.alive:
            return
        self.world = world
        self.enemySnake = [i for i in self.world.snakes if i != self.snake]
        tempMoveableGrid = self.get_current_moveable_grid(self.snake.head, 0, set())
        num, candidate = -1, None 
        currentMoveableGrid = []
        distance = 100000
        food = world.foods[0]

        for grid in tempMoveableGrid:
            fillNum, isOk = self.seed_fill(grid)
            if fillNum > num:
                num = fillNum
                candidate = grid
                distance = abs(grid.pos[0] - food.pos[0]) + \
                    abs(grid.pos[1] - food.pos[1])

            elif fillNum == num:
                temp_d = abs(grid.pos[0] - food.pos[0]) + \
                    abs(grid.pos[1] - food.pos[1])
                if temp_d < distance:
                    num = fillNum
                    candidate = grid

            self.currentMove = (candidate.pos[0] - self.snake.head.pos[0], candidate.pos[1] - self.snake.head.pos[1])
            self.snake.update_direction(self.currentMove)

 
class StupidAIPlayer(Player):
    def dist(self, pos1, pos2):
        return abs(pos1[0]-pos2[0]) + abs(pos1[1] - pos2[1])

    def grid_is_ok(self, pos, depth):
        grid = self.world.field.get_grid_at(*pos)
        return grid is not None and grid.type in (grids.BLANK, grids.FOOD)

    def update(self, world):
        if not self.snake.alive:
            return 
        headPos = self.snake.head.pos
        self.world = world
        food = min((self.dist(f.pos, headPos), f) for f in world.foods)[1]
        prev = {}
        stk = [(0, headPos)]
        vis = set()
        while stk:
            d1, p1 = stk.pop(0)
            if p1 == food.pos:
                break
            for dx, dy in Directions.all:
                p2 = p1[0] + dx, p1[1] + dy
                if p2 in vis: continue
                d2 = d1 + 1
                if self.grid_is_ok(p2, d2):
                    stk.append((d2, p2))
                    prev[p2] = p1
                    vis.add(p2)
        p = food.pos
        path = []
        while p in prev:
            path.append(p)
            p = prev[p]
        if len(path) > 0:
            p = path[-1]
            self.currentMove = (p[0] - headPos[0], p[1] - headPos[1])
        else:
            p1 = headPos
            for dx, dy in Directions.all:
                p2 = p1[0] + dx, p1[1] + dy
                if self.grid_is_ok(p2, 0):
                    self.currentMove = dx, dy
                    break
        self.snake.update_direction(self.currentMove)

class ProgramedPlayer(Player):
    Mapping = {'u': Directions.UP, 'd': Directions.DOWN, 'l': Directions.LEFT, 'r': Directions.RIGHT}
    def __init__(self, name, actions):
        super(ProgramedPlayer, self).__init__(name)
        self.round = 0
        self.actions = actions.lower()

    def update(self, world):
        if not self.snake.alive: return
        self.currentMove = self.Mapping[self.actions[self.round]]
        self.snake.update_direction(self.currentMove)
        self.round += 1
        if self.round == len(self.actions):
            self.round = 0
