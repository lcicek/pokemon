from pygame import time

class Lock:
    def __init__(self, duration) -> None:
        self.locked = False
        self.start_time = -1
        self.duration = duration
    
    def is_unlocked(self):
        return not self.locked

    def is_locked(self):
        return self.locked

    def lock(self, start_time):
        self.locked = True
        self.start_time = start_time

    def try_unlock(self):
        if self.time_elapsed():
            self.locked = False

    def time_elapsed(self):
        current_time = time.get_ticks()
        return current_time - self.start_time >= self.duration