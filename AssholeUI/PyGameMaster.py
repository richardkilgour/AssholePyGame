#!/usr/bin/env python
"""
Contains the Asshole game logic

Wrapper around a generic Asshole GameMaster to make it asynchronous
Has a primitive state machine that can change with a call to update_game_state, in the main game loop
"""
from random import shuffle

# Only for making the list of Sprites
import pygame
from asshole.Episode import Episode, State
from asshole.GameMaster import GameMaster
from asshole.cards.PlayingCard import PlayingCard

from AssholeUI import PyGameCard, PyGamePlayer

# Remember the current state
from enum import Enum


def player_is_human(player):
    return isinstance(player, PyGamePlayer.PyGamePlayer)


class PyGameMaster(GameMaster):
    def __init__(self, width, height):
        super().__init__()

        # Sprites should be persistent, so init them here
        self.cards = pygame.sprite.Group()
        for i in range(0, self.deck_size):
            self.cards.add(PyGameCard(i))

        # Do it after players added
        self.player_labels = []
        self.episode = None
        self.current_player = None
        self.active_players = None
        self.positions = []
        self.width = width
        self.height = height

    def make_player(self, player_type, name=None):
        super().make_player(player_type, name)

    # Stolen from Episode
    def set_player_finished(self, player):
        """
        Someone just played out, so assign them a position,
        Technically they are still 'in' and their meld counts
        If the hands makes it back round, they will pass (and gloat)
        """
        player.set_position(len(self.positions))
        self.notify_listeners("notify_played_out", player, len(self.positions))
        self.positions.append(player)

    def play(self):
        # check for any action, and display the current playfield
        if not self.episode:
            # Create a new episode
            self.episode = Episode(self.players, self.positions, self.deck, self.listener_list)

        # Do this, but do not block = 1 tick
        self.positions = self.episode.play()
        if self.episode.state == State.INITIALISED:
            # Do an episode - We need 4 players and a deck of cards.
            pass
        elif self.episode.state == State.DEALING:
            pass
        elif self.episode.state == State.SWAPPING:
            pass
        elif self.episode.state == State.ROUND_STARTING:
            pass
        elif self.episode.state == State.PLAYING:
            # Play until the round is won (only one player remaining)
            pass
        elif self.episode.state == State.HAND_WON:
            pass
        elif self.episode.state == State.FINISHED:
            self.episode = None

        # Find the human current_player (if any)
        human_player_index = 0
        for i, player in enumerate(self.players):
            if player_is_human(player):
                human_player_index = i
                break

        # i 0 is human (or computer), then clockwise
        for i in range(0, 4):
            # Current player is offset by the 'human' index
            # TODO: move human to first place? (locally)
            player = self.players[(human_player_index + i) % 4]

            # Render played cards
            if player.last_played and player.last_played != '␆':
                # draw the played cards
                for j, card in enumerate(player.last_played.cards):
                    pycard = self.cards[card.get_index()]
                    if i == 0:
                        pos = (self.width // 2 + 40 * j, 2 * self.height // 3 - 120)
                    elif i == 1:
                        pos = (90, self.height // 3 + j * self.height // 12)
                        pycard.setCardParams(newAngle=90, faceup=True)
                    elif i == 2:
                        pos = (self.width // 2 + 40 * j, 120)
                        pycard.setCardParams(newAngle=180, faceup=True)
                    elif i == 3:
                        pos = (2 * self.width // 3 + 40, self.height // 3 + j * self.height // 12)
                        pycard.setCardParams(newAngle=270, faceup=True)
                    pycard.rect.x = pos[0]
                    pycard.rect.y = pos[1]

            # Render unplaced cards
            for j, card in enumerate(player._hand):
                # index to the pycard
                # It will draw itself, but needs some parameters
                pycard = self.cards.sprites()[card.get_index()]
                if i == 0:
                    pos = (120 + 40 * j, 2 * self.height // 3)
                elif i == 1:
                    pos = (40, j * self.height // 24)
                    pycard.setCardParams(newAngle=90, faceup=(i == 0))
                elif i == 2:
                    pos = (self.width // 3 + j * self.width // 45, 10)
                    pycard.setCardParams(newAngle=180, faceup=(i == 0))
                elif i == 3:
                    pos = (self.width - 40, j * self.height // 24)
                    pycard.setCardParams(newAngle=270, faceup=(i == 0))
                pycard.rect.x = pos[0]
                pycard.rect.y = pos[1]

            # TODO: Render discarded cards
        return self.cards

    def keypress(self, key):
        pass

    def notify_click(self, card):
        # If it's a current_player's card, queue it up for playing
        if card in self.player_labels:
            return
        for p in self.players:
            if player_is_human(p):
                # Let the player decide which to take if multiple clicks
                p.send_card_click(card)

    def notify_mouseover(self, card, param):
        card.setCardParams(highlighted=param)
