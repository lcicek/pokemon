from pygame import transform
from parameters import DEFAULT_SCALE, CENTER_WIDTH, CENTER_HEIGHT, SCREEN_POS

class Renderer:
    def __init__(self, location):
        self.location = location
        self.scale = DEFAULT_SCALE
        self.center_x = CENTER_WIDTH * DEFAULT_SCALE
        self.center_y = CENTER_HEIGHT * DEFAULT_SCALE

    def scaleImage(self, image):
        width = image.get_width() * self.scale
        height = image.get_height() * self.scale

        return transform.scale(image, (width, height))

    def renderLocation(self, screen, image, pos):
        image = self.scaleImage(image)
        screen.blit(image, pos)

    def renderPlayer(self, screen, image):
        image = self.scaleImage(image)
        screen.blit(image, (self.center_x, self.center_y))

    def updateScale(self, scale):
        self.scale = scale
        self.center_x = CENTER_WIDTH * scale
        self.center_y = CENTER_HEIGHT * scale