from pygame import image, transform
from parameters import DEFAULT_SCALE

class Graphic:
    def __init__(self, file, x, y) -> None:
        self.file = file
        self.src_img = image.load(file)
        self.width = self.src_img.get_width()
        self.height = self.src_img.get_height()
        self.updateScale(DEFAULT_SCALE) # sets self.scale and self.scaled_img
        self.x = x
        self.y = y

    def updateScale(self, scale):
        self.scale = scale
        self.scaled_width = self.width * scale
        self.scaled_height = self.height * scale
        self.scaled_img = transform.scale(self.src_img, (self.scaled_width, self.scaled_height))

    def updatePos(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y