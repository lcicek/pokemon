import keyboard
from ordered_set import OrderedSet

from constant.parameters import (
    LEFT, RIGHT, UP, DOWN, A, B, START
)

class Controller:
    def __init__(self) -> None:
        self.movement_keys = OrderedSet()        
        self.active_movement_key = None

        self.action_keys = {A: False, B: False, START: False}
        self.was_pressed = {A: False, B: False, START: False}

        self.b_toggled = False

    # listen(): Listens for input and returns corresponding action.
    def listen(self, outside_is_locked):
        self.collect_input(outside_is_locked)
        
        if len(self.movement_keys) == 0:
            self.active_movement_key = None
        else:
            self.active_movement_key = self.movement_keys[0]

    def movement_input(self):
        if len(self.movement_keys) == 0:
            return None
        else:
            return self.movement_keys[0]

    def collect_input(self, outside_is_unlocked):
        for key in [UP, DOWN, LEFT, RIGHT]:
            if keyboard.is_pressed(key):
                self.movement_keys.add(key)
            else:
                self.remove_movement_key(key)

        for key in self.action_keys:
            self.collect_action_input(key, outside_is_unlocked)

    def collect_action_input(self, key, outside_is_unlocked):
        pressed = keyboard.is_pressed(key)
        press_is_valid = not self.was_pressed[key] and pressed
        
        if press_is_valid and key == B and outside_is_unlocked:
            self.b_toggled = not self.b_toggled

        self.action_keys[key] = press_is_valid # single press
        self.was_pressed[key] = pressed

    def remove_movement_key(self, key):
        if key in self.movement_keys:
            self.movement_keys.remove(key)

    def has_movement_input(self):
        return self.active_movement_key is not None
        