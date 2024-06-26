import pickle
import socket
from typing import Any

from settings import Settings


class Network:
    def __init__(self, settings: Settings) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = settings.server_host
        self.port = settings.server_port
        self.addr = (self.server, self.port)
        self.player_num = self.connect()

    def get_player_number(self) -> int:
        return self.player_num

    def connect(self) -> int:
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(f"Failed to connect to server {self.addr}: {e}")
            exit(1)

    def send(self, data) -> Any:
        try:
            self.client.send(pickle.dumps(data))
            data = self.client.recv(2048)
            data = pickle.loads(data)
            return data
        except socket.error as e:
            print(e)
