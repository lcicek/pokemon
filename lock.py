from pygame import time
from parameters import FRAMES_PER_WALK, FRAMES_PER_STANDING_TURN, FRAMES_PER_JUMP, FRAMES_PER_SPRINT

class Lock:
    def __init__(self) -> None:
        self.locked = False
        self.frames_since_lock = None
        self.lock_duration = None

    def frame_count(self):
        assert self.frames_since_lock is not None
        
        return self.frames_since_lock

    def is_unlocked(self):
        return not self.locked

    def is_locked(self):
        return self.locked

    def lock(self, player):
        self.set_lock_duration(player)
        self.locked = True
        self.frames_since_lock = 1

    def set_lock_duration(self, player):
        if player.is_walking():
            self.lock_duration = FRAMES_PER_WALK
        elif player.is_jumping():
            self.lock_duration = FRAMES_PER_JUMP
        elif player.is_sprinting():
            self.lock_duration = FRAMES_PER_SPRINT
        else:
            self.lock_duration = FRAMES_PER_STANDING_TURN

    def unlock(self):
        self.locked = False
        self.frames_since_lock = None
        self.lock_duration = None

    def try_unlock(self):
        lock_elapsed = self.frames_since_lock >= self.lock_duration

        if lock_elapsed:
            self.unlock()
        else:
            self.frames_since_lock += 1
        
        return lock_elapsed