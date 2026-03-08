#

from buildz import Base, dz, fz, xf
import time,threading
import json
class FileRead(Base):
    def load(self):
        if self.fp is None:
            self.datas = None
            return
        s = fz.read(self.fp).decode()
        datas = json.loads(s)
        self.datas = datas
        #dz.fill(info, self.info, replace=1)
        loop, stop,power_rate, speed_rate = dz.g(self.info, loop=True, stop=False, power_rate=0.7, speed_rate=1.0)
        self.loop = loop
        self.stop_after_play = stop
        self.power_rate = power_rate
        self.speed_rate = speed_rate
    def init(self, maps, obj):
        maps = maps or {}
        self.th = None
        self.running = True
        self.obj = obj
        self.fp = dz.g(maps, fp=None)
        self.info = maps
        self.load()
    def presses(self, arr):
        rst = []
        for k in arr:
            rst+= spts_ks(k)
        for k in rst:
            if check_empty(k):
                continue
            n = key2offset[k]-base_offset+self.base
            self.obj.dv_sound(True,n,self.power)
    def single(self):
        curr=None
        curr_time=time.time()
        base_sec = time.time()
        curr_sec = base_sec
        for dt in self.datas:
            if not self.running:
                break
            press_type, key, power, channel, sec = dt
            sec = sec*self.speed_rate
            assert press_type in {"press", "unpress"}
            diff = sec-curr_sec+base_sec
            if diff>0:
                while time.time()-curr_sec<diff:
                    time.sleep(min(diff, 0.01))
                curr_sec=time.time()
            self.obj.dv_sound(press_type=="press",key,power*self.power_rate, True)
    def run(self):
        if self.datas is None:
            return
        self.running = True
        while self.running:
            self.single()
            if not self.loop:
                break
        if self.running and self.stop_after_play:
            time.sleep(self.sec*0.25)
            self.obj.quit()
    def stop(self):
        self.running = False
    def start(self):
        if self.th is not None:
            return
        self.th = threading.Thread(target=self.run, daemon=True)
        self.th.start()