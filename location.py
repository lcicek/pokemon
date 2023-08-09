import xml.etree.ElementTree as ET

from square import Square
from graphic import Graphic
from parameters import (
    TILED_MAP_PATH,
    RIGHT, DOWN,
    UNIT_SIZE
)

class Location:
    def __init__(self, graphic, foreground_graphic) -> None:
        self.map = self.init_map()
        
        self.graphic = Graphic(graphic)
        self.foreground_graphic = Graphic(foreground_graphic)

        self.width = self.graphic.width # width in tiles
        self.height = self.graphic.height # height in tiles

    def square_is_solid(self, col, row, direction):
        return self.map[col][row].is_solid() or self.map[col][row].is_blocking_ledge(direction)

    def square_is_jumping_ledge(self, col, row, direction):
        return self.map[col][row].is_jumping_ledge(direction)

    def init_map(self):
        tree = ET.parse(TILED_MAP_PATH)
        root = tree.getroot()
        map = root[1][0].text # change
        map = map.split()
        
        for i, row in enumerate(map):
            row = row.split(',')
            row = self.init_row(row)

            map[i] = row

        return map

    def init_row(self, row):
        for i, elem in enumerate(row):
            solid = True if elem == '2' else False
            ledge = None

            if elem == '3':
                ledge = RIGHT
            elif elem == '4':
                ledge = DOWN

            row[i] = Square(solid, ledge)
        
        return row