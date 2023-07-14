from pygame import image, transform
from parameters import DEFAULT_SCALE, CENTER_WIDTH, CENTER_HEIGHT

class Sprite:
    def __init__(self, file, name) -> None:
        self.file = file
        self.name = name
        self.src_img = image.load(file)
        self.width = self.src_img.get_width()
        self.height = self.src_img.get_height()

        self.updateScale(DEFAULT_SCALE) # sets self.scale and self.scaled_img

    def updateScale(self, scale):
        self.scale = scale
        self.scaled_img = transform.scale(self.src_img, (self.width * scale, self.height * scale))