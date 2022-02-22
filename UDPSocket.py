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
        self.zoom = 3

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected to {addr}")
                while True:
                    data = conn.recv(512)
                    if not data:
                        continue
                    r = self.callback(data)
                    conn.sendall(r)

    def callback(self, data) -> bytes:
        return asyncio.run(self.request_gb_bytes())

    async def request_gb_bytes(self):
        png = await self.mapRequester.request_image_by_center(self.x, self.y, 3)
        img = ImageEditor.lower_resolution_to(png, 40, 36)
        tiles = ImageEditor.img_to_tiles(img)
        tiles = ImageEditor.remove_bouteille(tiles)
        tiles = ImageEditor.add_padding_to_tiles(tiles)
        tiles_to_png(tiles, 32)
        return bytes([tile.to_byte() for tile in tiles])

