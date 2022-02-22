import aiohttp

from ImageEditor import ImageEditor
from tools.SpriteTileGenerator import tiles_to_png
from models import RawPngResponse

class MapRequester:
    BASE_URL = 'https://dev.virtualearth.net/'
    IMAGE_BY_CENTER_BASE = BASE_URL + "REST/v1/Imagery/Map/Aerial"
    IMG_SIZE = 500

    tmp_global = b"blabla"

    def __init__(self, api_key_path):
        with open(api_key_path, 'r') as fd:
            self._api_key = fd.read().strip()

    async def request_image_by_center(self, x : float, y : float, zoomLevel : int) -> RawPngResponse:
        async with aiohttp.request('GET',
                                   f"{self.IMAGE_BY_CENTER_BASE}/{y},{x}/{zoomLevel}",
                                   params={'mapSize': f"{self.IMG_SIZE},{self.IMG_SIZE}", 'key':self._api_key}) as resp:
            print(f"{self.IMAGE_BY_CENTER_BASE}/{y},{x}/{zoomLevel}")
            return RawPngResponse(await resp.read())
