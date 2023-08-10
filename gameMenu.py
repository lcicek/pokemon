from constant.paths import GAME_MENU_PATH, ARROW_PATH
from constant.parameters import X, Y, UNIT_SIZE, UP, DOWN
from graphic import Graphic

class GameMenu:
    def __init__(self) -> None:
        self.open = False
        self.layer = None

        self.x_offset = X - 5.5
        self.y_offset = 0.5

        self.entries = 5

        self.list_offset = 1 # in relation to regular unit
        self.list_distance = 1.5
        
        self.arrow = Graphic(ARROW_PATH)
        self.arrow_pointer = 0

        self.display_box = { # each layer has its own display
            0: Graphic(GAME_MENU_PATH)
        }

        self.position = {
            0: (self.x_offset, self.y_offset)
        } 

    def select(self, outside_lock):
        if self.arrow_at_exit():
            self.close_menu(outside_lock)
        else:
            print("Menu action isn't implemented yet.")

    def arrow_at_exit(self):
        return self.arrow_pointer == self.entries - 1

    def move_arrow(self, direction):
        if direction is UP and self.arrow_pointer > 0:
            self.arrow_pointer -= 1
        elif direction is DOWN and self.arrow_pointer < self.entries-1:
            self.arrow_pointer += 1

    def get_arrow_graphic(self):
        return self.arrow.scaled_image

    def get_arrow_position(self):
        return (self.x_offset + 0.4, self.y_offset + self.list_offset + self.arrow_pointer*self.list_distance)

    def get_menu_graphic(self):
        return self.display_box[self.layer].scaled_image

    def get_menu_position(self):
        return self.position[self.layer]

    def enter_layer(self):
        self.layer += 1
        
    def exit_layer(self):
        self.layer -= 1

    def open_menu(self, outside_lock):
        assert outside_lock.is_unlocked()

        self.open = True
        self.layer = 0
        outside_lock.lock()

    def close_menu(self, outside_lock):
        assert self.can_be_closed() and outside_lock.is_locked()

        self.open = False
        self.layer = None
        outside_lock.unlock()

    def can_be_closed(self):
        return self.layer == 0

    def is_open(self):
        return self.open
    
    def is_closed(self):
        return not self.open
    
    def rescale(self, scale):
        for key in self.display_box:
            self.display_box[key].rescale(scale)