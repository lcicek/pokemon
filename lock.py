from pygame import time
from parameters import FRAMES_PER_WALK, FRAMES_PER_STANDING_TURN

class Lock:
    def __init__(self) -> None:
        self.locked = False
        self.frames_since_lock = None

    def get_frame_number(self):
        return self.frames_since_lock

    def is_unlocked(self):
        return not self.locked

    def is_locked(self):
        return self.locked

    def lock(self):
        self.locked = True
        self.frames_since_lock = 1

    def try_unlock(self, standing=False):
        if self.is_unlocked():
            return

        if self.time_elapsed(standing=standing):
            self.locked = False
            self.frames_since_lock = None
        else:
            self.frames_since_lock += 1

    def time_elapsed(self, standing):
        if standing:
            return self.frames_since_lock >= FRAMES_PER_STANDING_TURN
        else:
            return self.frames_since_lock >= FRAMES_PER_WALK