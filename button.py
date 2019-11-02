import pygame
import label

pygame.init()

LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1
CENTER = 0.5


class ButtonList:
    def __init__(self, buttonList=None):
        if buttonList is None:
            buttonList = []
        self.buttonList = list(buttonList)  # if passed a tuple
        self.current = -1

    def find(self, item):
        if item in self.buttonList:
            return self.buttonList.index(item)
        else:
            return -1

    def get(self, ind):
        return self.buttonList[ind]

    def get_button_at(self, pos):
        for b in self.buttonList:
            if b.is_hover(pos):
                return b
        return -1

    def draw(self, win):
        for b in self.buttonList:
            if b.is_visible():
                b.draw(win)

    def add(self, button):
        self.buttonList.append(button)

    def process_events(self, click_bool, release_bool, mousepos):
        for b in self.buttonList:
            if (b.is_hover(mousepos) or b.is_clicked) and b.is_active():
                if click_bool:
                    b.on_click_default()
                    b.on_click(b)
                elif release_bool:
                    b.on_release_default()
                    b.on_release(b)
                else:
                    b.on_hover()
            else:
                b.reset_color()

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 1
        if self.current < len(self.buttonList):
            return self.buttonList[self.current]
        self.current = -1
        raise StopIteration


class Button:
    def __init__(self, rect, fColor=(255, 255, 255), bColor=(0, 0, 0), onHoldColor=(100, 100, 100),
                 onHoverColor=(200, 200, 200), border=1, text="", visible=True, active=True, tAlignx=CENTER,
                 tAligny=CENTER):
        self.rect = rect
        self.x, self.y, self.w, self.h = rect
        self.irect = (self.x + border, self.y + border, self.w - border * 2, self.h - border * 2)
        self.text = text
        self.tAlignx = tAlignx
        self.tAligny = tAligny
        self.rendered_text = None
        self.render_text()
        self.fColor = fColor
        self.onHoldColor = onHoldColor
        self.currentFillColor = fColor
        self.onHoverColor = onHoverColor
        self.bColor = bColor
        self.visible = visible
        self.active = active
        self.is_clicked = False
        self.is_hovered = False
        self.on_click = self.blank_func
        self.on_release = self.blank_func
        self.values = {}

    def draw(self, win):
        if self.visible:
            pygame.draw.rect(win, self.bColor, self.rect)
            pygame.draw.rect(win, self.currentFillColor, self.irect)
        self.rendered_text.draw(win)

    def render_text(self):
        self.rendered_text = label.Label(self.text)
        self.rendered_text.set_x(self.x + (self.w-self.rendered_text.get_width())*self.tAlignx)
        self.rendered_text.set_y(self.y + (self.h-self.rendered_text.get_height())*self.tAligny)

    def blank_func(self, blank):
        pass

    def is_hover(self, mousepos):
        x, y = mousepos
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def on_click_default(self):
        self.currentFillColor = self.onHoldColor
        self.is_clicked = True

    def on_release_default(self):
        self.currentFillColor = self.fColor
        self.is_clicked = False

    def set_text(self, text):
        self.text = text
        self.render_text()

    def get_text(self):
        return self.text

    def set_fColor(self, color):
        self.fColor = color
        if not self.is_clicked and not self.is_hovered:
            self.currentFillColor = self.fColor

    def set_hoverColor(self, color):
        self.onHoverColor = color
        if self.is_hovered and not self.is_clicked:
            self.currentFillColor = self.onHoverColor

    def set_holdColor(self, color):
        self.onHoldColor = color
        if not self.is_hovered and self.is_clicked:
            self.currentFillColor = self.onHoldColor

    def set_bColor(self, color):
        self.bColor = color

    def on_hover(self):
        if not self.is_clicked:
            self.currentFillColor = self.onHoverColor

    def reset_color(self):
        self.currentFillColor = self.fColor

    def set_active(self, torf):
        self.active = torf

    def is_active(self):
        return self.active

    def set_visible(self, torf):
        self.visible = torf

    def is_visible(self):
        return self.visible
