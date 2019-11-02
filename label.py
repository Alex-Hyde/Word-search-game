import pygame
pygame.init()


class Label:
    def __init__(self, text, x=0, y=0, font="lucida bright", size=18, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.size = size
        self.label = self.render_label()

    def draw(self, win):
        win.blit(self.label, (self.x, self.y))

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_width(self):
        return self.label.get_width()

    def get_height(self):
        return self.label.get_height()

    def set_text(self, text):
        self.text = text
        self.label = self.render_label()

    def render_label(self):
        return pygame.font.SysFont(self.font, self.size).render(self.text, True, self.color)

    def set_color(self, color):
        self.color = color
        self.label = self.render_label()
