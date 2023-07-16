from graphic import Graphic
from parameters import CENTER_WIDTH, CENTER_HEIGHT

class Player(Graphic):
    def __init__(self, file, x, y) -> None:
        super().__init__(file, x, y)

    def recenter(self):
        self.x = CENTER_WIDTH * self.scale
        self.y = CENTER_HEIGHT * self.scale

    def updateScale(self, scale):
        super().updateScale(scale)
        self.recenter()