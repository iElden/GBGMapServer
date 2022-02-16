import socket
import asyncio
from typing import Tuple

from MapRequester import mapRequester

class GBServerProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        print(f"Recieved packet : {data} from {addr}")
        response = mapRequester.from_gb_input(data)
        self.socket.sendto(response, addr)