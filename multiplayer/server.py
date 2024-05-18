import pickle
import signal
import socket
import sys
import threading

import pygame

from multiplayer.paddle import Paddle
from multiplayer.settings import Settings


pygame.init()

settings = Settings()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((settings.server_host, settings.server_port))
except socket.error as e:
    print(e)
    sys.exit(1)

s.listen(2)
s.settimeout(1)  # Set a timeout for the accept call
print("Server Started, Waiting for a connection")

paddles = [Paddle(settings, 1), Paddle(settings, 2)]


def threaded_client(conn: socket.socket, player):
    try:
        conn.send(pickle.dumps(paddles))
    except Exception as e:
        print(f"Failed to send initial data to player {player}: {e}")
        conn.close()
        return

    print(f"Client {player} connected and initial data sent")

    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print(f"No data received from player {player}")
                break

            data = pickle.loads(data)
            paddles[player] = data
            print(f"Player {player} sent data: {data}")

            if player == 1:
                reply = paddles[0]
            else:
                reply = paddles[1]

            print(f"Sending to player {player}: {reply}")
            conn.sendall(pickle.dumps(reply))
        except (pickle.UnpicklingError, EOFError, socket.error) as e:
            print(f"Error receiving/sending data for player {player}: {e}")
            break

    print(f"Lost connection to player {player}")
    conn.close()


def signal_handler(sig, frame):
    print("Interrupt received, shutting down...")
    s.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

currentPlayer = 0
while True:
    try:
        conn, addr = s.accept()
        print("Connected to:", addr)

        thread = threading.Thread(target=threaded_client, args=(conn, currentPlayer))
        thread.daemon = True  # Ensure thread exits when main thread exits
        thread.start()

        if currentPlayer < 1:
            currentPlayer += 1
        else:
            currentPlayer = 0
    except socket.timeout:
        continue
    except Exception as e:
        print(f"Error accepting connections: {e}")
        break
