import pygame
import random
import math

# stroke step
d = 3
# stroke error
e = 4
# stroke radius
r = 4
# stroke repeat
p = 4

colors = [
        (0, 0, 0),
        (20, 20, 20),
        (40, 40, 40),
        # (80, 80, 80),
        ]

def circle(surface, pos, R, fill):
    pygame.draw.circle(surface, fill, (int(pos[0]), int(pos[1])), R)
    # pygame.draw.circle(surface, color, pos, R, 5)
    dt = float(d) / R
    n = int(math.pi * 2 / dt) + 1
    range_ = range(0, n)
    random.shuffle(range_)
    x0, y0 = pos
    for i in range_:
        t = dt * i
        x, y = math.cos(t), math.sin(t)
        for j in xrange(p):
            f = (random.random() - .5) * 2 * e
            color = random.choice(colors)
            pygame.draw.circle(surface, color, (
                int(x0 + (R + f) * x), int(y0 + (R + f) * y)), r)

def main():
    pygame.display.init()
    screen = pygame.display.set_mode((800, 600))

    tm = pygame.time.Clock()
    while 1:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit(0)
        screen.fill((0xff, 0xff, 0xff))
        circle(screen, (400, 300), 180, (0xef, 0xef, 0xff))
        circle(screen, (300, 300), 50, (0xef, 0xef, 0xff))
        circle(screen, (400, 300), 50, (0xef, 0xef, 0xff))
        circle(screen, (500, 300), 50, (0xef, 0xef, 0xff))
        pygame.display.update()
        tm.tick(5)
if __name__ == '__main__':
    main()
