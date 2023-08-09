class Animation:
    def __init__(self, frames, length, duration) -> None:
        self.frames = frames
        self.length = length
        self.duration = duration
        
        self.direction = None
        self.frame_number = 0
        self.time_per_frame = self.duration // self.length

        assert self.duration % self.length == 0

    def update_frame_number(self):
        pass

    def get_frame(self):
        return self.frames[self.direction][self.frame_number].scaled_image

    def update_direction(self, direction):
        self.direction = direction

    def next_frame(self):
        self.frame_number = (self.frame_number + 1) % self.length

    def rescale_frames(self, scale):
        for _, cycle in self.frames.items():
            for frame in cycle:
                frame.rescale(scale)
    
class WalkAnimation(Animation):
    def __init__(self, frames, length, duration) -> None:
        super().__init__(frames, length, duration)

        self.time_per_frame = self.duration

    def update_frame_number(self, state_time):
        self.frame_number = state_time % self.length

class JumpAnimation(Animation):
    def __init__(self, frames, length, duration) -> None:
        super().__init__(frames, length, duration)

    def update_frame_number(self, frames_since_start):
        self.frame_number = (frames_since_start-1) // self.time_per_frame