class Lock:
    def __init__(self) -> None:
        self.locked = False

    def unlock(self):
        self.locked = False

    def lock(self):
        self.locked = True

    def is_unlocked(self):
        return not self.locked

    def is_locked(self):
        return self.locked

    def is_newly_locked(self):
        return self.frames_since_start == 1

class MovementLock(Lock):
    def __init__(self) -> None:
        super().__init__()

        self.frames_since_start = None
        self.lock_duration = None

    def lock(self, lock_duration):
        self.locked = True
        self.lock_duration = lock_duration
        self.frames_since_start = 1

    def update(self):
        self.frames_since_start += 1

        if self.frames_since_start > self.lock_duration:
            self.locked = False
            self.lock_duration = None
    
    def will_be_unlocked(self):
        return self.locked and self.frames_since_start == self.lock_duration