import sys
from PIL import Image

if __name__ == '__main__':
    sys.path.append('..')

from models import Tile

def tiles_to_png(tiles, max_y):
    img = Image.new('RGB', ((len(tiles) // max_y) * 8, max_y * 8))
    for i, tile in enumerate(tiles):
        x = i // max_y
        y = i % max_y
        sub_img = tile.to_jpg()
        img.paste(sub_img, (x*8, y*8) )
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