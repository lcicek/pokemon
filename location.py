from graphic import Graphic
import pytmx

class Location:
    def __init__(self, image_file, tiled_map_file) -> None:
        self.graphic = Graphic(image_file)

        tiled_map = pytmx.TiledMap(tiled_map_file) # temporary map

        self.width = tiled_map.width # in tiles
        self.height = tiled_map.height # in tiles