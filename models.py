from typing import Tuple

class RawPngResponse:
    def __init__(self, raw_data):
        self.raw_data : bytes = raw_data
        with open("tmp.png", 'wb') as fd:
            fd.write(raw_data)