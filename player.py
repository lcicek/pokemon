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

    def turn(self, delta_x, delta_y):
        self.update_direction(delta_x= delta_x, delta_y=delta_y)

    def update_position(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y

    def update_move_bit(self):
        self.move_bit ^= 1 # flip bit

    def update_move_state(self):
        self.move_state = (self.action, self.direction)

    def update_action(self, action):
        self.action = action
        self.update_move_state()

    def update_direction(self, delta_x, delta_y):
        delta = (delta_x, delta_y)

        if delta == (-1, 0):
            self.direction = LEFT
        elif delta == (1, 0):
            self.direction = RIGHT
        elif delta == (0, -1):
            self.direction = UP
        elif delta == (0, 1):
            self.direction = DOWN
        else:
            raise RuntimeError("The delta_x, delta_y tuple is invalid.")

        self.update_move_bit()
        self.update_move_state()

    def is_in_bounds(self, location, delta_x, delta_y):
        """ Returns true if the next move is still in bounds of location."""
        next_x = self.x + delta_x
        next_y = self.y + delta_y

        return next_x >= 0 or next_y >= 0 or next_x < location.max_x or next_y < location.max_y