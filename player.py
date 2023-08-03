from playerAnimation import PlayerAnimation
from parameters import (
    LEFT, RIGHT, UP, DOWN, 
    STANDING, WALKING,
    WALK_CYCLE_FRAMES
)

class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

        self.prev_x = 0
        self.prev_y = 0

        self.action = STANDING # STANDING, WALKING, SPRINTING
        self.direction = DOWN # LEFT, RIGHT, UP, DOWN
        self.move_state = (self.action, self.direction)
        self.move_frame = 0 # 4 possible frames per move cycle

        self.animation = PlayerAnimation()

    def get_previous_delta(self):
        delta_x = self.x - self.prev_x
        delta_y = self.y - self.prev_y

        return delta_x, delta_y

    def turns(self, new_direction):
        return self.direction != new_direction

    def is_walking(self):
        return self.action == WALKING

    def is_standing(self):
        return self.action == STANDING

    def bumped(self):
        return self.prev_x == self.x and self.prev_y == self.y

    def update_animation(self):
        self.animation.update_active_frame(self.move_state, self.move_frame)

    def update_previous_position(self):
        self.prev_x = self.x
        self.prev_y = self.y

    def update_position(self, direction):
        self.next_move_frame()
        self.update_previous_position()

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

    def next_move_frame(self):
        self.move_frame = (self.move_frame + 1) % WALK_CYCLE_FRAMES

    def update_move_state(self):
        self.move_state = (self.action, self.direction)

    def update_action(self, action):
        if self.action == action:
            return

        if action == WALKING:
            self.move_frame = 0 if self.move_frame >= 2 else 2 # set correct spot in walk cycle

        self.action = action
        self.update_move_state()

    def update_direction(self, new_direction):
        self.direction = new_direction
        self.update_move_state()

    def is_at_edge(self, location):
        return self.x == 0 or self.y == 0 or self.x == location.width-1 or self.y == location.height-1

    def next_is_out_of_bounds(self, location, direction):
        return not self.next_is_in_bounds(location, direction)

    def next_is_in_bounds(self, location, direction):
        """ Returns true if the next move is still in bounds of location."""
        next_x = self.x
        next_y = self.y

        if direction == LEFT:
            next_x -= 1
        elif direction == RIGHT:
            next_x += 1
        elif direction == UP:
            next_y -= 1
        else:
            next_y += 1

        return next_x >= 0 and next_y >= 0 and next_x < location.width and next_y < location.height