from playerAnimation import PlayerAnimation
from parameters import (
    LEFT, RIGHT, UP, DOWN, 
    STANDING, WALKING, SPRINTING, JUMPING
)

class Player:
    def __init__(self) -> None:
        self.x = 10
        self.y = 11

        self.prev_x = 10
        self.prev_y = 11

        self.action = STANDING # STANDING, WALKING, SPRINTING
        self.direction = DOWN # LEFT, RIGHT, UP, DOWN

        self.animation = PlayerAnimation()

    def get_previous_delta(self):
        delta_x = self.x - self.prev_x
        delta_y = self.y - self.prev_y

        return delta_x, delta_y

    def update_previous_position(self):
        self.prev_x = self.x
        self.prev_y = self.y

    def step(self, step_size):
        if self.direction == UP:
            self.y -= step_size
        elif self.direction == DOWN:
            self.y += step_size
        elif self.direction == LEFT:
            self.x -= step_size
        elif self.direction == RIGHT:
            self.x += step_size
        else:
            raise RuntimeError("Invalid value for direction.")

    def update_position(self):
        self.update_previous_position()

        if self.action == JUMPING:
            self.step(step_size=2)
        elif self.action == WALKING or self.action == SPRINTING:
            self.step(step_size=1)

    def update_animation(self):
        move_state = (self.action, self.direction)
        self.animation.update_active_frame(move_state)

    def update_state(self, action, direction):
        if action is not None and self.action != action:
            self.action = action
            self.animation.reset_keyframe(action)
        
        if direction is not None:
            self.direction = direction

    def update(self, action=None, direction=None, move=False):
        assert action is not None or direction is not None
        
        self.update_state(action, direction)
        self.update_animation()

        if move:
            self.update_position()

    def is_at_edge(self, location):
        return self.x == 0 or self.y == 0 or self.x == location.width-1 or self.y == location.height-1

    def turns(self, new_direction):
        return self.direction != new_direction

    def is_jumping(self):
        return self.action == JUMPING

    def is_walking(self):
        return self.action == WALKING

    def is_sprinting(self):
        return self.action == SPRINTING

    def is_standing(self):
        return self.action == STANDING

    def bumped(self):
        return self.prev_x == self.x and self.prev_y == self.y
    
    def get_move_state(self):
        return (self.action, self.direction)