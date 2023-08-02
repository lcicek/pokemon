from pynput.keyboard import Listener
from time import perf_counter_ns

class Controller:
    def __init__(self, key_press_event) -> None:
        self.key_press_event = key_press_event
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        
        self.pressed_keys = set()
        self.press_start_time = None 

        self.delta_x = 0
        self.delta_y = 1

        self.start()

    def start(self):
        self.listener.start()

    def on_press(self, key):
        """
            Sets key_press_event.
            Updates direction (via delta_x, delta_y).
            Saves start time of press.
        """
        press_start_time = perf_counter_ns()
        key = key.char
        delta = delta_of_valid_key(key)

        if delta is None: # invalid key
            return

        self.pressed_keys.add(key) # track if additional valid keys are being pressed

        if self.key_press_event.is_set(): # ...but don't do anything with additional pressed keys here (we handle them in on_release)
            return

        # else: first and only key press
        self.press_start_time = press_start_time
        self.update_delta(delta)
        self.key_press_event.set() # set event flag to true

    def on_release(self, key):
        """
            Clears key_press_event if all keys are released.
            If all but one key are released, updates direction accordingly.
        """
        key = key.char
        if key not in self.pressed_keys:
            return
        
        self.pressed_keys.remove(key)

        if len(self.pressed_keys) == 0: # event is over
            self.key_press_event.clear()
        elif len(self.pressed_keys) == 1: # if multiple keys were pressed: make sure that for the last pressed key left, the corresponding delta is used
            delta = delta_of_valid_key(key)
            self.update_delta(delta)

    def update_delta(self, delta):
        assert delta is not None

        self.delta_x = delta[0]
        self.delta_y = delta[1]

    def quit(self):
        self.listener.stop()

# not part of class
def delta_of_valid_key(key):
        if key == 'w': # up
            return (0, -1)
        elif key == 's': # down
            return (0, 1)
        elif key == 'a': # left
            return (-1, 0)
        elif key == 'd': # right
            return (1, 0)
        else:
            return None