import sys

import pygame

from game_stats import GameStats
from menu import BaseButton
from multiplayer.run import multiplayer
from singleplayer.run import single_player
from two_players.run import two_players


pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0)


clock = pygame.time.Clock()
single_player_button = BaseButton(screen, "Single Player", -100)
two_players_button = BaseButton(screen, "Two Players")
multiplayer_button = BaseButton(screen, "Multiplayer", 100)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_q:
                    sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # check mouse click

    single_player_button.render()
    two_players_button.render()
    multiplayer_button.render()

    pygame.display.flip()

    clock.tick(30)
