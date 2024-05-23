# Ping Pong Online

## Description
A ping pong game with 3 game modes:
- singleplayer
- two players on same PC
- online multiplayer for 2

Multiplayer is realized as a client / server system via the python sockets module. The server handles connections (max 2
players), game logic and event processing is mostly client side.

## Run
Launch ping_pong.exe
To run multiplayer you have to run server.py. To connect - first update connection details in the settings.yml file,
then launch the exe file and choose multiplayer. Both players have to connect for the game to start.
