import pygame
import label
import button

pygame.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
THE_BLUE = (130, 250, 226)
GREY = (100, 100, 100)
BROWN = (48, 29, 2)


class Grid:
    def __init__(self, rect, r, c, gap):
        self.rect = rect
        self.x, self.y, self.w, self.h = rect
        self.r = r
        self.c = c
        self.gap = gap
        self.cWidth = (self.w - gap * (c + 1)) / c
        self.cHeight = (self.h - gap * (r + 1)) / r
        self.points = self.create_points()
        self.current = -1

    def create_points(self):
        points = []
        for y in range(self.r):
            for x in range(self.c):
                points.append((self.x + self.gap * (x + 1) + self.cWidth * x,
                               self.y + self.gap * (y + 1) + self.cHeight * y))
        return points

    def draw(self, win, color=BLACK):
        pygame.draw.rect(win, color, self.rect, 1)

        for p in self.points:
            pygame.draw.rect(win, color, (p[0], p[1], self.cWidth, self.cHeight), 1)

    def get_cell_index(self, x, y):
        if x < 0 or x >= self.c:
            return -1
        if y < 0 or y >= self.y:
            return -1
        return y*self.c + x

    def get_cell_pos(self, ind):
        return ind % self.c, ind // self.c

    def get_cell_coords(self, ind):
        return self.points[ind]

    def __len__(self):
        return self.r*self.c

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < len(self.points):
            return self.points[self.current]
        self.current = -1
        raise StopIteration
