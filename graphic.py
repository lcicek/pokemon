from pygame import image, transform
from constant.parameters import (
    DEFAULT_SCALE, UNIT_SIZE
)

class Graphic:
    def __init__(self, file) -> None:
        self.file = file
        self.scaled_image = None # initialized by calling update_scale() in line 13
        self.init() # sets self.scaled_image

    def init(self):
        img = image.load(self.file)

        self.width = img.get_width() // UNIT_SIZE
        self.height = img.get_height() // UNIT_SIZE

        self.rescale(DEFAULT_SCALE)

    def rescale(self, scale):
        img = image.load(self.file)

        scaled_width = img.get_width() * scale
        scaled_height = img.get_height() * scale
        
        self.scaled_image = transform.scale(img, (scaled_width, scaled_height))
        