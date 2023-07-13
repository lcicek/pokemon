from parameters import VIEWPORT_WIDTH, VIEWPORT_HEIGHT
import math

def calculateScale(rescaled_size):
    rescaled_width = rescaled_size[0]
    rescaled_height = rescaled_size[1]

    if rescaled_width != VIEWPORT_WIDTH: # "if the width has been resized"
        scale = rescaled_width / VIEWPORT_WIDTH
    else: # "if only the height has been resized"
        scale = rescaled_height / VIEWPORT_HEIGHT

    return scale