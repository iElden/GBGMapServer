import socket
import asyncio
import struct
import traceback
from typing import Tuple, Dict

from ImageEditor import ImageEditor
from MapRequester import MapRequester
from tools.SpriteTileGenerator import tiles_to_png, old_tiles_to_png

from dataclasses import dataclass

ADDR = str

@dataclass
class ClientCoords:
    x : float
    y : float
    zoom : int

class GBServer:
    def __init__(self, host="127.0.0.1", port=23568):
        self.host = host
        self.port = port
        self.mapRequester = MapRequester('private/bing_api_key')

        #client location
        self.client : Dict[ADDR, ClientCoords]= {}
        self.x = 0
        self.y = 0
        self.zoom = 1

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.host, self.port))
            while True:
                data, addr = s.recvfrom(512)
                print(addr)
                if not data:
                    continue
                r = self.callback(data, addr)
                s.sendto(r, addr)

    def callback(self, data, addr) -> bytes:
        try:
            coords = self.client.get(addr[0], ClientCoords(0, 0, 0))
            print(data)
            op, h, v, zoom = struct.unpack("<BffB", data)
            if op == 1:
                coords.zoom = zoom + 1
                print(op, h, v, zoom)
                if h < 0: # left
                    coords.x -= (240 / 2**coords.zoom)
                elif h > 0: # right
                    coords.x += (240 / 2**coords.zoom)
                if v < 0: # Down
                    coords.y -= (240 / 2**coords.zoom)
                elif v > 0:  # Up
                    coords.y += (240 / 2**coords.zoom)
                if coords.x > 180:
                    coords.x = -360 + coords.x
                if coords.x < -180:
                    coords.x = 360 + coords.x
                if coords.y > 90:
                    coords.y = -180 + coords.y
                if coords.y < -90:
                    coords.y = 180 + coords.y
                return asyncio.run(self.request_gb_bytes(coords))
            if op == 2:
                x, y = self.mapRequester.get_coords_for_query(data[1:])
                if not x and not y:
                    return b"\x02Location not found\x00"
                coords.x = x
                coords.y = y
                return asyncio.run(self.request_gb_bytes(coords))
            else:
                return b"\x02Unknown Opcode\x00"
        except Exception as e:
            return b"\x02" + bytes(e.__class__.__name__, encoding="ASCII") + b"\x00"
        finally:
            self.client[addr[0]] = coords

    async def request_gb_bytes(self, coords):
        png = await self.mapRequester.request_image_by_center(coords.x, coords.y, coords.zoom)
        img = ImageEditor.lower_resolution_to(png, 40, 36)
        tiles = ImageEditor.img_to_tiles(img)
        tiles = ImageEditor.add_padding_to_tiles(tiles, 20, 32)
        tiles_to_png(tiles, 32)
        old_tiles_to_png(tiles, 32)
        return b'\x01' + bytes([tile.to_byte() for tile in tiles])

