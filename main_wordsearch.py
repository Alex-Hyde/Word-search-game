# --------------------------------------------------------------------
# Program: Word Search Assignment - OOP implementation
# Author: Alex Hyde
# Date: Nov 06 2019
# Description: Word Search game implementing many OOP concepts,
#   including inheritance and polymorphism. The program allows the
#   user to select the puzzle that they wish to play. The program
#   will then allow the user to attempt to solve the puzzle, using
#   draging to select words. The program allows free movement between
#   any word search puzzle and the puzzle select screen.
# Input: The program takes input from the user through button clicks.
# --------------------------------------------------------------------

import pygame
import vector
import label
import random
import grid
import frame

pygame.init()

# window screen constants
WIN_WIDTH = 800
WIN_HEIGHT = 700
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (200, 0, 200)
LIGHT_GREEN = (200, 255, 200)
YELLOW = (255, 255, 0)
THE_BLUE = (130, 220, 226)
GREY = (100, 100, 100)
LIGHT_GREY = (200, 200, 200)
MEDIUM_GREY = (150, 150, 150)
BROWN = (48, 29, 2)
ORANGE = (255, 150, 0)
DARK_ORANGE = (200, 100, 0)


# main word search class for gameplay
class WordSearch(grid.Menu):
    def __init__(self, rect, puzzle, gap=0, hColor=RED, color=BLACK, fColor=WHITE):
        super().__init__(rect, puzzle.r, puzzle.c, puzzle.letters, gap, on_button_click,
                         color=color, visible_lines=False)
        self.title = puzzle.get_title()  # title from puzzle object
        self.highlight_color = hColor
        self.first_click = None  # button at first click of drag
        self.second_click = None  # mousepos of drag
        self.word_list = puzzle.words
        self.start_pos = None  # mouse position at frist click of drag
        self.current_highlight_buttons = []
        self.used_buttons = []  # buttons used in found words
        self.word_grid = self.create_word_labels()
        self.rendered_title = grid.WordGrid((self.x, self.y - 70, self.w, 50), 1, 1,
                                            text_list=[self.title + " Word Search!"], visible_lines=False)
        self.rendered_title.labels[0].set_size(40)  # sets title size
        self.rendered_title.update_labels_pos()  # update title pos to center of grid
        self.found_words = 0
        for b in self.button_list:  # sets button colours
            b.set_fColor(fColor)
            b.set_bColor(color)
            b.set_hoverColor(hColor)
            b.set_holdColor(hColor)

    def draw(self, win):
        super().draw(win)
        self.word_grid.draw(win)  # word list on side of word search
        self.rendered_title.draw(win)

    # create rendered word labels for word list
    def create_word_labels(self):
        xgap = 10
        ygap = 30
        g = grid.WordGrid((self.x + self.w + xgap, self.y, 1, ygap * len(self.word_list)), len(self.word_list), 1,
                          text_list=self.word_list, text_hAlign=grid.LEFT, text_vAlign=grid.TOP, visible_lines=False)
        return g

    # get list of buttons from button to another button (only in straight or perfectly diagonal lines)
    def get_b_list(self):
        b_list = []
        if self.first_click[0] == self.second_click[0]:  # if vertical
            if self.first_click[1] < self.second_click[1]:
                start = self.first_click[1]
            else:
                start = self.second_click[1]
            for l in range(abs(self.first_click[1] - self.second_click[1])+1):
                b_list.append(self.get_button_by_pos(self.first_click[0], start + l))

        elif self.first_click[1] == self.second_click[1]:  # if horizontal
            if self.first_click[0] < self.second_click[0]:
                start = self.first_click[0]
            else:
                start = self.second_click[0]
            for l in range(abs(self.first_click[0] - self.second_click[0])+1):
                b_list.append(self.get_button_by_pos(start + l, self.first_click[1]))

        # if diagonal
        elif abs(self.first_click[0] - self.second_click[0]) == abs(self.first_click[1] - self.second_click[1]):

            # starts from left most button. Sign determines if the slope if up or down
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
                b_list.append(self.get_button_by_pos(start[0] + l, start[1] + l * sign))

        return b_list

    # checks if the buttons in the button list for a word in the word search's word list
    def check_word(self, b_list):
        string = ""
        for b in b_list:
            string += b.get_text()

        if string in self.word_list:
            self.word_grid.get_label(string).set_color(ORANGE)
            for b in b_list:
                b.set_fColor(GREY)
                self.used_buttons.append(b)
            self.found_words += 1
        elif string[::-1] in self.word_list:  # backwards
            self.word_grid.get_label(string[::-1]).set_color(ORANGE)
            for b in b_list:
                b.set_fColor(GREY)
                self.used_buttons.append(b)
            self.found_words += 1

        # check if the puzzle is complete
        if self.found_words == len(self.word_list):
            winLabel.set_visible(True)
            winLabel2.set_visible(True)
            current_word_search.button_list.set_active(False)
            current_frame.fill = LIGHT_GREEN
            for word in self.word_grid.labels:
                word.set_color(PURPLE)
            self.rendered_title.get_label_by_index(0).set_color(PURPLE)

    # highlights buttons from start click to current mouse position (only gets buttons in valid directions)
    def highlight_buttons(self):
        mousepos = pygame.mouse.get_pos()
        if self.first_click is not None:
            angle = vector.Vec2(self.start_pos[0], self.start_pos[1]).angle(vector.Vec2(mousepos[0], mousepos[1]))

            if 90-22.5 <= angle < 90+22.5 or 270-22.5 <= angle < 270+22.5:  # vertical
                end_button = self.button_list.get_button_at((self.start_pos[0], mousepos[1]))

            elif 180-22.5 <= angle < 180+22.5 or 360 - 22.5 <= angle or angle < 22.5:  # horizontal
                end_button = self.button_list.get_button_at((mousepos[0], self.start_pos[1]))

            elif 135-22.5 <= angle < 135+22.5 or 315 - 22.5 <= angle < 315 + 22.5:  # diagonal (bottom left/top right)
                pos = vector.Vec2.closest_point(vector.Vec2(self.start_pos[0], self.start_pos[1]),
                                                vector.Vec2(self.start_pos[0] - 1, self.start_pos[1] + 1),
                                                vector.Vec2(mousepos[0], mousepos[1]))
                end_button = self.button_list.get_button_at((pos.x, pos.y))

            elif 45-22.5 <= angle < 45+22.5 or 225 - 22.5 <= angle < 225 + 22.5:  # diagonal (top left/bottom right)
                pos = vector.Vec2.closest_point(vector.Vec2(self.start_pos[0], self.start_pos[1]),
                                                vector.Vec2(self.start_pos[0] + 1, self.start_pos[1] + 1),
                                                vector.Vec2(mousepos[0], mousepos[1]))
                end_button = self.button_list.get_button_at((pos.x, pos.y))
            else:  # if mouse if on top of the start click
                end_button = -1

            if end_button != -1:  # if a second button was gotten
                self.second_click = self.get_button_pos(end_button)
                temp_b_list = self.get_b_list()
                self.unhighlight_buttons()
                self.current_highlight_buttons = temp_b_list
                for b in temp_b_list:
                    b.set_fColor(self.highlight_color)

    # reset all buttons that shouldn't be highlighted
    def unhighlight_buttons(self):
        for b in self.current_highlight_buttons:
            if b not in self.used_buttons:
                b.set_fColor(WHITE)
            else:
                b.set_fColor((200, 200, 200))


# puzzle class for storing puzzle info (used as argument in word search class)
class Puzzle:
    def __init__(self, title, ltrs, wrds, c, r):
        self.title = title
        self.words = wrds
        self.letters = ltrs
        self.c = c
        self.r = r

    def get_title(self):
        return self.title


# create a list of puzzle objects storing the puzzles read in from the puzzle file
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


# function run when any word search button is clicked
def on_button_click(b):
    ws = current_word_search
    if ws.first_click is None:
        ws.first_click = ws.get_button_pos(b)
        ws.start_pos = pygame.mouse.get_pos()


def redraw():
    current_frame.draw(WIN)
    pygame.display.update()


# read in puzzles from text file
puzzles = read_in_puzzles(open("puzzles.txt", "r"))
current_word_search = None  # initializes variable

# puzzle select screen
puzzle_select = grid.Menu((150, 100, 500, 500), len(puzzles), 1, [p.get_title() for p in puzzles], gap=10)
for but in puzzle_select.button_list:  # set button attributes
    but.rendered_text.set_size(40)
    but.reset_text_pos()
    but.set_hoverColor(ORANGE)
    but.set_holdColor(DARK_ORANGE)
# title label
super_cool_label = label.Label("SUPER COOL WORD SEARCH!", y=30)
super_cool_label.set_size(50)
super_cool_label.set_x((WIN_WIDTH - super_cool_label.get_width())/2)
super_cool_label.set_color(BLACK)

# frame displayed on puzzle select (title screen)
puzzle_select_frame = frame.Frame([puzzle_select, super_cool_label], [puzzle_select.button_list], fill=THE_BLUE)

# labels displayed when a puzzle is complete
winLabel = label.FilledLabel((200, 300, 400, 80), "TA-DA!!!", border=3)
winLabel.set_size(50)
winLabel.fColor = GREEN
winLabel.update_text_pos()
winLabel2 = label.FilledLabel((220, 400, 360, 60), "Press anywhere to continue", border=3)
winLabel2.set_size(25)
winLabel2.fColor = THE_BLUE
winLabel2.update_text_pos()

# frame displayed on screen (starts with puzzle select)
current_frame = puzzle_select_frame

inPlay = True
clock = pygame.time.Clock()


while inPlay:
    redraw()
    clock.tick(60)

    events = pygame.event.get()

    # booleans used for button click processing
    mouse_click = False
    mouse_release = False

    for event in events:
        if event.type == pygame.QUIT:
            inPlay = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # prevent scrolling on buttons (left or right click only)
                mouse_click = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_release = True
                # if a puzzle is complete, press anywhere to return to the puzzle screen
                if winLabel.visible and current_frame != puzzle_select_frame:
                    current_frame = puzzle_select_frame
                if current_word_search is not None:
                    # when you release, check if a word is highlighted and reset the highlight and click variables
                    if current_word_search.second_click is not None:
                        current_word_search.check_word(current_word_search.get_b_list())
                    current_word_search.unhighlight_buttons()
                    current_word_search.first_click = None
                    current_word_search.second_click = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # return to puzzle select screen
                current_word_search = None
                current_frame = puzzle_select_frame

    # if draging a word, button below mouse if not highlighted (mousepos is adjusted to the last button in the line)
    if current_word_search is not None and current_word_search.second_click is not None:
        mp = current_word_search.second_click
    else:
        mp = pygame.mouse.get_pos()
    current_frame.process_events(mouse_click, mouse_release, mp)

    # process puzzle select button on release
    if current_frame == puzzle_select_frame:
        for but in puzzle_select.get_released():
            p = puzzles[but]
            current_word_search = WordSearch((100, 100, 500, 500), p, gap=2, hColor=ORANGE)  # create new word search
            winLabel.set_visible(False)
            winLabel2.set_visible(False)
            # switches to game frame from puzzle select frame
            # creates frame with word search (and win labels, currently invisible)
            current_frame = frame.Frame([current_word_search, winLabel, winLabel2],
                                        [current_word_search.button_list], THE_BLUE)
    elif current_word_search is not None:
        current_word_search.highlight_buttons()

# always quit pygame :)
pygame.quit()
