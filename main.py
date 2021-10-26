import asyncio

from MapRequester import MapRequester
from ImageEditor import ImageEditor

async def main():
    mm = MapRequester('private/bing_api_key')
    png = await mm.request_image_by_center(0, 0, 1)
    ImageEditor.lower_resolution_to(png, 25, 25)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())