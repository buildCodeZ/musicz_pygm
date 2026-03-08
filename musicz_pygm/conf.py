#
from buildz import xf, fz, pyz, dz, Args, Base
import os,threading
from . import playz, keyz, fmt
def loadf(fps, sys_conf={}):
    #print(fps)
    confs = [xf.loadf(fp) for fp in fps]
    conf = dz.Conf(spt="..")
    for obj in confs:
        conf.update(obj)
    conf.update(sys_conf)
    return conf
"""
    按下按键后
    不同按键调用不同方法
    有一个映射，按键到方法的映射，方法调用又会传入按键参数
"""
class Orders(Base):
    def init(self):
        self.orders = {}
        self.set = self.add
        self.push = self.add
    def add(self, key, fc):
        if key not in self.orders:
            self.orders[key]=[]
        self.orders[key].append(fc)
    def pop(self, key):
        self.orders[key].pop(-1)
    def has(self, key):
        return key in self.orders and len(self.orders[key])>0
    def call(self, key, conf):
        return self.orders[key][-1](conf)

pass

from .base import default_src, conf_fp, path
class Conf(Base):
    def init(self, fps, sys_conf={}):
        # print("fps:", fps)
        if type(fps) not in (list, tuple):
            fps = [fps]
        conf = loadf(fps, sys_conf)
        self.to_stops = set()
        self.fps = fps
        self.conf = conf
        self.lock = threading.Lock()
        sfile, fps, select, sample_rate, libpath, background, debug = conf("init").gets("sfile, fps, select, sample_rate, libpath, background,debug", default_src, 30, {}, 44100, None, {}, False)
        self.trs = conf.get("transforms", {})
        background = fmt.FileRead(background, self)
        play = playz.Play(fps=fps, sample_rate=sample_rate)
        play.select(**select)
        channel = dz.g(select, channel= 0)
        self.channel= channel
        self.background = background
        self.play = play
        width,height, noframe = conf("display").gets("width, height, noframe", 900,400,False)
        width,height, noframe = conf("init").gets("width, height, noframe", width,height, noframe)
        width,height, noframe = int(width),int(height), int(noframe)
        self.ks = keyz.Keys(self.press_callback, debug, width,height,noframe)
        #self.vars = vs
        self.save_fp = None
        if conf('saves').get("work",0) or conf('init').get("save",0):
            # print(f"saves a:",conf.get("saves..filepath"))
            # print(f"saves b:",conf("saves").get("filepath"))
            self.save_fp = conf.get("saves..filepath", "%Y%m%d%H%M%S.rd")
        self.build_fc(conf("keys"))
        self.running = True
    def press_callback(self, char, press):
        #print(f"press:", char.encode(), press)
        if char in self.trs:
            char = str(self.trs[char])
        #print(f"press1:", char.encode(), press)
        if not self.orders.has(char):
            return
        conf = dz.Conf()
        conf.s(conf=self,key=char, press=press)
        return self.orders(char, conf)
    def build_hand(self, conf, label='left'):
        orders = self.orders
        self.moves[label] = 0
        base = conf("base")
        vals = base.get("vals")
        val = base.get("val")
        self.bases[label] = vals
        ibase = vals.index(val)
        self.ibases[label] = ibase
        val,vals=conf("power").gets("val,vals")
        self.powers[label]=vals
        ipower=vals.index(val)
        self.ipowers[label] = ipower
        power=conf("power")
        keys = conf.get("keys")
        for k,v in keys.items():
            k = str(k)
            self.ks.key_color(k, label)
            def text_fc(v):
                def wrap():
                    return str(self.get_base(v, label))
                return wrap
            def power_fc(v):
                def wrap():
                    n = self.get_base(v, label)
                    power = self.get_power(label)
                    power = self.fix_power(n, power)
                    s = f"/{power}"
                    return s
                return wrap
            self.ks.bind_text(k, text_fc(v))
            self.ks.bind_note(k, power_fc(v))
            orders.push(k, self.make_sound(k,v,label))
        for key in ["up", "down"]:
            chars = base.get(key)
            if type(chars) not in (list, tuple):
                chars =[chars]
            chars =tuple(chars)
            orders.push(chars[0], self.make_base(chars,key,label))
            self.ks.key_color(chars[0], label+"_opt")
            self.ks.bind_text(chars[0], "N"+("+" if key == 'up' else '-'))
        for key in ['up', 'down']:
            orders.push(power.get(key), self.make_power(key,label))
            self.ks.key_color(power.get(key), label+"_opt")
            self.ks.bind_text(power.get(key), "V"+("+" if key == 'up' else '-'))
        val,key = conf("base").gets("move_val, move")
        orders.push(key, self.make_move(val, label))
        self.ks.bind_text(key, lambda : "V"+(f"+{val}" if val>0 else f"{val}"))
        self.ks.key_color(key, label+"_opt")
    def make_move(self, val, label):
        def fc(conf):
            if not conf.get("press"):
                self.moves[label] = 0
            else:
                self.moves[label] = val
            #print(f"moves[{label}]:", self.moves[label])
        return fc
    def make_power(self, way, label):
        def fc(conf):
            if not conf.get("press"):
                return
            if way=='up':
                self.ipowers[label] = min(self.ipowers[label]+1, len(self.powers[label])-1)
            else:
                self.ipowers[label] = max(self.ipowers[label]-1, 0)
            #print(f"{label} power change to {self.powers[label][self.ipowers[label]]}")
        return fc
    def make_base(self, chars, way,label):
        # 移动基准音
        assert len(chars) in [1,2]
        def fc(conf):
            if not conf.get("press"):
                return
            if way=='up':
                self.ibases[label] = min(self.ibases[label]+1, len(self.bases[label])-1)
            else:
                self.ibases[label] = max(self.ibases[label]-1, 0)
            #print(f"{label} base change to {self.bases[label][self.ibases[label]]}")
        def fc2(conf):
            c1 = chars[1]
            if not conf.get("press"):
                self.orders.pop(c1)
                return
            self.orders.push(c1, fc)
        if len(chars)==1:
            return fc
        return fc2
    def build_fc(self, conf):
        self.orders = Orders()
        self.bases = {}
        self.ibases = {}
        self.powers={}
        self.ipowers={}
        self.moves = {}
        self.mode = conf.get("mode", 0)
        self.soundfix = conf.get("soundfix")
        for key in ["left", "right"]:
            self.build_hand(conf(key), key)
        self.orders.push(conf.get("stop"), self.stop)
        self.ks.bind_text(conf.get("stop"), "stop")
        self.ks.key_color(conf.get("stop"), "opt")
        self.orders.set(conf.get("change_mode"), self.change_mode)
        self.ks.bind_text(conf.get("change_mode"), "mode")
        self.ks.bind_note(conf.get("change_mode"), lambda :str(self.mode))
        self.ks.key_color(conf.get("change_mode"), "opt")
        self.orders.set(conf.get("quit"), self.quit)
    def dv_sound(self, do_press, n, power):
        # 实际调用设备发音
        if not do_press:
            if self.mode==0:
                self.play.unpress(n, self.channel)
                with self.lock:
                    if n in self.to_stops:
                        self.to_stops.remove(n)
            return
        power = self.fix_power(n, power)
        self.play.press(n, power, self.channel)
        with self.lock:
            self.to_stops.add(n)
    def make_sound(self, key, val, label):
        def fc(conf):
            press = conf.get("press")
            offset = self.get_base(val, label)
            #print(f"offset: {offset}")
            power = self.get_power(label)
            return self.dv_sound(press, offset, power)
        return fc
    def get_base(self, val, label):
        return self.bases[label][self.ibases[label]]+val+self.moves[label]
    def get_power(self, label):
        return self.powers[label][self.ipowers[label]]
    def start(self):
        self.running = True
        self.play.start()
        self.background.start()
        self.ks.run()
    def close(self):
        self.ks.stop()
        self.background.stop()
        self.play.stop()
        self.play.close(self.save_fp)
    def stop(self, conf):
        for n in self.to_stops:
            self.play.unpress(n, self.channel)
        self.to_stops = set()
    def quit(self, conf):
        self.running = False
        input("press enter to quit:\n")
    def wait(self):
        import time
        while self.running:
            time.sleep(0.1)
    def change_mode(self, conf):
        #print(f"call change_mode: {do_press}, {a}, {b}")
        if not conf.get("press"):
            return
        self.mode = 1-self.mode
        #print(f"mode: {self.mode}")
    def fix_power(self, n,power):
        vmin, vmax = dz.g(self.soundfix, min=0, max=0)
        vdst = vmax-vmin
        n = min(max(n, 36), 132)
        rate = (n-36)/(132-36)
        #rate=rate*rate
        v = int(power+vmin+vdst*rate)
        #print(f"sound for {n}: {v}")
        return v


from buildz import argx
s_help = fz.fread(path("help.txt")).decode("utf-8")
def test():
    import time,sys
    ft = argx.Fetch(*xf.loads("[fp,sfile,libpath,default,help],{f:fp,s:sfile,l:libpath,t:default,b:background,h:help,w:width,h:height}"))
    rst = ft(sys.argv[1:])
    if 'help' in rst:
        print(s_help)
        return
    fps = []
    if 'fp' in rst:
        fps.append(path(rst['fp']))
        del rst['fp']
    default = '1'
    if 'default' in rst:
        default = rst['default']
        del rst['default']
    if 'background' in rst:
        background = rst['background']
        del rst['background']
        background = {'fp':background}
        rst['background'] = background
    if default in (0,'0'):
        default = None
    elif default in (1,'1'):
        default = conf_fp
    if default:
        fps = [path(default)]+fps
    sys_conf = {'init':rst}
    print("run success, enter 'esc' to quit")
    print("运行中,按下'esc'键来退出")
    conf = Conf(fps, sys_conf)
    conf.start()
    #conf.wait()
    #print("release")
    conf.close()

pass

pyz.lc(locals(), test)
'''
python -m musicz_pygm.run
'''