class View:
    def __init__(self, x, y, unit) -> None:
        self.x = x
        self.y = y
        self.unit = unit
        self.center_x = x // 2
        self.center_y = y // 2

        self.inPixels()

    def inPixels(self):
        self.width = self.x * self.unit
        self.height = self.y * self.unit
        self.center_width = self.center_x * self.unit
        self.center_height = self.center_y * self.unit

    def setUnit(self, new_unit):
        self.unit = new_unit

        self.inPixels()