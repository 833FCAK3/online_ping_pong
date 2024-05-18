import pickle
import socket
from typing import List

from multiplayer.paddle import Paddle
from multiplayer.settings import Settings


class Network:
    def __init__(self, settings: Settings):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = settings.server_host
        self.port = settings.server_port
        self.addr = (self.server, self.port)
        self.paddle = self.connect()

    def getPaddle(self) -> List[Paddle]:
        return self.paddle

    def connect(self) -> List[Paddle]:
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            exit(1)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
