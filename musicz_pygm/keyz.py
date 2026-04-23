#coding=utf-8

import pygame
pygame.init()
from pygame import locals as Key
from buildz import xf
# from pynput.keyboard import Listener, Key
from . import draw
k2s = xf.loads(r"""
ESCAPE: esc, PRINT: prtsc
BACKQUOTE: '`', MINUS: '-', EQUALS: '=', BACKSPACE: backspace
TAB: tab, LEFTBRACKET: '[', RIGHTBRACKET: ']', BACKSLASH: '\\'
CAPSLOCK: caps_lock, SEMICOLON:";", QUOTE: "'", RETURN: enter
LSHIFT: shift_l, COMMA: ',', PERIOD: '.', SLASH: '/', RSHIFT: shift_r
LCTRL: ctrl_l, LMETA: win_l, LALT: alt_l, SPACE: space, RALT: alt_r, RCTRL: ctrl_r
LEFT: left, RIGHT: right, UP: up, DOWN: down
""")

ckeys2s = {}
for k, v in k2s.items():
    ckeys2s[getattr(Key, 'K_'+k)] = v
bs = b'az09'
for i in range(bs[0], bs[1]+1):
    c = bytes([i]).decode()
    ckeys2s[getattr(Key, 'K_'+c)]=c
for i in range(bs[2], bs[3]+1):
    c = bytes([i]).decode()
    ckeys2s[getattr(Key, 'K_'+c)]=c

pass
for i in range(1, 13):
    c=str(i)
    ckeys2s[getattr(Key, 'K_F'+c)]=f"f{c}"
pass

# 键盘布局显示
kb_rows = [
    list('`1234567890-=')+["backspace"],
    ['tab']+list('qwertyuiop[]\\'),
    ['caps_lock']+list("asdfghjkl;'")+['enter'],
    ['shift_l']+list("zxcvbnm,./")+['shift_r'],
    'ctrl_l,win_l,alt_l,space,alt_r,ctrl_r,##,up'.split(","),
    "##x,left,down,right".split(",")
]
kbs_shows = {}
for kb_row in kb_rows:
    for kb in kb_row:
        kbs_shows[kb] = [kb.upper(), 1]

pass
shows = """
`,`,0.8
backspace,Backspace,1.7
tab,Tab,1.5
caps_lock,Caps,1.7
enter,Enter,1.9
shift_l,Shift,2.25
shift_r,Shift,2.4
win_l,Win,2.25
space,Space,5.5
ctrl_l,Ctrl,1
alt_l,Alt,1
alt_r,Alt,1
ctrl_r,Ctrl,1
up, up, 1
down,down,1
left,left,1
right,right,1
##x,##x,12.3
"""
shows=shows.strip().split("\n")
shows = [k.split(",") for k in shows]
for k,n,v in shows:
    v = float(v)
    kbs_shows[k] = [n,v]

pass

from buildz.base import Args, Base
import threading
class Keys(Base):
    def key_color(self, key, color):
        self.show_keys[key].color(color)
    def bind_text(self, key, text):
        self.show_keys[key].bind_text(text)
    def bind_note(self, key, text):
        self.show_keys[key].bind_note(text)
    def init_draw(self,x,y,w,h):
        # x = 50
        # y = 100
        # w = 45
        # h = 60
        sp_rw = 0.11
        sp_rh = 0.09
        sp_w = sp_rw*w
        sp_h = sp_rh*h
        for kb_row in kb_rows:
            cx = x
            for kb in kb_row:
                rw = 1
                if kb in kbs_shows:
                    name, rw = kbs_shows[kb]
                    if kb.strip()!="" and kb[:2]!="##":
                        item = draw.Key(cx,y,int(w*rw),h,' ',name, ' ')
                        self.show_keys[kb]=item
                        self.win.add(item)
                        self.rects.append([kb, item.rect])
                cx+=int(w*rw)+sp_w
            y+=h+sp_h
        y = y-h-sp_h

    def char(self, key):
        if key in ckeys2s:
            return ckeys2s[key]
        if hasattr(key, "char"):
            return key.char
        return None
    def stop(self):
        self.running=False
    def init(self, fc=None,debug=False,width=1400,height=600,noframe=False,tick=120):
        '''
            callback: fc(char, press=bool)
        '''
        self.win = draw.Wind(width,height,noframe)
        self.rects = []
        self.show_keys = {}
        self.init_draw(width*0.01,height*0.01,width*0.06,height*0.15)
        self.th = None
        self.fc = fc
        self.debug = debug
        self.keys= set()
        self.mouse_key=None
        self.running=True
        self.tick = tick
    def get_key_from_pos(self, pos):
        """给定鼠标坐标，返回按下了哪个键"""
        x, y = pos
        for key_code, rect in self.rects:
            if rect.collidepoint(x, y):
                return key_code
        return None
    def press(self, key, cal_char=True):
        #print("press", key)
        if cal_char:
            c = self.char(key)
        else:
            c = key
        #print("press c:", c)
        if self.debug:
            print(f"press '{c.encode()}'")
        if c is not None:
            if c in self.keys:
                return
            self.keys.add(c)
            if c in self.show_keys:
                self.show_keys[c].press()
            if self.fc:
                self.fc(c, True)
    def release(self, key, cal_char=True):
        if cal_char:
            c = self.char(key)
        else:
            c = key
        if self.debug:
            print(f"release '{c}'")
        if c is not None:
            if c in self.keys:
                self.keys.remove(c)
                if c in self.show_keys:
                    self.show_keys[c].unpress()
            if self.fc:
                self.fc(c, False)
    def start(self):
        if self.th:
            return
        self.th = threading.Thread(target=self.run, daemon=True)
        self.th.start()
    def run(self):
        self.running=True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                #print(f"event: {event}")
                if event.type == Key.QUIT:
                    self.running = False
                if event.type == Key.KEYDOWN:
                    if event.key == Key.K_ESCAPE:
                        self.running = False
                    else:
                        #print(f"press {event.key}")
                        self.press(event.key)
                if event.type == Key.KEYUP:
                    #print(f"release {event.key}")
                    self.release(event.key)
                # 鼠标事件
                if event.type == Key.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        key_code = self.get_key_from_pos(event.pos)
                        if key_code:
                            self.press(key_code, False)
                            self.mouse_key = key_code
                if event.type == Key.MOUSEMOTION:
                    if event.buttons[0] == 1:
                        key_code = self.get_key_from_pos(event.pos)
                        if self.mouse_key and self.mouse_key!=key_code:
                            self.release(self.mouse_key, False)
                            self.mouse_key = None
                        if key_code:
                            self.press(key_code, False)
                            self.mouse_key = key_code
                if event.type == Key.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.mouse_key:
                            self.release(self.mouse_key, False)
                            self.mouse_key = None
            self.win.update()
            clock.tick(self.tick)

pass

def test():
    keys = Keys()
    keys.run()

pass

if __name__=="__main__":
    test()

pass

'''
python -m musicz_pygm.keyz_pygame

'''