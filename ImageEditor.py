from PIL import Image
import io
from typing import List

from models import RawPngResponse, Tile

class ImageEditor:
    @staticmethod
    def lower_resolution_to(png : RawPngResponse, x : int, y : int) -> Image.Image:
        img = Image.open(io.BytesIO(png.raw_data))
        small_img = img.resize((x,y),resample=Image.BILINEAR)
        result = small_img.convert('LA').resize(img.size, Image.NEAREST)
        result.save("tmp2.png")
        return small_img

    @staticmethod
    def img_to_tiles(img : Image.Image) -> List[Tile]:
        tiles = []
        for y in range(0, img.height, 2):
            for x in range(0, img.width, 2):
                tiles.append(Tile(
                    Tile.get_tile_id_for_color(img.getpixel((x  , y))),
                    Tile.get_tile_id_for_color(img.getpixel((x+1, y))),
                    Tile.get_tile_id_for_color(img.getpixel((x  , y+1))),
                    Tile.get_tile_id_for_color(img.getpixel((x+1, y+1)))
                ))
        print(f"img_to_tiles return tiles array of {len(tiles)} elements")
        return tiles

    @staticmethod
    def add_padding_to_tiles(tiles : List[Tile], pad_from, pad_to) -> List[Tile]:
        result = []
        blank_tile = [Tile(0, 0, 0, 0)] * (pad_to - pad_from)
        for i in range(len(tiles) // pad_from):
            result.extend(tiles[i*pad_from:(i+1)*pad_from])
            result.extend(blank_tile)
        print(f"Added padding: tiles array now {len(result)} elements")
        return result
