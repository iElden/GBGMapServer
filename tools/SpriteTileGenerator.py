import sys
from PIL import Image

if __name__ == '__main__':
    sys.path.append('..')

from models import Tile

def tiles_to_png(tiles, max_x):
    # img = Image.new('RGB', ((len(tiles) // max_y) * 8, max_y * 8))
    img = Image.new('RGB', (max_x * 8, (len(tiles) // max_x) * 8))
    for i, tile in enumerate(tiles):
        b = tile.to_byte()
        x = i % max_x
        y = i // max_x
        with Image.open("tools/tilemap.png") as tilemap:
            for x2 in range(8):
                for y2 in range(8):
                    img.putpixel((x*8+x2, y*8+y2), tilemap.getpixel(((b % 16) * 8 + x2, (b // 16) * 8 + y2)))
    img.save('tiles_to_png.png')

def main():
    tiles = []
    for i in range(256):
        a = (i & 0xc0) >> 6
        b = (i & 0x30) >> 4
        c = (i & 0x0c) >> 2
        d = (i & 0x03)
        tile = Tile(a, b, c, d)
        tiles.append(tile)
        # jpegs.append(tile.to_jpg())
    tiles_to_png(tiles, 16)

if __name__ == '__main__':
    main()
