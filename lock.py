class MovementLock:
    def __init__(self) -> None:
        self.locked = False
        self.frames_since_start = None
        self.lock_duration = None

    def is_unlocked(self):
        return not self.locked

    def is_locked(self):
        return self.locked

    def lock(self, lock_duration):
        self.locked = True
        self.lock_duration = lock_duration
        self.frames_since_start = 1

    def update(self):
        if self.is_unlocked():
            return

        self.frames_since_start += 1

        if self.frames_since_start > self.lock_duration:
            self.locked = False
            self.lock_duration = None