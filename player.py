from playerAnimation import PlayerAnimation
from parameters import (
    LEFT, RIGHT, UP, DOWN, 
    STANDING, WALKING, JUMPING,
    WALK_CYCLE_FRAMES, FRAMES_PER_JUMP_CYCLE_KEYFRAME
)

class Player:
    def __init__(self) -> None:
        self.x = 10
        self.y = 11

        self.prev_x = 10
        self.prev_y = 11

        self.action = STANDING # STANDING, WALKING, SPRINTING
        self.direction = DOWN # LEFT, RIGHT, UP, DOWN
        self.move_state = (self.action, self.direction)
        self.cycle_frame = 0 # 4 possible frames per move/jump cycle

        self.animation = PlayerAnimation()

    def get_previous_delta(self):
        delta_x = self.x - self.prev_x
        delta_y = self.y - self.prev_y

        return delta_x, delta_y

    def turns(self, new_direction):
        return self.direction != new_direction

    def is_jumping(self):
        return self.action == JUMPING

    def is_walking(self):
        return self.action == WALKING

    def is_standing(self):
        return self.action == STANDING

    def bumped(self):
        return self.prev_x == self.x and self.prev_y == self.y

    def update_animation(self):
        self.animation.update_active_frame(self.move_state, self.cycle_frame)

    def update_previous_position(self):
        self.prev_x = self.x
        self.prev_y = self.y

    def step(self, direction, step_size):
        if direction == UP:
            self.y -= step_size
        elif direction == DOWN:
            self.y += step_size
        elif direction == LEFT:
            self.x -= step_size
        elif direction == RIGHT:
            self.x += step_size
        else:
            raise RuntimeError("Invalid value for direction.")

    def jump(self, direction):
        self.update_previous_position()
        self.step(direction, step_size=2)

    def walk(self, direction):
        self.next_move_frame()
        self.update_previous_position()
        self.step(direction, step_size=1)

    def update_jump_frame(self, frames):
        if frames % FRAMES_PER_JUMP_CYCLE_KEYFRAME == 0:
            self.cycle_frame += 1
            self.update_animation()

    def next_move_frame(self):
        self.cycle_frame = (self.cycle_frame + 1) % WALK_CYCLE_FRAMES

    def update_move_state(self):
        self.move_state = (self.action, self.direction)

    def update_action(self, action):
        if self.action == action:
            return

        if action == WALKING:
            self.cycle_frame = 0 if self.cycle_frame >= 2 else 2 # set correct spot in walk cycle
        elif action == JUMPING:
            self.cycle_frame = 0

        self.action = action
        self.update_move_state()

    def update_direction(self, new_direction):
        self.direction = new_direction
        self.update_move_state()

    def is_at_edge(self, location):
        return self.x == 0 or self.y == 0 or self.x == location.width-1 or self.y == location.height-1