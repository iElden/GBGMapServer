from PIL import Image
import io

from models import RawPngResponse

class ImageEditor:

    @staticmethod
    def lower_resolution_to(png : RawPngResponse, x : int, y : int) -> Image.Image:
        img = Image.open(io.BytesIO(png.raw_data))
        small_img = img.resize((x,y),resample=Image.BILINEAR)
        result = small_img.resize(img.size, Image.NEAREST)
        result.save("tmp2.png")
        return small_img

