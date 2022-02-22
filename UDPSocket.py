import socket
import asyncio
from typing import Tuple

from ImageEditor import ImageEditor
from MapRequester import MapRequester
from tools.SpriteTileGenerator import tiles_to_png


class GBServer:
    def __init__(self, host="127.0.0.1", port=23568):
        self.host = host
        self.port = port
        self.mapRequester = MapRequester('private/bing_api_key')

        #client location
        self.x = 0
        self.y = 0
        self.zoom = 1

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))
            while True:
                data, addr = s.recvfrom(512)
                if not data:
                    continue
                r = self.callback(data)
                s.sendto(r, addr)

    def callback(self, data) -> bytes:
        try:
            h = int.from_bytes(data[0:4], byteorder="little", signed=True)
            v = int.from_bytes(data[4:8], byteorder="little", signed=True)
            zoom = data[8]
            self.zoom = zoom + 1
            if h < 0: # left
                print("Left")
                self.x -= (240 / self.zoom)
            elif h > 0: # right
                print("Right")
                self.x += (240 / self.zoom)
            if v < 0: # Down
                print("Up")
                self.y -= (240 / self.zoom)
            elif v > 0:  # Up
                print("Up")
                self.y += (240 / self.zoom)
            return asyncio.run(self.request_gb_bytes())
        except Exception as e:
            return b"\x02" + bytes(e.__class__.__name__)

    async def request_gb_bytes(self):
        png = await self.mapRequester.request_image_by_center(self.x, self.y, 3)
        img = ImageEditor.lower_resolution_to(png, 40, 36)
        tiles = ImageEditor.img_to_tiles(img)
        tiles = ImageEditor.add_padding_to_tiles(tiles)
        tiles_to_png(tiles, 32)
        return bytes([tile.to_byte() for tile in tiles])

