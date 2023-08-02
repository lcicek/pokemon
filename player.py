from playerAnimation import PlayerAnimation
from parameters import (
    LEFT, RIGHT, UP, DOWN, 
    STANDING, WALKING, SPRINTING
)

class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

        self.action = STANDING # STANDING, WALKING, SPRINTING
        self.direction = DOWN # LEFT, RIGHT, UP, DOWN
        self.move_state = (self.action, self.direction)
        self.move_bit = 0 # to track left and right step for animation (no matter the direction)

        self.animation = PlayerAnimation()

    def turns(self, new_direction):
        return self.direction != new_direction

    def is_standing(self):
        return self.action == STANDING

    def update_animation(self):
        self.animation.update_active_frame(self.move_state, self.move_bit)

    def update_position(self, direction):
        if direction == UP:
            self.y -= 1
        elif direction == DOWN:
            self.y += 1
        elif direction == LEFT:
            self.x -= 1
        elif direction == RIGHT:
            self.x += 1
        else:
            raise RuntimeError("Invalid value for direction.")

    def update_move_bit(self):
        self.move_bit ^= 1 # flip bit

    def update_move_state(self):
        self.move_state = (self.action, self.direction)

    def update_action(self, action):
        self.action = action

        if action != STANDING:
            self.update_move_bit()
        
        self.update_move_state()

    def update_direction(self, new_direction):
        self.direction = new_direction
        self.update_move_state()

    def is_in_bounds(self, location, delta_x, delta_y):
        """ Returns true if the next move is still in bounds of location."""
        next_x = self.x + delta_x
        next_y = self.y + delta_y

        return next_x >= 0 or next_y >= 0 or next_x < location.max_x or next_y < location.max_y