import keyboard
from ordered_set import OrderedSet

from constant.parameters import (
    LEFT, RIGHT, UP, DOWN, A, B
)

class Controller:
    def __init__(self) -> None:
        self.movement_keys = OrderedSet()
        
        self.active_movement_key = None

        self.a_was_pressed = False
        self.b_was_pressed = False

        self.a = False
        self.b = False

    # listen(): Listens for input and returns corresponding action.
    def listen(self):
        self.collect_input()
        
        if len(self.movement_keys) == 0:
            self.active_movement_key = None
        else:
            self.active_movement_key = self.movement_keys[0]

    def movement_input(self):
        if len(self.movement_keys) == 0:
            return None
        else:
            return self.movement_keys[0]

    def collect_input(self):
        for key in [UP, DOWN, LEFT, RIGHT]:
            if keyboard.is_pressed(key):
                self.movement_keys.add(key)
            else:
                self.remove_movement_key(key)

        self.collect_input_A()
        self.collect_input_B()        

    def collect_input_A(self):
        a_pressed = keyboard.is_pressed(A)
        press_is_valid = not self.a_was_pressed and a_pressed
        
        self.a = press_is_valid
        self.a_was_pressed = a_pressed

    def collect_input_B(self):
        b_pressed = keyboard.is_pressed(B)
        press_is_valid = not self.b_was_pressed and b_pressed
        
        if press_is_valid:
            self.b = not self.b

        self.b_was_pressed = b_pressed

    def remove_movement_key(self, key):
        if key in self.movement_keys:
            self.movement_keys.remove(key)
        