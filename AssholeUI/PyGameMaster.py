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
from AssholeUI import PyGameCard, PyGamePlayer, PlayerNameLabel


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
        self.player_status_labels = []

    def make_player(self, player_type, name=None):
        super().make_player(player_type, name)
        self.player_status_labels.append(PlayerNameLabel(name))

    def set_label_pos(self, label, index):
        # TODO: Really should not do this every time
        if index == 0:
            label.rect.x = self.width // 2
            label.rect.y = 2 * self.height // 3 - 120
        elif index == 1:
            label.rect.x = self.width // 3 - 40
            label.rect.y = self.height // 3
        elif index == 2:
            label.rect.x = self.width // 2
            label.rect.y = 120
        elif index == 3:
            label.rect.x = 2 * self.width // 3 + 40
            label.rect.y = self.height // 3

    def play(self, number_of_rounds=100, preset_hands=None):
        # check for any action, and display the current play field
        if not self.episode:
            # Create a new episode
            self.episode = Episode(self.players, self.positions, self.deck, self.listener_list)

        self.positions = self.episode.play()
        if self.episode.state == State.INITIALISED:
            # Do an episode - We need 4 players and a deck of cards.
            pass
        elif self.episode.state == State.DEALING:
            for c in self.cards:
                c.set_card_params(faceup=False)
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
            # Set highlight state of all cards to False
            for c in self.cards:
                c.set_card_params(highlighted=False)
            self.episode = None

        # Find the human current_player (if any)
        human_player_index = 0
        for i, player in enumerate(self.players):
            if player_is_human(player):
                human_player_index = i
                break

        visible_cards = pygame.sprite.Group()
        visible_others = pygame.sprite.Group()

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

            # Render played cards or labels
            if player_meld is None:
                # TODO: Put a label saying "Passed"
                self.player_status_labels[i].set_text(f'{player.name} PASSED')
                self.set_label_pos(self.player_status_labels[i], i)
                visible_others.add(self.player_status_labels[i])
            elif player_meld == '␆':
                # TODO: Put a label saying "Waiting"
                self.player_status_labels[i].set_text(f'{player.name} WAITING')
                self.set_label_pos(self.player_status_labels[i], i)
                visible_others.add(self.player_status_labels[i])
            else:
                # draw the played cards
                for j, card in enumerate(player_meld.cards):
                    pycard = self.cards.sprites()[card.get_index()]
                    visible_cards.add(pycard)
                    pycard.set_card_params(faceup=True)
                    if i == 0:
                        pos = (self.width // 2 + 40 * j, 2 * self.height // 3 - 120)
                    elif i == 1:
                        pos = (self.width // 3 - 40, self.height // 3 + j * self.height // 12)
                    elif i == 2:
                        pos = (self.width // 2 + 40 * j, 120)
                    elif i == 3:
                        pos = (2 * self.width // 3 + 40, self.height // 3 + j * self.height // 12)
                    pycard.set_card_params(newAngle=i * 90)
                    pycard.rect.x = pos[0]
                    pycard.rect.y = pos[1]

            # Render unplaced cards
            mid_card_index = len(player._hand) / 2.
            for j, card in enumerate(player._hand):
                # index to the pycard
                # It will draw itself, but needs some parameters
                pycard = self.cards.sprites()[card.get_index()]
                pycard.set_card_params(faceup=i == 0)
                visible_cards.add(pycard)
                # TODO: more elegant pos and angle to make a nice arc
                if i == 0:
                    pos = (120 + 40 * j, 2 * self.height // 3)
                elif i == 1:
                    pos = (40, j * self.height // 24)
                elif i == 2:
                    pos = (self.width // 3 + j * self.width // 45, 10)
                elif i == 3:
                    pos = (self.width - 40, j * self.height // 24)
                pycard.set_card_params(newAngle= i * 90 - (j - mid_card_index) * 10)
                pycard.rect.x = pos[0]
                pycard.rect.y = pos[1]

        return visible_cards, visible_others


    def keypress(self, key):
        pass

    def notify_click(self, pycard):
        """Forward a clicked card to the human player (if any) to decide which to play"""
        for p in self.players:
            if player_is_human(p):
                # Let the player decide which to take if multiple clicks
                p.send_card_click(pycard)

    def notify_mouseover(self, pycard, param):
        for p in self.players:
            if player_is_human(p) and pycard.card.get_index() in p.get_hand_indices():
                pycard.set_card_params(highlighted=param)
