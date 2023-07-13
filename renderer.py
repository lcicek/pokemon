from pygame import transform
from parameters import DEFAULT_SCALE, CENTER_WIDTH, CENTER_HEIGHT, SCREEN_POS

class Renderer:
    def __init__(self, location):
        self.location = location
        self.scale = DEFAULT_SCALE

    def scaleImage(self, image):
        width = image.get_width() * self.scale
        height = image.get_height() * self.scale

        return transform.scale(image, (width, height))

    def renderViewport(self, screen, image):
        image = self.scaleImage(image)
        screen.blit(image, SCREEN_POS)

    def renderPlayer(self, screen, image):
        image = self.scaleImage(image)
        screen.blit(image, (CENTER_WIDTH * self.scale, CENTER_HEIGHT * self.scale))

    def updateScale(self, scale):
        self.scale = scale