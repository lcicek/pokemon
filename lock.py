from pygame import time
from parameters import FRAMES_PER_WALK, FRAMES_PER_STANDING_TURN

class Lock:
    def __init__(self) -> None:
        self.locked = False
        self.frames_since_lock = None

    def frame_count(self):
        assert self.frames_since_lock is not None
        
        return self.frames_since_lock

    def is_unlocked(self):
        return not self.locked

    def is_locked(self):
        return self.locked

    def lock(self):
        self.locked = True
        self.frames_since_lock = 1

    def try_unlock(self, player_is_walking):
        if self.is_unlocked():
            return

        if self.lock_elapsed(player_is_walking):
            self.locked = False
        else:
            self.frames_since_lock += 1

    def lock_elapsed(self, player_is_walking):
        if player_is_walking:
            lock_duration = FRAMES_PER_WALK
        else:
            lock_duration = FRAMES_PER_STANDING_TURN

        return self.frames_since_lock >= lock_duration