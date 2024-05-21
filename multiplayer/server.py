import pickle
import signal
import socket
import sys
import threading
from random import choice

import pygame

from multiplayer.settings import Settings


def reset_game_state() -> None:
    global players_ready, ball_directions
    players_ready = [False, False]
    ball_directions = [choice([True, False]), choice([True, False])]


def threaded_client(conn: socket.socket, player_num) -> None:
    try:
        conn.send(pickle.dumps(player_num))
        print(f"Player number sent to player_{player_num}")
    except Exception as e:
        print(f"Failed to send player number to player_{player_num}: {e}")
        conn.close()
        return

    try:
        paddle_x_coord = conn.recv(2048)
        paddle_x_coord = pickle.loads(paddle_x_coord)
        print(f"Received initial x coordinate of player_{player_num}: {paddle_x_coord}")
        paddles[player_num - 1] = paddle_x_coord
        print(f"Coordinates are: {paddles}")
        conn.sendall(pickle.dumps(""))
    except Exception as e:
        print(f"Failed to receive player_{player_num} paddle coordinate: {e}")
        conn.close()
        return

    print(f"Client {player_num} connected, initial data sent and received")

    while True:
        try:
            data = conn.recv(2048)
            if not data:
                print(f"No data received from player_{player_num}")
                break

            data = pickle.loads(data)
            print(f"Player_{player_num} sent data: {data}")

            if data == "rdy":
                players_ready[player_num - 1] = True

            if data == "rdy" or data == "rdy_check":
                reply = players_ready[1 // player_num]  # Send opponent's ready status
            elif data == "game over":
                players_ready[player_num - 1] = False
                if not any(players_ready):
                    reset_game_state()
                reply = "200"
            elif data == "ball_moving_left":
                reply = ball_directions[0]
            elif data == "ball_moving_down":
                reply = ball_directions[1]
            else:
                paddles[player_num - 1] = data
                reply = paddles[1 // player_num]  # Send opponent's coordinates

            print(f"Sending to player_{player_num}: {reply}")
            conn.sendall(pickle.dumps(reply))
        except (pickle.UnpicklingError, EOFError, socket.error) as e:
            print(f"Error receiving/sending data for player_{player_num}: {e}")
            break

    print(f"Lost connection to player_{player_num}")
    reset_game_state()
    conn.close()


def signal_handler(sig, frame) -> None:
    print("Interrupt received, shutting down...")
    s.close()
    sys.exit()


# Run server
pygame.init()
settings = Settings()
paddles = [0, 0]


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("", settings.server_port))
except socket.error as e:
    print(e)
    sys.exit(1)

s.listen(2)
s.settimeout(1)  # Set a timeout for the accept call
print("Server Started, Waiting for a connection")

reset_game_state()

signal.signal(signal.SIGINT, signal_handler)

current_player = 1
while True:
    try:
        conn, addr = s.accept()
        print(f"Connected to player_{current_player}:", addr)

        thread = threading.Thread(target=threaded_client, args=(conn, current_player))
        thread.daemon = True  # Ensure thread exits when main thread exits
        thread.start()

        if current_player < 2:
            current_player += 1
        else:
            current_player = 1
    except socket.timeout:
        continue
    except Exception as e:
        print(f"Error accepting connections: {e}")
        break
