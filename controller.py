import keyboard
from ordered_set import OrderedSet

from parameters import (
    LEFT, RIGHT, UP, DOWN
)

class Controller:
    def __init__(self) -> None:
        self.pressed_keys = OrderedSet()  

    # listen(): Listens for input and returns corresponding action.
    def listen(self):
        self.collect_input()
        
        if len(self.pressed_keys) == 0:
            return None
        else:
            return self.pressed_keys[0]

    def collect_input(self):
        for key in [UP, DOWN, LEFT, RIGHT]:
            if keyboard.is_pressed(key):
                self.pressed_keys.add(key)
            else:
                self.remove_key(key)

    def remove_key(self, key):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)
        