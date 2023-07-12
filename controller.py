from pynput.keyboard import Listener
from movement import move

class Controller:
    def __init__(self, event) -> None:
        self.event = event
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        self.delta_x = None
        self.delta_y = None

    def on_press(self, key):
        key = key.char
        if key in "wasd":
            self.delta_x, self.delta_y = move(key)
            self.event.set() # set event flag to true

    def quit(self):
        self.listener.stop()