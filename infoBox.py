from constant.paths import GAME_MENU_PATH, ARROW_RIGHT_PATH, ARROW_DOWN_PATH, DIALOGUE_BOX_PATH, DIALOGUE_FONT
from constant.parameters import X, Y, UNIT_SIZE, UP, DOWN, FONT_COLOR, DEFAULT_SCALE
import pygame
from graphic import Graphic
from PIL import Image, ImageDraw, ImageFont

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

        # DRAW TEXT:
        self.size = (self.box_graphic.width, self.box_graphic.height)
        self.scaled_size = (self.box_graphic.width * DEFAULT_SCALE, self.box_graphic.height * DEFAULT_SCALE)
        
        self.font = ImageFont.truetype(font=DIALOGUE_FONT, size=9) # original font size is 9px
        self.empty_image = Image.new(mode='RGBA', size=self.size, color=(0, 0, 0, 0)) # transparent color
        self.text_image = None

        self.padding = UNIT_SIZE * 0.65 # here: values in pixels (to draw text on images):
        self.second_line_y_offset = self.padding + UNIT_SIZE

        self.text = None
        self.num_lines = None
        self.current_line = None
        self.end = None     

    def clear_text(self):
        self.text_image = self.empty_image.copy()

    def draw_text(self):
        self.clear_text()
        draw = ImageDraw.Draw(im=self.text_image)

        x1, y1, x2, y2 = self.get_text_positions()
        draw.text(xy=(x1, y1), text=self.text[self.current_line-1], font=self.font, fill=FONT_COLOR)

        if self.second_line_exists():
            draw.text(xy=(x2, y2), text=self.text[self.current_line], font=self.font, fill=FONT_COLOR)

    def next(self):
        if self.current_line + 1 < self.num_lines:
            self.current_line += 2
        elif self.current_line < self.num_lines:
            self.current_line += 1

        self.draw_text()

        if self.current_line + 1 >= self.num_lines:
            self.end = True

    def open(self, text):
        assert len(text) > 0

        super().open()

        self.text = text
        self.num_lines = len(text)
        self.current_line = 1
        self.end = self.current_line == self.num_lines

        self.draw_text()

    def get_text_positions(self): # in px
        return self.padding, self.padding, self.padding, self.second_line_y_offset

    def second_line_exists(self):
        return self.current_line < self.num_lines

    def get_text_graphic(self):
        pygame_surface = pygame.image.fromstring(self.text_image.tobytes(), self.size, self.text_image.mode).convert_alpha()
        pygame_surface = pygame.transform.scale(pygame_surface, self.scaled_size)
        
        return pygame_surface

    def end_reached(self):
        return self.end
    
    def get_arrow_position(self):
        return self.arrow_x_offset, self.arrow_y_offset

    def get_arrow_graphic(self):
        return self.arrow_graphic.scaled_image

    def rescale(self, scale):
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