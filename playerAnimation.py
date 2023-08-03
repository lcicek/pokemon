from graphic import Graphic
from parameters import (
    STANDING_FRONT, STANDING_BACK, STANDING_LEFT, STANDING_RIGHT,
    WALKING_FRONT, WALKING_BACK, WALKING_LEFT, WALKING_RIGHT,
    WALKING_FRONT_2, WALKING_BACK_2, WALKING_LEFT_2, WALKING_RIGHT_2,
    LEFT, RIGHT, UP, DOWN,
    STANDING, WALKING, SPRINTING
)

class PlayerAnimation:
    def __init__(self) -> None:
        self.frames = []
        self.active_frame = None

        self.initialize_frames()
        self.initialize_active_frame()

    def initialize_active_frame(self):
        self.active_frame = self.frames[0][(STANDING, DOWN)].scaled_image

    def initialize_frames(self):
        standing_frames = {
            (STANDING, DOWN): Graphic(STANDING_FRONT),
            (STANDING, UP): Graphic(STANDING_BACK),
            (STANDING, LEFT): Graphic(STANDING_LEFT),
            (STANDING, RIGHT): Graphic(STANDING_RIGHT)
        }

        walk_cycle_frames = {
            (WALKING, DOWN): [Graphic(WALKING_FRONT), Graphic(STANDING_FRONT), Graphic(WALKING_FRONT_2), Graphic(STANDING_FRONT)],
            (WALKING, UP): [Graphic(WALKING_BACK), Graphic(STANDING_BACK), Graphic(WALKING_BACK_2), Graphic(STANDING_BACK)],
            (WALKING, LEFT): [Graphic(WALKING_LEFT), Graphic(STANDING_LEFT), Graphic(WALKING_LEFT_2), Graphic(STANDING_LEFT)],
            (WALKING, RIGHT): [Graphic(WALKING_RIGHT), Graphic(STANDING_RIGHT), Graphic(WALKING_RIGHT_2), Graphic(STANDING_RIGHT)]
        }

        frames = []
        frames.extend([standing_frames, walk_cycle_frames])
        self.frames = frames

    def update_active_frame(self, move_state, move_frame=None):
        if move_state in self.frames[0]:
            self.active_frame = self.get_standing_frame(move_state)
        elif move_state in self.frames[1] and move_frame is not None:
            self.active_frame = self.get_walking_frame(move_state=move_state, move_frame=move_frame)
        else:
            raise RuntimeError("Found invalid state while trying to find current player frame.")

    def get_standing_frame(self, move_state):
        return self.frames[0][move_state].scaled_image
    
    def get_walking_frame(self, move_state, move_frame):
        walk_frames = self.frames[1][move_state]
        frame = walk_frames[move_frame]

        return frame.scaled_image