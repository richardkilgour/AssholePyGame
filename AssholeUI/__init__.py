#!/usr/bin/env python
"""
Run an Asshole game with PyGame

This module has the main game loop, but he game logic is delegated to the PyGameMaster
Config is read from config.yaml
THIS guy should hold all the game objects
"""
import sys
import yaml
import pygame
from asshole.player.AbstractPlayer import AbstractPlayer
from pygame.locals import *
# TODO: load dynamically using importlib
from AssholeUI.GuiElements import PlayerNameLabel, PassButton
from AssholeUI.PyGameCard import PyGameCard
from AssholeUI.PyGameMaster import PyGameMaster
from AssholeUI.PyGamePlayer import PyGamePlayer

from asshole.player.HumanPlayer import HumanPlayer
from asshole.player.PlayerSimple import PlayerSimple
from asshole.player.PlayerHolder import PlayerHolder
from asshole.player.PlayerSplitter import PlayerSplitter


# TODO: read a configuration file
config = yaml.safe_load(open("./config.yaml"))

size = width, height = config['screen']['width'], config['screen']['height']

pygame.init()
screen = pygame.display.set_mode(size)
# Read config file
# Make some actors
actors = []

turn_count = 0
segment_count = 0

all_sprites_list = pygame.sprite.Group()
ui_sprites_list = pygame.sprite.Group()

TEST_CARD_LAYOUT = False
if TEST_CARD_LAYOUT:
    for i in range(0, 54):
        # pos = (width * random(), height * random())
        row_length = 12
        col_height = 5
        pos = ((width / row_length) * (i % row_length), (height / col_height) * (i // row_length))
        new_card = PyGameCard(i % 4, i // 4, pos)
        new_card.rect.x = pos[0]
        new_card.rect.y = pos[1]
        all_sprites_list.add(new_card)

# PyGame will ceed control to the GM
gm = PyGameMaster(width, height)

players = [config['player1'], config['player2'], config['player3'], config['player4'], ]

for p in players:
    player_class = getattr(sys.modules[__name__], p['type'])
    gm.make_player(player_class, p['name'])
    ui_sprites_list.add(PlayerNameLabel(p['name']))
    if p['type'] == 'PyGamePlayer':
        human_player = gm.players[-1]

# Yuck - explicitly place them
ui_sprites_list.sprites()[0].rect.x = width - 60
ui_sprites_list.sprites()[0].rect.y = height // 3
ui_sprites_list.sprites()[1].rect.x = width // 2
ui_sprites_list.sprites()[1].rect.y = height - 60
ui_sprites_list.sprites()[2].rect.x = 0
ui_sprites_list.sprites()[2].rect.y = height // 3
ui_sprites_list.sprites()[3].rect.x = width // 2
ui_sprites_list.sprites()[3].rect.y = 0

clock = pygame.time.Clock()
running = True

pass_button = PassButton()
ui_sprites_list.add(pass_button)
pass_button.rect.x = width // 2
pass_button.rect.y = height // 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # we press a button
        if event.type == KEYDOWN:
            gm.keypress(event.key)
        # where is the mouse
        for s in ui_sprites_list:
            if s == pass_button and s.rect.collidepoint(
                    pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                human_player.send_card_click('PASS')

        for s in all_sprites_list:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                gm.notify_mouseover(s, True)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gm.notify_click(s.card)
            else:
                gm.notify_mouseover(s, False)

    # increment the current game state, and render sprites
    all_sprites_list = gm.update_game_state()
    # Add pass and quit buttons
    for position, player in enumerate(gm.episode.positions):
        # Find the nametag
        for tag in ui_sprites_list.sprites():
            if tag.text[-len(player.name):] == player.name:
                break
        # Update the name tags
        tag.set_text(f'{AbstractPlayer.ranking_names[position]} {player.name}')

    # Update the display
    screen.fill(pygame.color.THECOLORS['white'])
    all_sprites_list.draw(screen)
    ui_sprites_list.draw(screen)
    pygame.display.flip()
    # print(f'x', end='')
    pygame.time.wait(60)