from graphic import Graphic
from animationPaths import *
from parameters import (
    LEFT, RIGHT, UP, DOWN,
    STANDING, WALKING, JUMPING, SPRINTING,
    JUMP_CYCLE_LENGTH,
    WALK_CYCLE_LENGTH, SPRINT_CYCLE_LENGTH
)

class PlayerAnimation:
    def __init__(self) -> None:
        self.frames = []
        self.active_frame = None
        self.keyframe = 0

        self.initialize_frames()
        self.initialize_active_frame()

    def initialize_active_frame(self):
        self.active_frame = self.frames[0][(STANDING, DOWN)].scaled_image

    def set_active_frame(self, move_state):
        if move_state in self.frames[0]:
            self.active_frame = self.get_standing_frame(move_state)
            return

        if move_state in self.frames[1]:
            self.active_frame = self.get_move_frame(move_state, 1)
            self.next_walk_frame()
        elif move_state in self.frames[2]:
            self.active_frame = self.get_move_frame(move_state, 2)
            self.next_sprint_frame()
        elif move_state in self.frames[3]:
            self.active_frame = self.get_move_frame(move_state, 3)
        else:
            raise RuntimeError(f"Found invalid state {move_state} while trying to find current player frame.")

    def get_standing_frame(self, move_state):
        return self.frames[0][move_state].scaled_image
    
    def get_move_frame(self, move_state, state_index):
        move_frames = self.frames[state_index][move_state]
        frame = move_frames[self.keyframe]

        return frame.scaled_image

    def next_jump_frame(self):
        self.keyframe = (self.keyframe + 1) % JUMP_CYCLE_LENGTH

    def next_walk_frame(self):
        self.keyframe = (self.keyframe + 1) % WALK_CYCLE_LENGTH

    def next_sprint_frame(self):
        self.keyframe = (self.keyframe + 1) % SPRINT_CYCLE_LENGTH

    def reset_walk_cycle(self):
        self.keyframe = 0 if self.keyframe >= 2 else 2 # set correct spot in walk cycle

    def reset_keyframe(self, action):
        if action == STANDING:
            return

        if action == WALKING or action == SPRINTING:
            self.reset_walk_cycle()
        elif action == JUMPING:
            self.keyframe = 0
    
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
            (JUMPING, DOWN): [Graphic(JUMPING_DOWN_1), Graphic(JUMPING_DOWN_2), Graphic(JUMPING_DOWN_3)],
            (JUMPING, UP): [Graphic(JUMPING_UP_1), Graphic(JUMPING_UP_2), Graphic(JUMPING_UP_3)],
            (JUMPING, LEFT): [Graphic(JUMPING_LEFT_1), Graphic(JUMPING_LEFT_2), Graphic(JUMPING_LEFT_3)],
            (JUMPING, RIGHT): [Graphic(JUMPING_RIGHT_1), Graphic(JUMPING_RIGHT_2), Graphic(JUMPING_RIGHT_3)]
        }
        
        sprint_cycle_frames = {
            (SPRINTING, DOWN): [Graphic(SPRINTING_DOWN_1), Graphic(SPRINTING_DOWN_2), Graphic(SPRINTING_DOWN_3), Graphic(SPRINTING_DOWN_2)],
            (SPRINTING, UP): [Graphic(SPRINTING_UP_1), Graphic(SPRINTING_UP_2), Graphic(SPRINTING_UP_3), Graphic(SPRINTING_UP_2)],
            (SPRINTING, LEFT): [Graphic(SPRINTING_LEFT_1), Graphic(SPRINTING_LEFT_2), Graphic(SPRINTING_LEFT_3), Graphic(SPRINTING_LEFT_2)],
            (SPRINTING, RIGHT): [Graphic(SPRINTING_RIGHT_1), Graphic(SPRINTING_RIGHT_2), Graphic(SPRINTING_RIGHT_3), Graphic(SPRINTING_RIGHT_2)]
        }

        frames = []
        frames.extend([standing_frames, walk_cycle_frames, sprint_cycle_frames, jump_cycle_frames])
        self.frames = frames
