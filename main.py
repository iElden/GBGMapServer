import asyncio

from MapRequester import MapRequester
from ImageEditor import ImageEditor
from UDPSocket import GBServerProtocol
from tools.SpriteTileGenerator import tiles_to_png

async def main():
    mm = MapRequester('private/bing_api_key')
    png = await mm.request_image_by_center(0, 0, 3)
    img = ImageEditor.lower_resolution_to(png, 40, 36)
    tiles = ImageEditor.img_to_tiles(img)
    tiles_to_png(tiles, 18)


if __name__ == '__main__':
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    exit()
    sock = loop.create_datagram_endpoint(GBServerProtocol, local_addr=('0.0.0.0', 23568))
    loop.run_until_complete(sock)
    loop.run_forever()
