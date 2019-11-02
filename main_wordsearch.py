import pygame
import menu
import vector
import label
import random

pygame.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 700
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
LIGHT_GREY = (200, 200, 200)
BROWN = (48, 29, 2)


class WordSearch(menu.Menu):
    def __init__(self, rect, gap, puzzle, hColor=RED, color=BLACK, fColor=WHITE):
        super().__init__(rect, puzzle.r, puzzle.c, gap, puzzle.letters, on_button_click, color=color)
        self.highlight_color = hColor
        self.first_click = None
        self.second_click = None
        self.word_list = puzzle.words
        self.start_pos = None
        self.current_highlight_buttons = []
        self.used_buttons = []
        self.word_label_list = self.create_word_labels()
        for b in self.button_list:
            b.set_fColor(fColor)
            b.set_bColor(color)
            b.set_hoverColor(hColor)
            b.set_holdColor(hColor)

    def draw(self, win):
        super().draw(win)
        for label in self.word_label_list:
            label.draw(win)

    def create_word_labels(self):
        l_list = []
        xgap = 10
        ygap = 30
        for i, word in enumerate(self.word_list):
            l_list.append(label.Label(word, self.x + self.w + xgap, self.y + i*ygap))
        return l_list

    def get_b_list(self):
        b_list = []
        if self.first_click[0] == self.second_click[0]:
            if self.first_click[1] < self.second_click[1]:
                start = self.first_click[1]
            else:
                start = self.second_click[1]
            for l in range(abs(self.first_click[1] - self.second_click[1])+1):
                b_list.append(self.get_button(self.first_click[0], start + l))

        elif self.first_click[1] == self.second_click[1]:
            if self.first_click[0] < self.second_click[0]:
                start = self.first_click[0]
            else:
                start = self.second_click[0]
            for l in range(abs(self.first_click[0] - self.second_click[0])+1):
                b_list.append(self.get_button(start + l, self.first_click[1]))

        elif abs(self.first_click[0] - self.second_click[0]) == abs(self.first_click[1] - self.second_click[1]):
            if self.first_click[0] < self.second_click[0]:
                start = self.first_click
                if self.first_click[1] - self.second_click[1] < 0:
                    sign = 1
                else:
                    sign = -1
            else:
                start = self.second_click
                if self.second_click[1] - self.first_click[1] < 0:
                    sign = 1
                else:
                    sign = -1
            for l in range(abs(self.first_click[0] - self.second_click[0])+1):
                b_list.append(self.get_button(start[0] + l, start[1] + l * sign))

        return b_list

    def check_word(self, b_list):
        string = ""
        for b in b_list:
            string += b.get_text()

        if string in self.word_list:
            self.word_label_list[self.word_list.index(string)].set_color(LIGHT_GREY)
            for b in b_list:
                b.set_fColor((200, 200, 200))
                self.used_buttons.append(b)
        elif string[::-1] in self.word_list:
            self.word_label_list[self.word_list.index(string[::-1])].set_color(LIGHT_GREY)
            for b in b_list:
                b.set_fColor((200, 200, 200))
                self.used_buttons.append(b)

    def highlight_buttons(self):
        mousepos = pygame.mouse.get_pos()
        if self.first_click is not None:
            angle = vector.Vec2(self.start_pos[0], self.start_pos[1]).angle(vector.Vec2(mousepos[0], mousepos[1]))
            if 90-22.5 <= angle < 90+22.5 or 270-22.5 <= angle < 270+22.5:
                end_button = self.button_list.get_button_at((self.start_pos[0], mousepos[1]))
            elif 180-22.5 <= angle < 180+22.5 or 360 - 22.5 <= angle or angle < 22.5:
                end_button = self.button_list.get_button_at((mousepos[0], self.start_pos[1]))
            elif 135-22.5 <= angle < 135+22.5 or 315 - 22.5 <= angle < 315 + 22.5:
                pos = vector.Vec2.closest_point(vector.Vec2(self.start_pos[0], self.start_pos[1]),
                                                vector.Vec2(self.start_pos[0] - 1, self.start_pos[1] + 1),
                                                vector.Vec2(mousepos[0], mousepos[1]))
                end_button = self.button_list.get_button_at((pos.x, pos.y))
            elif 45-22.5 <= angle < 45+22.5 or 225 - 22.5 <= angle < 225 + 22.5:
                pos = vector.Vec2.closest_point(vector.Vec2(self.start_pos[0], self.start_pos[1]),
                                                vector.Vec2(self.start_pos[0] + 1, self.start_pos[1] + 1),
                                                vector.Vec2(mousepos[0], mousepos[1]))
                end_button = self.button_list.get_button_at((pos.x, pos.y))
            else:
                end_button = -1
            if end_button != -1:
                self.second_click = self.get_button_pos(end_button)
                temp_b_list = self.get_b_list()
                self.unhighlight_buttons()
                self.current_highlight_buttons = temp_b_list
                for b in temp_b_list:
                    b.set_fColor(self.highlight_color)

    def unhighlight_buttons(self):
        for b in self.current_highlight_buttons:
            if b not in self.used_buttons:
                b.set_fColor(WHITE)
            else:
                b.set_fColor((200, 200, 200))


class Puzzle:
    def __init__(self, title, ltrs, wrds, c, r):
        self.title = title
        self.words = wrds
        self.letters = ltrs
        self.c = c
        self.r = r


def read_in_puzzles(file):
    pz = []
    for i in range(int(file.readline().strip())):
        title = file.readline().strip()
        rows = int(file.readline().strip())
        cols = int(file.readline().strip())
        ltrs = ""
        for r in range(rows):
            ltrs += file.readline().strip() + " "
        ltrs = ltrs.split()
        wordnum = int(file.readline().strip())
        wrds = []
        for w in range(wordnum):
            wrds.append(file.readline().strip())
        pz.append(Puzzle(title, ltrs, wrds, rows, cols))
    return pz


def on_button_click(b):
    ws = current_word_search
    if ws.first_click is None:
        ws.first_click = ws.get_button_pos(b)
        ws.start_pos = pygame.mouse.get_pos()


def redraw():
    WIN.fill(WHITE)
    current_word_search.draw(WIN)
    pygame.display.update()


puzzles = read_in_puzzles(open("puzzles.txt", "r"))
current_word_search = WordSearch((50, 50, 600, 600), 2, random.choice(puzzles), GREEN)

inPlay = True
clock = pygame.time.Clock()


while inPlay:
    redraw()
    clock.tick(60)

    events = pygame.event.get()

    current_word_search.highlight_buttons()

    mouse_click = False
    mouse_release = False
    for event in events:
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_release = True
                if current_word_search.second_click is not None:
                    current_word_search.check_word(current_word_search.get_b_list())
                current_word_search.unhighlight_buttons()
                current_word_search.first_click = None
                current_word_search.second_click = None
    # ws.second_click = ws.get_button_pos(b)
    # ws.check_for_word()
    # ws.get_button(ws.first_click[0], ws.first_click[1]).set_active(True)
    # ws.first_click = None
    # ws.second_click = None

    current_word_search.button_list.process_events(mouse_click, mouse_release, pygame.mouse.get_pos())

pygame.quit()
