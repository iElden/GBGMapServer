import aiohttp
from typing import Tuple

from ImageEditor import ImageEditor
from tools.SpriteTileGenerator import tiles_to_png
from models import RawPngResponse

class MapRequester:
    BASE_URL = 'https://dev.virtualearth.net/'
    IMAGE_BY_CENTER_BASE = BASE_URL + "REST/v1/Imagery/Map/Aerial"
    LOCATION_LIST = BASE_URL + "REST/v1/Locations"
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

    async def get_coords_for_query(self, query : bytes) -> Tuple[float, float]:
        async with aiohttp.request('GET',
                                   f"{self.LOCATION_LIST}/{query.decode('ASCII')}",
                                   params={'key': self._api_key}) as resp:
            js = await resp.json()
            try:
                res = js['resourceSets']['resources']
                if not res:
                    return (0, 0)
                return res[0]['point']['coordinates']
            except Exception as e:
                return (0, 0)