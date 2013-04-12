import pygame
from grids import Directions
import grids
from debug import dprint
import copy
import random
from collections import deque

# TODO: run vim :%s/\(\w\),\(\w\)/\1, \2/g<cr>  on this file

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
        self.food = None

    def get_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_current_moveable_grid(self, head, depth, visited):
        currentMoveableGrid = [] 
        get_grid_at = self.world.field.get_grid_at
        snake = self.snake
        for dx, dy in Directions.all:
            grid = get_grid_at(head.pos[0] + dx, head.pos[1] + dy)

            if grid is not None and grid.pos not in visited:
                flag = True
                add = False
                if depth < 0 and grid == snake.lastTail:
                    flag = False
                if grid.type == grids.BLANK and flag:
                    add = True
                elif grid.type == grids.FOOD:
                    add = True
                elif depth > 0:
                    # # if depth >= len(snake.body):
                    # #    depth = 0 # bug here ?
                    # depth1 = 0 if depth >= len(snake.body) else depth
                    # for i in snake.body[-depth1:]:
                    #     if i.pos == grid.pos:
                    #         add = True
                    #         break

                    # avoid list copy and for loop here 
                    if grid.owner is snake:
                        if len(snake.body) - grid.content.secID <= depth:
                            add = True

                for i in self.enemySnakes:
                    if add and self.get_distance(i.head.pos, grid.pos) == 2:
                        add = False
                if add: currentMoveableGrid.append(grid)
        return currentMoveableGrid

    def seed_fill(self, grid):
        fillNum = 0
        visited = {grid.pos}
        depth = 1
        if grid.type == grids.FOOD:
            depth = 0
        queue = deque([(grid, depth)])
        food_distance = 0
        # fillGraph = {g.pos: 0 for g in self.world.field}
        fillGraph = []
        for i  in xrange(self.world.field.height):
            temp = []
            for j  in xrange(self.world.field.height):
                temp.append(0)
            fillGraph.append(temp)

        while queue:
            pivotGrid, depth = queue.popleft()
            # fillGraph[pivotGrid.pos] = depth0 = depth
            fillGraph[pivotGrid.pos[1]][pivotGrid.pos[0]] = depth0 = depth
            fillNum +=1
            depth0 += 1
            if pivotGrid.type == grids.FOOD:
                food_distance = depth
                depth0 -=1
            # XXX: why depth0 ??
            for i in self.get_current_moveable_grid(pivotGrid, depth0, visited):
                visited.add(i.pos)
                if i.type == grids.FOOD:
                    queue.append((i, depth))
                else:
                    queue.append((i, depth+1))


        blankNum = len(self.world.field.fields) - \
                sum(len(snake.body) for snake in self.enemySnakes)

        # dir = direction[(grid.pos[0] - self.snake.head.pos[0], grid.pos[1] - self.snake.head.pos[1], )]
        # dprint ("==========================================================")
        # dprint ("expect: %d but got %d,  dir in %s" %(blankNum, fillNum, dir))
        # dprint ("food_distance: ",food_distance )
        # dprint ("len of snake:", len(self.snake.body))
        # s = ""
        # for i in fillGraph:
        #     s += str(i);
        #     s += '\n'
        # dprint (self.world)
        # dprint (s)
        
        # XXX: bug here previously, pos[1] -> pos[0]
        return True, fillNum, food_distance, fillGraph[self.snake.body[-1].pos[1]][self.snake.body[-1].pos[1]]
        # return (fillNum == blankNum) , fillNum, food_distance, fillGraph[self.snake.body[-1].pos]

    def update(self, world):
        if not self.snake.alive:
            return
        if len(world.foods):
            if not self.food or self.food.pos != world.foods[0].pos:
                self.food = world.foods[0]
                self.food_count = 0
            if world.foods[0].pos == self.food.pos:
                self.food_count += 1
                # print "food_count, mulipyer", self.food_count, float(self.food_count)/len(self.snake.body)

            self.multipier = float(self.food_count)/len(self.snake.body)

        self.world = world
        self.enemySnakes= [i for i in self.world.snakes if (i != self.snake and i.alive)]
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
                    choice = 10
                    if len(self.enemySnakes) == 0:
                        choice = 9
                        if self.multipier>= 1.5:
                            choice = 2
                    if random.randint(0,choice) == 0:
                        candidate = grid
                        distance = food_distance
                        tempGap = gap

                elif food_distance == distance:
                    if random.randint(0,2):
                        candidate = grid
                    
        if candidate:
            self.currentMove = (candidate.pos[0] - self.snake.head.pos[0], 
                    candidate.pos[1] - self.snake.head.pos[1])
            self.snake.update_direction(self.currentMove)
            dprint("decide to move in dir", direction[self.currentMove])
        else:
            dprint("!!!!!!!!NO choice!! body length:{}, map size:{}".format(
                len(self.snake.body), len(world.field.fields)))

 
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
