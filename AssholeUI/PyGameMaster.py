#!/usr/bin/env python
"""
Creates and repeatedly calls an Asshole episode
Holds all the card sprites and player playfields
Processes UI actions
"""
# Only for making the list of Sprites
import pygame
from asshole.Episode import Episode, State
from asshole.GameMaster import GameMaster
from AssholeUI import PyGameCard, PyGamePlayer


def player_is_human(player):
    return isinstance(player, PyGamePlayer.PyGamePlayer)


class PyGameMaster(GameMaster):
    def __init__(self, width, height):
        super().__init__()

        # Sprites should be persistent, so init them here
        self.cards = pygame.sprite.Group()
        for i in range(0, self.deck_size):
            self.cards.add(PyGameCard(i))

        self.episode = None
        self.current_player = None
        self.active_players = None
        self.positions = []
        self.width = width
        self.height = height

    def play(self, number_of_rounds=100, preset_hands=None):
        # check for any action, and display the current play field
        if not self.episode:
            # Create a new episode
            self.episode = Episode(self.players, self.positions, self.deck, self.listener_list)

        # Do this, but do not block = 1 tick
        self.positions = self.episode.play()
        if self.episode.state == State.INITIALISED:
            # Do an episode - We need 4 players and a deck of cards.
            pass
        elif self.episode.state == State.DEALING:
            for c in self.cards:
                c.setCardParams(faceup=False)
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

        # i = 0 is human (or computer), then clockwise
        for i in range(0, 4):
            # Current player is offset by the 'human' index
            # TODO: move human to first place? (locally)
            player_index = (human_player_index + i) % 4
            player = self.players[player_index]

            if self.episode:
                player_meld = self.episode.current_melds[player_index]
            else:
                player_meld = None
            # Render played cards
            if player_meld is None:
                # TODO: Put a label saying "Passed"
                pass
            elif player_meld == '␆':
                # TODO: Put a label saying "Waiting"
                pass
            else:
                # draw the played cards
                for j, card in enumerate(player_meld.cards):
                    pycard = self.cards.sprites()[card.get_index()]
                    pycard.setCardParams(faceup=True)
                    if i == 0:
                        pos = (self.width // 2 + 40 * j, 2 * self.height // 3 - 120)
                    elif i == 1:
                        pos = (90, self.height // 3 + j * self.height // 12)
                        pycard.setCardParams(newAngle=90)
                    elif i == 2:
                        pos = (self.width // 2 + 40 * j, 120)
                        pycard.setCardParams(newAngle=180)
                    elif i == 3:
                        pos = (2 * self.width // 3 + 40, self.height // 3 + j * self.height // 12)
                        pycard.setCardParams(newAngle=270)
                    pycard.rect.x = pos[0]
                    pycard.rect.y = pos[1]

            # Render unplaced cards
            for j, card in enumerate(player._hand):
                # index to the pycard
                # It will draw itself, but needs some parameters
                pycard = self.cards.sprites()[card.get_index()]
                pycard.setCardParams(faceup=i == 0)

                if i == 0:
                    pos = (120 + 40 * j, 2 * self.height // 3)
                elif i == 1:
                    pos = (40, j * self.height // 24)
                    pycard.setCardParams(newAngle=90)
                elif i == 2:
                    pos = (self.width // 3 + j * self.width // 45, 10)
                    pycard.setCardParams(newAngle=180)
                elif i == 3:
                    pos = (self.width - 40, j * self.height // 24)
                    pycard.setCardParams(newAngle=270)
                pycard.rect.x = pos[0]
                pycard.rect.y = pos[1]

            # TODO: Render discarded cards
        return self.cards

    def keypress(self, key):
        pass

    def notify_click(self, card):
        """Forward a clicked card to the human player (if any) to decide which to play"""
        for p in self.players:
            if player_is_human(p):
                # Let the player decide which to take if multiple clicks
                p.send_card_click(card)

    def notify_mouseover(self, pycard, param):
        for p in self.players:
            if player_is_human(p) and pycard.card.get_index() in p.get_hand_indices():
                pycard.setCardParams(highlighted=param)
