import socket

msgFromClient = "Hello UDP Server"

bytesToSend = str.encode(msgFromClient)

serverAddressPort = ("127.0.0.1", 23568)

bufferSize = 1024

# Create a UDP socket at client side

with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
    s.connect(serverAddressPort)
    s.sendall(bytesToSend)
    data = s.recv(1024)
    print(f"Received {data!r}")