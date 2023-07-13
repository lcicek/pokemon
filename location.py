from pygame import image

class Location:
    def __init__(self, file, name) -> None:
        self.file = file
        self.name = name
        self.surface = self.generateSurface(file)

    def generateSurface(self, file):
        return image.load(file)