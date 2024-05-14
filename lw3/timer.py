from pygame.time import get_ticks


class Timer:
    def __init__(self, duration, func=None, repeat=False):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat
        self.current_time = get_ticks()

    def activate(self):
        if not self.active:
            self.active = True
            self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        self.current_time = get_ticks()
        if self.current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate()
