import pygame
import grid
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


class Menu(grid.Grid):
    def __init__(self, rect, r, c, gap, button_text_list, button_on_click=None, color=BLACK):
        super().__init__(rect, r, c, gap)
        self.button_list = self.create_buttons(button_text_list, button_on_click)
        self.color = color

    def create_buttons(self, text_list, b_on_click):
        b_list = button.ButtonList()
        for p in self.points:
            b = button.Button((p[0], p[1], self.cWidth, self.cHeight), text=text_list[0])
            if b_on_click is not None:
                b.on_click = b_on_click
            b_list.add(b)
            del text_list[0]
        return b_list

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, 1)
        self.button_list.draw(win)

    def get_button_pos(self, b):
        ind = self.button_list.find(b)
        x = ind % self.c
        y = ind // self.c
        return x, y

    def get_button(self, x, y):
        return self.button_list.get(y*self.c + x)
