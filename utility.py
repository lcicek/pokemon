from pygame import time

from parameters import (
    VIEWPORT_WIDTH
)

def calculateScale(rescaled_width):
    scale = rescaled_width / VIEWPORT_WIDTH
    return scale