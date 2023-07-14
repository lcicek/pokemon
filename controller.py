from pynput.keyboard import Listener
from utility import direction

class Controller:
    def __init__(self, key_press_event) -> None:
        self.key_press_event = key_press_event
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        self.delta_x = None
        self.delta_y = None

    def on_press(self, key):
        delta = direction(key.char)

        if delta is not None:
            self.delta_x = delta[0]
            self.delta_y = delta[1]
            self.key_press_event.set() # set event flag to true

    def quit(self):
        self.listener.stop()