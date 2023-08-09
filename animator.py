from graphic import Graphic
from animation import Animation, WalkAnimation, JumpAnimation
from constant.paths import *
from constant.parameters import (
    LEFT, RIGHT, UP, DOWN,
    STANDING, WALKING, JUMPING, SPRINTING,
    JUMP_CYCLE_LENGTH, WALK_CYCLE_LENGTH, SPRINT_CYCLE_LENGTH,
    FRAMES_PER_WALK, FRAMES_PER_SPRINT, FRAMES_PER_JUMP
)

class Animator:
    def __init__(self) -> None:
        stand_frames, walk_frames, sprint_frames, jump_frames = self.init_player_frames()

        self.player_animations = {
            STANDING: Animation(stand_frames, 1, 0),
            WALKING: WalkAnimation(walk_frames, WALK_CYCLE_LENGTH, FRAMES_PER_WALK),
            SPRINTING: WalkAnimation(sprint_frames, SPRINT_CYCLE_LENGTH, FRAMES_PER_SPRINT),
            JUMPING: JumpAnimation(jump_frames, JUMP_CYCLE_LENGTH, FRAMES_PER_JUMP)
        }

        self.active_player_animation = self.player_animations[STANDING]

    def get_active_player_frame(self):
        return self.active_player_animation.get_frame().scaled_image

    def animate_player(self, player, move_lock):
        self.active_player_animation = self.player_animations[player.action]
        self.active_player_animation.update_direction(player.direction)

        if player.is_jumping():
            self.active_player_animation.update_frame_number(move_lock.frames_since_start)
        elif player.is_walking() or player.is_sprinting():
            self.active_player_animation.update_frame_number(player.continuous_steps)

    def rescale(self, scale):
        for _, animation in self.player_animations.items():
            animation.rescale_frames(scale)

    def init_player_frames(self):
        stand_frames = {
            DOWN: [Graphic(STANDING_FRONT)],
            UP: [Graphic(STANDING_BACK)],
            LEFT: [Graphic(STANDING_LEFT)],
            RIGHT: [Graphic(STANDING_RIGHT)]
        }

        walk_frames = {
            DOWN: [Graphic(WALKING_FRONT), Graphic(STANDING_FRONT), Graphic(WALKING_FRONT_2), Graphic(STANDING_FRONT)],
            UP: [Graphic(WALKING_BACK), Graphic(STANDING_BACK), Graphic(WALKING_BACK_2), Graphic(STANDING_BACK)],
            LEFT: [Graphic(WALKING_LEFT), Graphic(STANDING_LEFT), Graphic(WALKING_LEFT_2), Graphic(STANDING_LEFT)],
            RIGHT: [Graphic(WALKING_RIGHT), Graphic(STANDING_RIGHT), Graphic(WALKING_RIGHT_2), Graphic(STANDING_RIGHT)]
        }
        
        sprint_frames = {
            DOWN: [Graphic(SPRINTING_DOWN_1), Graphic(SPRINTING_DOWN_2), Graphic(SPRINTING_DOWN_3), Graphic(SPRINTING_DOWN_2)],
            UP: [Graphic(SPRINTING_UP_1), Graphic(SPRINTING_UP_2), Graphic(SPRINTING_UP_3), Graphic(SPRINTING_UP_2)],
            LEFT: [Graphic(SPRINTING_LEFT_1), Graphic(SPRINTING_LEFT_2), Graphic(SPRINTING_LEFT_3), Graphic(SPRINTING_LEFT_2)],
            RIGHT: [Graphic(SPRINTING_RIGHT_1), Graphic(SPRINTING_RIGHT_2), Graphic(SPRINTING_RIGHT_3), Graphic(SPRINTING_RIGHT_2)]
        }

        jump_frames = {
            DOWN: [Graphic(JUMPING_DOWN_1), Graphic(JUMPING_DOWN_2), Graphic(JUMPING_DOWN_3)],
            UP: [Graphic(JUMPING_UP_1), Graphic(JUMPING_UP_2), Graphic(JUMPING_UP_3)],
            LEFT: [Graphic(JUMPING_LEFT_1), Graphic(JUMPING_LEFT_2), Graphic(JUMPING_LEFT_3)],
            RIGHT: [Graphic(JUMPING_RIGHT_1), Graphic(JUMPING_RIGHT_2), Graphic(JUMPING_RIGHT_3)]
        }

        return stand_frames, walk_frames, sprint_frames, jump_frames