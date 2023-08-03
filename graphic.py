from pygame import image, transform
from parameters import (
    DEFAULT_SCALE, UNIT_SIZE
)

class Graphic:
    def __init__(self, file) -> None:
        self.file = file
        self.image = image.load(file)
        self.scale = None
        self.scaled_image = None # initialized by calling update_scale() in line 13

        self.max_x = self.image.get_width() // UNIT_SIZE # width in tiles
        self.max_y = self.image.get_height() // UNIT_SIZE # height in tiles
        
        self.update_scale(DEFAULT_SCALE) # sets self.scale and self.scaled_img

    def update_scale(self, scale):
        self.scale = scale

        scaled_width = self.image.get_width() * scale
        scaled_height = self.image.get_height() * scale
        
        self.scaled_image = transform.scale(self.image, (scaled_width, scaled_height))