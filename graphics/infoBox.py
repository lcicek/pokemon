import pygame

from graphics.graphic import Graphic
from constant.paths import (
    GAME_MENU_PATH, ARROW_RIGHT_PATH, ARROW_DOWN_PATH, DIALOGUE_BOX_PATH, DIALOGUE_FONT
)
from constant.parameters import (
    X, Y,
    UNIT_SIZE, DEFAULT_SCALE,
    UP, DOWN, 
    FONT_COLOR,
    CHARACTERS_PER_FRAME
)

class InfoBox:
    def __init__(self, graphic_path, x_offset, y_offset) -> None:
        self.box_graphic = Graphic(graphic_path)
        self.x_offset = x_offset
        self.y_offset = y_offset
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
        self.active = False
        self.box_graphic = Graphic(DIALOGUE_BOX_PATH)
        self.width = self.box_graphic.width // UNIT_SIZE ## width in unit size
        self.height = self.box_graphic.height // UNIT_SIZE ## height in unit size
        self.x_offset = (X - self.width) / 2 # dialogue box centered horizontally
        self.y_offset = Y - self.height - 0.5 # leave half a unit (8px) space on bottom
        
        self.arrow_graphic = Graphic(ARROW_DOWN_PATH)
        self.arrow_x_offset = self.x_offset + self.width - 1 # leave room of one unit size for arrow (at the right)
        self.arrow_y_offset = self.y_offset + self.height - 1 # leave room of one unit for arrow (at the bottom)

        self.font_size = 9
        self.font = pygame.font.Font(DIALOGUE_FONT, size=self.font_size*DEFAULT_SCALE)

        # DRAW TEXT:
        self.size = (self.box_graphic.width, self.box_graphic.height)
        self.scaled_size = (self.box_graphic.width * DEFAULT_SCALE, self.box_graphic.height * DEFAULT_SCALE)
    
        self.padding = 0.65 # here: values in pixels (to draw text on images):
        self.second_line_y_offset = self.padding + 1 

        self.text = None
        self.num_lines = None
        self.current_line = None
        self.character_count = None
        self.end = None

    def increment_character_count(self):
        self.character_count += CHARACTERS_PER_FRAME

    def get_first_line(self):
        if self.character_count >= len(self.text[self.current_line]):
            return self.text[self.current_line]
        else:
            return self.text[self.current_line][0:self.character_count]
        
    def get_second_line(self):
        if not self.second_line_exists() or self.character_count < len(self.text[self.current_line]):
            return None
        
        index = self.character_count - len(self.text[self.current_line])

        if index >= len(self.text[self.current_line+1]):
            return self.text[self.current_line+1]
        else:
            return self.text[self.current_line+1][0:index]

    def get_current_text_length(self):
        length = len(self.text[self.current_line])

        if self.second_line_exists():
            length += len(self.text[self.current_line+1])

        return length

    def next(self):
        self.character_count = 0

        if self.current_line + 2 < self.num_lines:
            self.current_line += 2
        elif self.current_line + 1 < self.num_lines:
            self.current_line += 1

        if self.current_line + 2 >= self.num_lines:
            self.end = True

    def open(self, text):
        assert len(text) > 0
        super().open()

        self.character_count = CHARACTERS_PER_FRAME - 1 if CHARACTERS_PER_FRAME <= len(text) else len(text) - 1
        self.text = text
        self.num_lines = len(text)
        self.current_line = 0
        self.end = self.current_line+1 >= self.num_lines-1

    def get_text_positions(self): # in px
        return self.padding, self.padding, self.padding, self.second_line_y_offset

    def second_line_exists(self):
        return self.current_line+1 < self.num_lines

    def get_text_graphics(self):
        lines = []
        first_line = self.get_first_line()
        second_line = self.get_second_line()
        self.increment_character_count()

        lines.append(self.font.render(first_line, False, FONT_COLOR))
        
        if second_line is not None:
            lines.append(self.font.render(second_line, False, FONT_COLOR))

        coordinates = []
        x1_off, y1_off, x2_off, y2_off = self.get_text_positions()
        coordinates.append((x1_off, y1_off))
        coordinates.append((x2_off, y2_off)) 
        
        return lines, coordinates

    def end_reached(self):
        return self.end
    
    def get_arrow_position(self):
        return self.arrow_x_offset, self.arrow_y_offset

    def get_arrow_graphic(self):
        return self.arrow_graphic.scaled_image

    def rescale(self, scale):
        self.font = pygame.font.Font(DIALOGUE_FONT, self.font_size * scale)
        self.scaled_size = (self.size[0] * scale, self.size[1] * scale)
        self.box_graphic.rescale(scale)
        self.arrow_graphic.rescale(scale)

class GameMenu(InfoBox):
    def __init__(self) -> None:
        super().__init__(GAME_MENU_PATH, X-5.5, 0.5)

        self.entries = 5
        self.vertical_spacing = 1.5
        
        self.arrow_graphic = Graphic(ARROW_RIGHT_PATH)
        self.arrow_pointer = 0
        self.arrow_x_offset = self.x_offset + 0.4
        self.arrow_y_offset = self.y_offset + 1

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