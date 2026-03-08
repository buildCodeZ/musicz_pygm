#
from buildz import Base
import pygame.midi
import time,threading
__doc__="""
输入输出
"""
class Play(Base):
    def select(self, channel=0, bank=0, preset=0):
        # 选择钢琴音色(通道0, 音色库0, 音色0)
        self.midi_out.set_instrument(channel)
    def press(self, key, power=90, channel=0):
        self.midi_out.note_on(key, power, channel)
        self.records.append(['press', key, power, channel, time.time()-self.base_sec])
    def unpress(self, key, channel=0):
        self.midi_out.note_off(key, 0, channel)
        self.records.append(['unpress', key, 0, channel, time.time()-self.base_sec])
    def init(self, fps=10, sample_rate = 44100):
        pygame.midi.init()
        self.base_sec = time.time()
        self.midi_out = pygame.midi.Output(0)
        self.select()
        self.sample_rate = sample_rate
        self.fps = fps
        self.running = True
        self.done_run = False
        self.th = None
        self.records = []
    def start(self):
        pass
    def stop(self):
        self.running = False
    def close(self, save = None):
        if save is not None:
            self.save(save)
    def save(self, fp):
        import json
        fp = time.strftime(fp)
        dt = json.dumps(self.records).encode("utf-8")
        print(f"save to {fp}")
        with open(fp, 'wb') as file:
            file.write(dt)

pass