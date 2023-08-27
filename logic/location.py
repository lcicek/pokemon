## Note: Location logic and graphics are still intertwined and maybe should be decoupled. ###

import xml.etree.ElementTree as ET
import csv

from graphics.graphic import Graphic
from logic.interactor import Interactor
from constant.paths import MAP_CSV_PATH, MAP_XML_PATH
from constant.locationCodebook import *
from constant.parameters import CHARACTERS_PER_LINE, UNIT_SIZE

class Location:
    def __init__(self, graphic, foreground_graphic) -> None:
        self.map = []
        self.init_map()
        self.init_objects()
        
        self.graphic = Graphic(graphic)
        self.foreground_graphic = Graphic(foreground_graphic)

        self.width = self.graphic.width // UNIT_SIZE # width in tiles
        self.height = self.graphic.height // UNIT_SIZE # height in tiles

    def square_is_grass(self, row, col):
        return self.map[row][col] == GRASS

    def square_is_solid(self, row, col, direction):
        return self.map[row][col] == SOLID or self.square_is_blocking_ledge(row, col, direction) or isinstance(self.map[row][col], Interactor)

    def square_is_ledge(self, row, col):
        return self.map[row][col] == LEDGE_DOWN or self.map[row][col] == LEDGE_LEFT or self.map[row][col] == LEDGE_RIGHT

    def square_is_blocking_ledge(self, row, col, direction):
        wrong_direction = self.map[row][col] != direction
        return self.square_is_ledge(row, col) and wrong_direction

    def square_is_jumping_ledge(self, row, col, direction):
        same_direction = self.map[row][col] == direction
        return self.square_is_ledge(row, col) and same_direction

    def init_objects(self):
        tree = ET.parse(MAP_XML_PATH)
        root = tree.getroot()

        for tag in root:
            for interactor in tag:
                x = int(interactor.attrib['x'])
                y = int(interactor.attrib['y'])
                text = self.format_text(interactor.text)
                self.map[y][x] = Interactor(text)

    def init_map(self):
        with open(MAP_CSV_PATH) as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                row = self.init_row(row)
                self.map.append(row)

    def init_row(self, row):
        for i, elem in enumerate(row):
            if elem in dictionary:
                row[i] = dictionary[elem]
        
        return row

    # could probably be optimized:
    def format_text(self, text_string):
        if len(text_string) <= CHARACTERS_PER_LINE:
            return [text_string]
        
        text = []
        text_string = text_string.split(' ')

        for i, word in enumerate(text_string):
            if i != len(text_string)-1:
                text_string[i] = word + ' ' # add space to all characters but the last

        line_length = 0
        current_string = ""
        for word in text_string:
            if line_length + len(word) <= CHARACTERS_PER_LINE:
                line_length += len(word)
                current_string += word
            else:
                assert len(word) <= CHARACTERS_PER_LINE

                text.append(current_string)
                line_length = len(word)
                current_string = word
        
        if len(current_string) > 0:
            text.append(current_string)

        return text