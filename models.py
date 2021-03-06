from typing import Tuple
from PIL import Image
from statistics import mean

COLOR_ID_TO_PIXEL_COLOR = [0xFF, 0xAA, 0x55, 0x00]

# type
COLOR_ID = int
COLOR_TUPLE = Tuple[int, int, int]

class RawPngResponse:
    def __init__(self, raw_data):
        self.raw_data : bytes = raw_data
        with open("tmp.png", 'wb') as fd:
            fd.write(raw_data)

class Tile:
    def __init__(self, a, b, c, d):
        self.a : COLOR_ID = a
        self.b : COLOR_ID = b
        self.c : COLOR_ID = c
        self.d : COLOR_ID = d

    @staticmethod
    def get_tile_id_for_color(color : COLOR_TUPLE):
        r, g, b = color
        m = mean([r, g, b])
        if m > 175:
            return 0
        if m > 100:
            return 1
        if m > 50:
            return 2
        return 3

    def get_color_id_by_coordinate(self, x, y) -> COLOR_ID:
        low_y = y <= 3
        if x <= 3:
            return self.a if low_y else self.c
        else:
            return self.b if low_y else self.d

    @staticmethod
    def color_id_to_rgb(i) -> COLOR_TUPLE:
        c = COLOR_ID_TO_PIXEL_COLOR[i]
        return c, c, c

    def to_jpg(self) -> Image.Image:
        img = Image.new('RGB', (8, 8))
        for i in range(8*8):
            x = i % 8
            y = i // 8
            img.putpixel((x, y), self.color_id_to_rgb(self.get_color_id_by_coordinate(x, y)))
        return img

    def to_byte(self) -> int:
        return (self.a << 6) | (self.b << 4) | (self.c << 2) | self.d

class MapResponse:
    def __init__(self):
        ...

    def to_gb(self) -> bytes:
        """
        :return: (20*18) tiles; 32*18 with padding
        """
