import socket
import asyncio

from typing import Tuple

class GBServerProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def connection_made(self, transport: asyncio.transports.BaseTransport) -> None:
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        print(f"Recieved packet : {data} from {addr}")
        self.socket.sendto(b"\x02Hello\x00", addr)