from __future__ import print_function
import pygame
import random

class Dirs:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)

GRID_WIDTH = 20
FPS = 5
COLOR_BG = (0xff, 0xff, 0xff)
COLOR_SNAKE = (0, 0xff, 0xff)
COLOR_FOOD = (0xff, 0, 0)

KEY_MAP = {
        pygame.K_w: Dirs.UP,
        pygame.K_s: Dirs.DOWN,
        pygame.K_a: Dirs.LEFT,
        pygame.K_d: Dirs.RIGHT,
        }

class Game:
    def __init__(self, fieldSize):
        self.fieldSize = fieldSize
        pygame.display.init()
        w = GRID_WIDTH * fieldSize[0]
        h = GRID_WIDTH * fieldSize[1]
        self.screen = pygame.display.set_mode((w, h))

    def draw(self):
        screen = self.screen
        screen.fill(COLOR_BG)
        # draw food
        for food in self.foods:
            i, j = food
            pygame.draw.rect(screen, COLOR_FOOD, 
                    (j*GRID_WIDTH, i*GRID_WIDTH, GRID_WIDTH-4, GRID_WIDTH-4))
        # draw snake
        for pos in self.snake:
            i, j = pos
            pygame.draw.rect(screen, COLOR_SNAKE,
                    (j*GRID_WIDTH, i*GRID_WIDTH, GRID_WIDTH-4, GRID_WIDTH-4))

    def reset(self, snakePos, snakeDir, snakeLen, foodNum=1):
        self.snake = self.gen_snake(snakePos, snakeDir, snakeLen)
        self.dir = snakeDir
        self.foods = []
        for i in xrange(foodNum):
            self.gen_food()

    def gen_snake(self, pos, dir, length):
        snake = [pos]
        x, y = pos
        dx, dy = dir
        for i in xrange(1, length):
            x, y = x - dx, y - dy
            snake.append((x, y))
        return snake

    def avail_positions(self):
        for pos in self.positions():
            if pos not in self.snake and pos not in self.foods:
                yield pos

    def positions(self):
        w, h = self.fieldSize
        for i in xrange(w):
            for j in xrange(h):
                yield i, j

    def gen_food(self):
        poss = list(self.avail_positions())
        pos = random.choice(poss)
        self.foods.append(pos)
        # print('gen food:', self.foods)

    def set_nextdir(self, dir):
        i0, j0 = self.dir
        i, j = dir
        if abs(i-i0)<2 and abs(j-j0) < 2:
            self.dir = dir

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN and event.key in KEY_MAP:
            self.set_nextdir(KEY_MAP[event.key])

    def update_logic(self):
        nextPoss = self.next_positions()
        w, h = self.fieldSize
        snakeDie = False
        for (i, j) in nextPoss:
            if not(0 <= i < h and 0 <= j < w):
                snakeDie = True
        if not snakeDie:
            if len(set(nextPoss)) != len(nextPoss):
                snakeDie = True
        if snakeDie:
            print('game over, snake die')
            self._quit = True
            return
        # snake not die
        # move snake
        self.move_snake()
        nextHead = nextPoss[0]
        if nextHead in self.foods:
            self.foods.remove(nextHead)
            self.gen_food()

    def move_snake(self):
        snake = self.snake
        snake.insert(0, self.next_head())
        snake.pop()

    def next_head(self):
        i0, j0 = self.snake[0]
        di, dj = self.dir
        nextHead = i0 + di, j0 + dj
        return nextHead

    def next_positions(self):
        return [self.next_head()] + self.snake[:-1]

    def main_loop(self):
        self._quit = False
        timer = pygame.time.Clock()
        while not self._quit:
            # handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit = True
                self.handle_input(event)
            # update snake, food
            self.update_logic()
            # draw
            self.draw()
            pygame.display.flip()
            # tick
            timer.tick(FPS)

if __name__ == '__main__':
    game = Game((20, 20))
    game.reset(snakePos=(8, 6), snakeDir=Dirs.RIGHT, snakeLen=3, foodNum=1)
    game.main_loop()
