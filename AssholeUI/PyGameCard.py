#!/usr/bin/env python
"""
Make a card which is a PyGame Sprite
TODO: move dynamic stuff elsewhere?
"""
import pygame
from asshole.cards.PlayingCard import PlayingCard
from pygame.sprite import Sprite


def load_court_card_image(card, width, height, border):
    # Set the img property (if needed)
    if card.suit_str() == "♣":
        card_suit = 'clubs'
    elif card.suit_str() == "♠":
        card_suit = 'spades'
    elif card.suit_str() == "♦":
        card_suit = 'diamonds'
    elif card.suit_str() == "♥":
        card_suit = 'hearts'
    else:
        assert False

    card_name = None
    if card.get_value() == 8:
        card_name = 'jack'
    elif card.get_value() == 9:
        card_name = 'queen'
    elif card.get_value() == 10:
        card_name = 'king'
    elif card.get_value() == 13:
        # Note: The file names are backwards
        card_suit = 'joker'
        if card.isRed():
            card_name = 'red'
        else:
            card_name = 'black'
    assert card_name
    img = pygame.image.load(f'img/{card_name}_{card_suit}.jpg')
    img = pygame.transform.scale(img, (width - 2 * border, height - 2 * border))
    return img


def generate_pip_card_image(card, font_pips, font_edge, width, height, border):
    def suit_color():
        return pygame.color.THECOLORS['red'] if card.isRed() else pygame.color.THECOLORS['black']

    def render_corner_values():
        # render_top_pip('A', suit)
        text = font_edge.render(card.rank_str(), 1, suit_color())
        img.blit(text, (1, 1))
        text = font_edge.render(f'{card.suit_str()}', 1, suit_color())
        img.blit(text, (1, 11))

    def render_pips(spot_col, spot_row):
        text = font_pips.render(f'{card.suit_str()}', 1, suit_color())
        # TODO scale the pos properly
        pip_width = width - 10
        # Need to account for the font size
        x_pos = 5 + pip_width // 6 * (2 * spot_col + 1)

        y_pos = (height // 8) * (spot_row + 1)

        text_rect = text.get_rect(center=(x_pos, y_pos))
        img.blit(text, text_rect)

    img = pygame.Surface((width - 2 * border, height - 2 * border))
    img.fill(pygame.color.THECOLORS['white'])

    # First, render the upside down stuff, then rotate it and draw the upside up
    render_corner_values()

    # Pip placement
    # x x x | row 0 are all the same
    #   x   \ row 1 is offset depending on the column
    # x   x /
    # x x x | row 3 is always the same
    # x   x \ row 4 is offset depending on the column
    #   x   /
    # x x x | row 5 is always the same
    if card.get_value() == 0:
        render_pips(1, 0)
    if card.get_value() == 12:
        render_pips(1, 1)
    if card.get_value() in range(1, 8):
        render_pips(0, 0)
        render_pips(2, 0)
    if card.get_value() in [5, 7]:
        render_pips(1, 1)
    if card.get_value() in [6, 7]:
        render_pips(0, 2)
        render_pips(2, 2)

    img = pygame.transform.rotate(img, 180)

    render_corner_values()

    # Same as above, but add the middle row pips, and add extra pip for 7 (value = 4)
    if card.get_value() == 11:
        render_pips(2, 3)
    if card.get_value() == 0:
        render_pips(1, 0)
    if card.get_value() == 12:
        render_pips(1, 1)
    if card.get_value() in range(1, 8):
        render_pips(0, 0)
        render_pips(2, 0)
    if card.get_value() in [4, 5, 7]:
        render_pips(1, 1)
    if card.get_value() in [6, 7]:
        render_pips(0, 2)
        render_pips(2, 2)
    if card.get_value() in [0, 2, 6]:
        render_pips(1, 3)
    if card.get_value() in [3, 4, 5]:
        render_pips(0, 3)
        render_pips(2, 3)
    return img


class PyGameCard(Sprite):
    def __init__(self, index, width=80, height=None, border=2):
        Sprite.__init__(self)
        self.card = PlayingCard(index)

        self.width = width
        if height:
            self.height = height
        else:
            self.height = self.width * 1.5
        self.border = border
        self.size = self.width, self.height

        # Create an image of the card, and fill it with pips and shit
        # This could also be an image loaded from the disk.
        # image is the whole card, including the border.
        # The image will contain img which is the card value, or maybe the back of the card
        # Before rendering, self.image must be set to front_face o back_face
        self.image = pygame.Surface(self.size)

        self.face_up = True
        self.highlighted = False
        self.angle = 0
        self.angle_delta = 0

        self.back_face = pygame.transform.scale(pygame.image.load('img/red_back.jpg'),
                                                (self.width - 2 * self.border, self.height - 2 * self.border))

        self.font_edge = pygame.font.SysFont('arial', self.width // 4, True)
        self.font_pips = pygame.font.SysFont('arial', self.width // 2, True)
        self.font_ace = pygame.font.SysFont('arial', self.width, True)
        # Make the img for this card
        if self.card.get_value() in [8, 9, 10, 13]:
            self.front_face = load_court_card_image(self.card, self.width, self.height, self.border)
        elif self.card.get_value() == 11:
            self.front_face = generate_pip_card_image(self.card, self.font_ace, self.font_edge, self.width,
                                                      self.height, self.border)
        else:
            self.front_face = generate_pip_card_image(self.card, self.font_pips, self.font_edge, self.width,
                                                      self.height, self.border)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()


    def set_card_params(self, highlighted=None, faceup=None, newAngle=None):
        changed = False
        if highlighted is not None and self.highlighted != highlighted:
            self.highlighted = highlighted
            changed = True

        if faceup is not None and self.face_up != faceup:
            self.face_up = faceup
            changed = True

        if newAngle is not None and self.angle != newAngle:
            self.angle_delta = newAngle - self.angle
            self.angle = newAngle
            changed = True

        if changed:
            self.render()

    def render(self):
        # Render the dynamic stuff (Card is face up or down, highlighted or not, rotation)
        if self.highlighted:
            pygame.draw.rect(self.image, pygame.color.THECOLORS['yellow'], (0, 0, self.width, self.height))
        else:
            pygame.draw.rect(self.image, pygame.color.THECOLORS['black'], (0, 0, self.width, self.height))

        pygame.draw.rect(self.image, pygame.color.THECOLORS['white'],
                         (self.border, self.border, self.width - 2 * self.border, self.height - 2 * self.border))

        if self.face_up:
            self.image.blit(self.front_face, (self.border, self.border))
        else:
            self.image.blit(self.back_face, (self.border, self.border))

        # TODO rotate an image while keeping its center
        if self.angle_delta != 0:
            self.image = pygame.transform.rotate(self.image, self.angle_delta)
            self.angle_delta = 0
