from constant.parameters import (
    LEFT, RIGHT, UP, DOWN, 
    STANDING, WALKING, SPRINTING, JUMPING,
    X_HALF, Y_HALF
)

class Player:
    def __init__(self) -> None:
        self.x = 22
        self.y = 8

        self.prev_x = 22
        self.prev_y = 8

        self.action = STANDING # STANDING, WALKING, SPRINTING, JUMPING
        self.direction = DOWN # LEFT, RIGHT, UP, DOWN

    def get_viewport_coordinate(self):
        """Returns top-left coordinate of viewport."""
        return (self.x - X_HALF, self.y - Y_HALF)

    def get_delta(self):
        if self.is_standing():
            return 0, 0
        
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

    def update_state(self, action, direction):
        if self.action == action and self.direction == direction:
            return

        if action is not None:
            self.action = action
        
        if direction is not None:
            self.direction = direction

    def update(self, action=None, direction=None, move=False):
        assert action is not None or direction is not None

        self.update_state(action, direction)

        if move:
            self.update_position()

    def next_coordinates(self, direction=None):
        next_x = self.x
        next_y = self.y

        if direction is None:
            direction = self.direction

        if direction == LEFT:
            next_x -= 1
        elif direction == RIGHT:
            next_x += 1
        elif direction == UP:
            next_y -= 1
        else:
            next_y += 1

        return next_x, next_y

    def is_at_edge(self, location):
        return self.x == 0 or self.y == 0 or self.x == location.width-1 or self.y == location.height-1

    def turns(self, new_direction):
        return self.direction != new_direction

    def is_moving_horizontally(self):
        return self.direction == LEFT or self.direction == RIGHT

    def is_moving_up(self):
        return self.direction == UP and self.is_moving()
    
    def is_moving_down(self):
        return self.direction == DOWN and self.is_moving()

    def is_moving(self):
        return not self.is_standing()

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