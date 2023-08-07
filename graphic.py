from pygame import image, transform
from parameters import (
    DEFAULT_SCALE
)

class Graphic:
    def __init__(self, file) -> None:
        self.file = file
        self.image = image.load(file)
        self.scaled_image = None # initialized by calling update_scale() in line 13
        self.rescale(DEFAULT_SCALE) # sets self.scaled_image

    def rescale(self, scale):
        scaled_width = self.image.get_width() * scale
        scaled_height = self.image.get_height() * scale
        
        self.scaled_image = transform.scale(self.image, (scaled_width, scaled_height))