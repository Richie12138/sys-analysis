import pygame
from grids import Directions
import grids
from debug import dprint
import copy
import random

direction = {(-1, 0):"LEFT",
        (1, 0): "RIGHT",
        (0, -1):"UP",
        (0, 1):"DOWN"}

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

        self Paramater: @self.currentMove:
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

            if grid != None and grid.pos not in visited and grid.pos != self.snake.head.pos :
                flag = True
                if depth < 0 and grid == self.snake.lastTail:
                    flag = False
                if grid.type == grids.BLANK and flag:
                   currentMoveableGrid.append(grid)
                elif grid.type == grids.FOOD:
                   currentMoveableGrid.append(grid)
                elif depth > 0:
                    if depth >= len(self.snake.body):
                       depth = 0
                    for i in self.snake.body[-1*depth ::]:
                        if i.pos == grid.pos:
                           currentMoveableGrid.append(grid)

                if len(self.enemySnake):
                    for i in self.enemySnake:
                        if grid in currentMoveableGrid and self.get_distance(i.head.pos, grid.pos) == 1:
                            currentMoveableGrid.remove(grid)

        return currentMoveableGrid

    def seed_fill(self, grid):
        fillNum = 0
        visited = {grid.pos}
        depth = 1
        # if grid.type == grids.FOOD:
        #     depth = 0
        queue = [(grid, depth)]
        fillGraph = []
        food_distance = 0

        for k in xrange(self.world.field.width):
            i = []
            for j in xrange(self.world.field.height):
                i.append(0)
            fillGraph.append(i)

        while queue:
            Node = queue.pop(0)
            myGrid = Node[0]
            depth = Node[1]
            fillNum +=1
            if myGrid.type == grids.FOOD:
                food_distance = Node[1]
                depth -=1

            # fillGraph[self.world.field.width - myGrid.pos[0]-1][self.world.field.height - myGrid.pos[1] - 1] = Node[1]
            fillGraph[myGrid.pos[1]][myGrid.pos[0]] = Node[1]
            # currentMoveableGrid = self.get_current_moveable_grid(myGrid, Node[1]+1, visited)
            currentMoveableGrid = self.get_current_moveable_grid(myGrid, Node[1], visited)
            if len(currentMoveableGrid):
                for i in currentMoveableGrid:
                    visited.add(i.pos)
                    queue.append((i, depth+1))
        

        blankNum = len(self.world.field.fields)
        enemySnakeLength = 0
        for i in self.enemySnake:
            if i.alive:
                enemySnakeLength += len(i.body)
        blankNum = blankNum - enemySnakeLength

        dir = direction[(grid.pos[0] - self.snake.head.pos[0], grid.pos[1] - self.snake.head.pos[1], )]
        # dprint ("==========================================================")
        # dprint ("expect: %d but got %d,  dir in %s" %(blankNum, fillNum, dir))
        # dprint ("food_distance: ",food_distance )
        # dprint ("len of snake:", len(self.snake.body))
        # s = ""
        # for i in fillGraph:
        #     s += str(i);
        #     s += '\n'
        # # self.world.test_snake_sync()
        # dprint (self.world)
        # dprint (s)
        
        if fillNum == blankNum:
            return True,fillNum,food_distance,fillGraph[self.snake.body[-1].pos[1]][self.snake.body[-1].pos[1]]
        else:
            return False,fillNum,food_distance, fillGraph[self.snake.body[-1].pos[1]][self.snake.body[-1].pos[1]]

    def update(self, world):
        if not self.snake.alive:
            return
        if len(world.foods):
            food = world.foods[0]
        self.world = world
        self.enemySnake= [i for i in self.world.snakes if (i != self.snake and i.alive)]
        tempMoveableGrid = self.get_current_moveable_grid(self.snake.head, 1, set())
        tempGap,num, candidate = -1, -1, None 
        currentMoveableGrid = []
        distance = 100000

        random.shuffle(tempMoveableGrid)
        for grid in tempMoveableGrid:
            isOk, fillNum, food_distance, gap = self.seed_fill(grid)
            if fillNum > num:
                num = fillNum
                candidate = grid
                distance = food_distance
                tempGap = gap
                # distance = abs(grid.pos[0] - food.pos[0]) + \
                #     abs(grid.pos[1] - food.pos[1])

            elif fillNum == num:
                if food_distance < distance:
                    # if random.randint(0,4):
                    candidate = grid
                    distance = food_distance
                    tempGap = gap
                elif food_distance == distance and gap > tempGap:
                    candidate = grid
                    distance = food_distance
                    tempGap = gap
                elif food_distance > distance and gap > tempGap:
                    if random.randint(0,6) == 0:
                        candidate = grid
                        distance = food_distance
                        tempGap = gap

                elif food_distance == distance:
                    if random.randint(0,2):
                        candidate = grid
                    
        if candidate:
            self.currentMove = (candidate.pos[0] - self.snake.head.pos[0], candidate.pos[1] - self.snake.head.pos[1])
            self.snake.update_direction(self.currentMove)
            dprint("decide to move in dir", direction[self.currentMove])
        else:
            print "!!!!!!!!NO choice!!"

 
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
        print world
