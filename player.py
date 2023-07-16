from graphic import Graphic
from parameters import PLAYER_SPRITE

class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.graphic = Graphic(PLAYER_SPRITE)

    def updatePos(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y