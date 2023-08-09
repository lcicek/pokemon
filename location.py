import xml.etree.ElementTree as ET
import csv

from graphic import Graphic
from interactor import Interactor
from constant.paths import MAP_CSV_PATH, MAP_XML_PATH
from constant.locationCodebook import *

class Location:
    def __init__(self, graphic, foreground_graphic) -> None:
        self.map = []
        self.init_map()
        
        self.graphic = Graphic(graphic)
        self.foreground_graphic = Graphic(foreground_graphic)

        self.width = self.graphic.width # width in tiles
        self.height = self.graphic.height # height in tiles

    def square_is_solid(self, col, row, direction):
        return self.map[col][row] == SOLID or self.square_is_blocking_ledge(col, row, direction)

    def square_is_ledge(self, col, row):
        return self.map[col][row] == LEDGE_DOWN or self.map[col][row] == LEDGE_LEFT or self.map[col][row] == LEDGE_RIGHT

    def square_is_blocking_ledge(self, col, row, direction):
        wrong_direction = self.map[col][row] != direction
        return self.square_is_ledge(col, row) and wrong_direction

    def square_is_jumping_ledge(self, col, row, direction):
        same_direction = self.map[col][row] == direction
        return self.square_is_ledge(col, row) and same_direction

    def init_objects(self):
        tree = ET.parse(MAP_XML_PATH)
        root = tree.getroot()

        for tag in root:
            for interactor in tag:
                x = interactor.attrib['x']
                y = interactor.attrib['y']
                self.map[x][y] = Interactor(interactor.text)

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

"""
    def init_map(self):
        tree = ET.parse(TILED_MAP_PATH)
        root = tree.getroot()
        map = root[1][0].text # change
        map = map.split()
        
        width = int(root.attrib['width'])
        height = int(root.attrib['height'])

        for i, row in enumerate(map):
            row = row.split(',')
            row = row[0:width]
            row = self.init_row(row)

            map[i] = row

        return map
"""