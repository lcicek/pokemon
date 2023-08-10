from constant.paths import GAME_MENU_PATH, ARROW_RIGHT_PATH, ARROW_DOWN_PATH, DIALOGUE_BOX_PATH, TEXT_FONT
from constant.parameters import X, Y, UNIT_SIZE, UP, DOWN, FONT_COLOR
from pygame import font
from graphic import Graphic
from PIL import ImageDraw

class InfoBox:
    def __init__(self, graphic_path, x_offset, y_offset, inner_offset) -> None:
        self.box_graphic = Graphic(graphic_path)
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.inner_offset = inner_offset
        self.active = False

    def get_graphic(self):
        return self.box_graphic.scaled_image

    def get_position(self):
        return self.x_offset, self.y_offset

    def open(self):
        self.active = True

    def close(self):
        self.active = False

    def is_active(self):
        return self.active
    
    def is_inactive(self):
        return not self.active
    
    def rescale(self, scale):
        self.box_graphic.rescale(scale)

class DialogueBox(InfoBox):
    def __init__(self) -> None:
        super().__init__(DIALOGUE_BOX_PATH, 1, Y-4, 1)

        self.font = font.Font(TEXT_FONT, 20)

        self.arrow_graphic = Graphic(ARROW_DOWN_PATH)
        self.arrow_x_offset = X - 2
        self.arrow_y_offset = Y - 1.5

        self.text = None
        self.num_lines = None
        self.current_line = None
        self.end = None

    def next(self):
        if self.current_line + 1 < self.num_lines:
            self.current_line += 2
        elif self.current_line < self.num_lines:
            self.current_line += 1
        
        if self.current_line + 1 >= self.num_lines:
            self.end = True

    def open(self, text):
        assert len(text) > 0

        super().open()

        self.text = text
        self.num_lines = len(text)
        self.current_line = 1
        self.end = self.current_line == self.num_lines

    def get_text_positions(self):
        first_x_offset = self.x_offset + self.inner_offset
        first_y_offset = self.y_offset + self.inner_offset

        second_x_offset = first_x_offset
        second_y_offset = first_y_offset + self.inner_offset

        return first_x_offset, first_y_offset, second_x_offset, second_y_offset

    def get_text_graphics(self):
        first_line = self.font.render(self.text[self.current_line-1], False, FONT_COLOR)

        if self.current_line == self.num_lines:
            second_line = None
        else:
            second_line = self.font.render(self.text[self.current_line], False, FONT_COLOR) 

        return first_line, second_line

    def end_reached(self):
        return self.end
    
    def get_arrow_position(self):
        return self.arrow_x_offset, self.arrow_y_offset

    def get_arrow_graphic(self):
        return self.arrow_graphic.scaled_image

class GameMenu(InfoBox):
    def __init__(self) -> None:
        super().__init__(GAME_MENU_PATH, X-5.5, 0.5, 1)

        self.entries = 5
        self.vertical_spacing = 1.5
        
        self.arrow_graphic = Graphic(ARROW_RIGHT_PATH)
        self.arrow_pointer = 0
        self.arrow_x_offset = self.x_offset + 0.4
        self.arrow_y_offset = self.y_offset + self.inner_offset

    def arrow_at_exit(self):
        return self.arrow_pointer == self.entries - 1

    def move_arrow(self, direction):
        if direction is UP and self.arrow_pointer > 0:
            self.arrow_pointer -= 1
        elif direction is DOWN and self.arrow_pointer < self.entries-1:
            self.arrow_pointer += 1

    def get_arrow_graphic(self):
        return self.arrow_graphic.scaled_image

    def get_arrow_position(self):
        return (self.arrow_x_offset, self.arrow_y_offset + self.arrow_pointer*self.vertical_spacing)
    
    def rescale(self, scale):
        self.box_graphic.rescale(scale)
        self.arrow_graphic.rescale(scale)