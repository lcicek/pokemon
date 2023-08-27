from copy import deepcopy

from graphic import Graphic
from animation import Animation, MoveAnimation, WalkAnimation
from constant.paths import *
from constant.parameters import (
    LEFT, RIGHT, UP, DOWN,
    STANDING, WALKING, JUMPING, SPRINTING,
    JUMP_CYCLE_LENGTH, WALK_CYCLE_LENGTH, SPRINT_CYCLE_LENGTH,
    FRAMES_PER_WALK, FRAMES_PER_SPRINT, FRAMES_PER_JUMP, FRAMES_PER_GRASS_ANIMATION
)

class Animator:
    def __init__(self) -> None:
        self.init_player_animations() # sets self.player_animations

        self.active_player_animation = self.player_animations[STANDING]
        self.active_player_animation.update_direction(DOWN) # default
        
        self.grass_animations = []

    def get_active_player_frame(self):
        return self.active_player_animation.get_frame()

    def update_active_player_animation(self, player):
        self.active_player_animation = self.player_animations[player.action]
        self.active_player_animation.update_direction(player.direction)
        self.active_player_animation.start()

    def animate(self, location, player, move_lock):
        self.animate_player(player)
        self.add_grass_animation(location, player, move_lock)

        if len(self.grass_animations) > 0:
            self.animate_grass()

    def animate_grass(self):
        remove = []
        for i, animation_tuple in enumerate(self.grass_animations):
            anim = animation_tuple[1]
            anim.timestep()

            if anim.frames_since_start > anim.duration: 
                remove.append(i)

        for index in remove:
            self.grass_animations.pop(index)

    def animate_player(self, player):
        state_changed = not (self.player_animations[player.action] == self.active_player_animation and self.active_player_animation.direction == player.direction)
        
        if state_changed:
            self.update_active_player_animation(player)
        
        self.active_player_animation.timestep()

    def add_grass_animation(self, location, player, move_lock):
        movement_is_new = move_lock.is_locked() and move_lock.frames_since_start == 1

        if player.is_moving() and movement_is_new and location.square_is_grass(row=player.y, col=player.x):
            index = self.grass_animation_exists(player.x, player.y)

            if index is not None:
                self.grass_animations.pop(index) # delete old animation if exists
            
            self.grass_animations.append(((player.x, player.y), self.new_grass_animation()))

    def grass_animation_exists(self, x, y):
        for i, anim in enumerate(self.grass_animations):
            if anim[0][0] == x and anim[0][1] == y:
                return i
        
        return None

    def rescale(self, scale):
        for _, anim in self.player_animations.items():
            anim.rescale_frames(scale)

        for anim in self.grass_animations:
            anim.rescale_frames(scale)

    def new_grass_animation(self):
        return Animation([Graphic(GRASS_1), Graphic(GRASS_2), Graphic(GRASS_3)], 3, FRAMES_PER_GRASS_ANIMATION)

    def init_player_animations(self):
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

        self.player_animations = {
            STANDING: MoveAnimation(stand_frames, 1, 1),
            WALKING: WalkAnimation(walk_frames, WALK_CYCLE_LENGTH, FRAMES_PER_WALK),
            SPRINTING: WalkAnimation(sprint_frames, SPRINT_CYCLE_LENGTH, FRAMES_PER_SPRINT),
            JUMPING: MoveAnimation(jump_frames, JUMP_CYCLE_LENGTH, FRAMES_PER_JUMP)
        }