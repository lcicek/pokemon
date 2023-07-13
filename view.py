from pygame import Rect
from parameters import *

class View:
    def __init__(self, parent):
        self.parent = parent
        self.viewport = Rect(0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
        self.surface = self.parent.subsurface(self.viewport)

    def updateViewport(self, delta_x, delta_y): # change
        self.viewport.move_ip(delta_x * UNIT_SIZE, delta_y * UNIT_SIZE)
        self.surface = self.parent.subsurface(self.viewport) # update surface being looked at
