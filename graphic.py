from pygame import image, transform
from parameters import DEFAULT_SCALE, UNIT_SIZE

class Graphic:
    def __init__(self, file) -> None:
        self.file = file
        self.src_img = image.load(file)
        self.max_x = self.src_img.get_width() // UNIT_SIZE # width in tiles
        self.max_y = self.src_img.get_height() // UNIT_SIZE # height in tiles
        self.updateScale(DEFAULT_SCALE) # sets self.scale and self.scaled_img

    def updateScale(self, scale):
        self.scale = scale

        scaled_width = self.src_img.get_width() * scale
        scaled_height = self.src_img.get_height() * scale
        
        self.scaled_img = transform.scale(self.src_img, (scaled_width, scaled_height))