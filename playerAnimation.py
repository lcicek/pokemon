from graphic import Graphic
from parameters import (
    STANDING_FRONT, STANDING_BACK, STANDING_LEFT, STANDING_RIGHT,
    WALKING_FRONT, WALKING_FRONT_2,
    WALKING_BACK, WALKING_BACK_2, 
    WALKING_LEFT, WALKING_LEFT_2,
    WALKING_RIGHT, WALKING_RIGHT_2,
    JUMPING_DOWN_1, JUMPING_DOWN_2, JUMPING_DOWN_3,
    JUMPING_UP_1, JUMPING_UP_2, JUMPING_UP_3,
    JUMPING_LEFT_1, JUMPING_LEFT_2, JUMPING_LEFT_3, 
    JUMPING_RIGHT_1, JUMPING_RIGHT_2, JUMPING_RIGHT_3,
    LEFT, RIGHT, UP, DOWN,
    STANDING, WALKING, JUMPING
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

        jump_cycle_frames = {
            (JUMPING, DOWN): [Graphic(JUMPING_DOWN_1), Graphic(JUMPING_DOWN_2), Graphic(JUMPING_DOWN_3), Graphic(STANDING_FRONT)],
            (JUMPING, UP): [Graphic(JUMPING_UP_1), Graphic(JUMPING_UP_2), Graphic(JUMPING_UP_3), Graphic(STANDING_BACK)],
            (JUMPING, LEFT): [Graphic(JUMPING_LEFT_1), Graphic(JUMPING_LEFT_2), Graphic(JUMPING_LEFT_3), Graphic(STANDING_LEFT)],
            (JUMPING, RIGHT): [Graphic(JUMPING_RIGHT_1), Graphic(JUMPING_RIGHT_2), Graphic(JUMPING_RIGHT_3), Graphic(STANDING_RIGHT)]
        }

        frames = []
        frames.extend([standing_frames, walk_cycle_frames, jump_cycle_frames])
        self.frames = frames

    def update_active_frame(self, move_state, move_frame=None):
        if move_state in self.frames[0]:
            self.active_frame = self.get_standing_frame(move_state)
        elif move_state in self.frames[1] and move_frame is not None:
            self.active_frame = self.get_move_frame(move_state, move_frame, 1)
        elif move_state in self.frames[2] and move_frame is not None:
            self.active_frame = self.get_move_frame(move_state, move_frame, 2)
        else:
            print(move_state)
            raise RuntimeError("Found invalid state while trying to find current player frame.")

    def rescale_stand_frames(self, scale):
        for _, frame in self.frames[0].items():
            frame.rescale(scale)

    def rescale_walk_frames(self, scale):
        for _, frames in self.frames[1].items():
            for frame in frames:
                frame.rescale(scale)

    def rescale(self, scale):
        self.rescale_stand_frames(scale)
        self.rescale_walk_frames(scale)

    def get_standing_frame(self, move_state):
        return self.frames[0][move_state].scaled_image
    
    def get_move_frame(self, move_state, move_frame, state_index):
        walk_frames = self.frames[state_index][move_state]
        frame = walk_frames[move_frame]

        return frame.scaled_image