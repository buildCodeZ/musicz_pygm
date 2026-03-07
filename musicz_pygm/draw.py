#
import pygame


class Item:
    def __init__(self):
        self.alive = True
    def update(self, screen):
        pass

pass
class Items(Item):
    def __init__(self):
        super().__init__()
        self.items = []
    def add(self, item):
        self.items.append(item)
    def update(self, screen):
        rst = []
        for item in self.items:
            if not item.alive:
                continue
            item.update(screen)
            rst.append(item)
        self.items = rst

pass

font_a = pygame.font.SysFont(None, 21)
font_b = pygame.font.SysFont(None, 18)
font_c = pygame.font.SysFont(None, 14)
TEXT_COLOR_A = (0, 0, 0)
TEXT_COLOR_B = (125, 125, 125)
KEY_BORDER = (100, 100, 100)
BACKGROUND_COLOR = (100, 100, 100)
KEY_UP = (200, 200,200)
KEY_DOWN = (150, 200, 255)

KEY_LEFT_COLOR = (200, 255,255)
KEY_RIGHT_COLOR = (255, 255,200)
KEY_LEFT_COLOR_SET = (200, 200,255)
KEY_RIGHT_COLOR_SET = (255, 200,200)
OPT = (255, 255, 255)
KEY_COLORS_STR = {
    'left': KEY_LEFT_COLOR,
    'right': KEY_RIGHT_COLOR,
    'left_opt': KEY_LEFT_COLOR_SET,
    'right_opt': KEY_RIGHT_COLOR_SET,
    'opt': OPT
}
FUNCTION_BG = (220, 220, 220)
POWER_COLOR = (0, 0, 255)   
PRESS_COLOR = (0, 128, 0)   
class Key(Item):
    def __init__(self, x, y, width, height, word_a=None, word_b=None, word_note = None, color=KEY_UP, press_color=KEY_DOWN):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.word_a = word_a
        self.word_b = word_b
        self.word_note = word_note
        self.colors = [color, press_color]
        self.is_press=False
        self.rect = pygame.Rect(x, y, width, self.height)
        if word_a:
            self.text_a = Label(x + width//2, y + height*0.3, word_a, TEXT_COLOR_A, font_a)
        if word_b:
            self.text_b = Label(x + width*0.4, y + height*0.7, word_b, TEXT_COLOR_B, font_b)
        if word_note:
            self.text_note = Label(x + int(width*0.7), y + height*0.7, word_note, TEXT_COLOR_B, font_c)
    def bind_text(self, text):
        self.word_a = text
        self.text_a.bind_text(text)
    def bind_note(self, text):
        self.word_note = text
        self.text_note.bind_text(text)
    def press(self, judge=True):
        self.is_press = judge
    def unpress(self):
        self.press(0)
    def color(self, val):
        if type(val)==str:
            val = KEY_COLORS_STR[val]
        self.colors[0]=val
    def update(self, screen):
        pygame.draw.rect(screen, self.colors[self.is_press], self.rect)
        pygame.draw.rect(screen, KEY_BORDER, self.rect, 2)
        if self.word_a:
            self.text_a.update(screen)
        if self.word_b:
            self.text_b.update(screen)
        if self.word_note:
            self.text_note.update(screen)

pass
class Label(Item):
    def __init__(self, x, y, text, color, font):
        super().__init__()
        self.color = color
        self.font = font
        self._rect = (x,y)
        self.bind_text(text)
    def bind_text(self, text):
        self._text = text
        if callable(text):
            text = text()
        self.set(text)
    def set(self, text):
        #print(f"label: {text}")
        self.text = self.font.render(text, True, self.color)
        self.rect = self.text.get_rect(center=self._rect)
    def update(self, screen):
        if callable(self._text):
            self.set(self._text())
        screen.blit(self.text, self.rect)


class Wind:
    def __init__(self, width=1400, height=600,noframe=False):
        args = [(width, height)]
        if noframe:
            args.append(pygame.NOFRAME)
        self.screen = pygame.display.set_mode(*args)
        pygame.display.set_caption("键盘钢琴模拟器")
        self.items = Items()
    def add(self, item):
        self.items.add(item)
    def update(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.items.update(self.screen)
        pygame.display.flip()