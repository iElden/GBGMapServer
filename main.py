import asyncio

from MapRequester import MapRequester, mapRequester
from ImageEditor import ImageEditor
from UDPSocket import GBServerProtocol
from tools.SpriteTileGenerator import tiles_to_png

async def test_request_packet():
    png = await mapRequester.request_image_by_center(0, 0, 3)
    img = ImageEditor.lower_resolution_to(png, 40, 36)
    tiles = ImageEditor.img_to_tiles(img)
    tiles = ImageEditor.remove_bouteille(tiles)
    tiles = ImageEditor.add_padding_to_tiles(tiles)
    tiles_to_png(tiles, 32)
    return bytes([tile.to_byte() for tile in tiles])


if __name__ == '__main__':
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    MapRequester.tmp_global = loop.run_until_complete(test_request_packet())
    print(f"Server will respond : {MapRequester.tmp_global}")
    sock = loop.create_datagram_endpoint(GBServerProtocol, local_addr=('0.0.0.0', 23568))
    loop.run_until_complete(sock)
    loop.run_forever()
