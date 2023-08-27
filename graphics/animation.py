class Animation:
    def __init__(self, frames, length, duration) -> None:
        self.frames = frames
        self.length = length
        self.duration = duration

        self.frames_since_start = 0
        self.frame_number = 0
        self.time_per_frame = self.duration // self.length
        
        assert self.duration % self.length == 0

    def start(self):
        self.frames_since_start = 0
        self.frame_number = 0

    def timestep(self):
        self.frames_since_start += 1
        self.update_frame()

    def update_frame(self):
        if self.frames_since_start % (self.time_per_frame+1) == 0:
            self.frame_number = (self.frame_number + 1) % self.length

    def get_frame(self):
        return self.frames[self.frame_number].scaled_image
    
    def rescale_frames(self, scale):
        for frame in self.frames:
            frame.rescale(scale)

class MoveAnimation(Animation):
    def __init__(self, frames, length, duration) -> None:
        super().__init__(frames, length, duration)
        self.direction = None

    def get_frame(self):
        return self.frames[self.direction][self.frame_number].scaled_image

    def update_direction(self, direction):
        self.direction = direction

    def rescale_frames(self, scale):
        for _, cycle in self.frames.items():
            for frame in cycle:
                frame.rescale(scale)
    
class WalkAnimation(MoveAnimation):
    def __init__(self, frames, length, duration) -> None:
        super().__init__(frames, length, duration)
        self.time_per_frame = self.duration