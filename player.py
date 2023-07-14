from parameters import CENTER_WIDTH, CENTER_HEIGHT, DEFAULT_SCALE
from sprite import Sprite

class Player(Sprite):
    def __init__(self, file, name) -> None:
        super().__init__(file, name)

        self.x = CENTER_WIDTH * DEFAULT_SCALE # position is always center square relativ to window
        self.y = CENTER_HEIGHT * DEFAULT_SCALE

    def updateX(self, x):
        self.x = x

    def updateY(self, y):
        self.y = y

