import pygame


class PlayerNameLabel(pygame.sprite.Sprite):
    def __init__(self, name, x_pos=0, y_pos=0):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = None
        self.font = pygame.font.SysFont("Arial", 24)
        self.set_text(name)

    def set_text(self, text):
        self.text = text
        text = self.font.render(text, 1, (0, 0, 0))
        self.image = pygame.Surface((120, 50))
        self.image.fill(pygame.color.THECOLORS['white'])
        self.image.blit(text, [0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = self.y_pos


# TODO: Make a generic abstract button
class PassButton(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width = 120, height = 40):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 24)
        self.text = self.font.render('PASS', 1, (0, 0, 0))
        self.x = x_pos
        self.y = y_pos
        self.border = 2
        self.highlighted = False
        self.width = width
        self.height = height
        self.render()


    def highlight(self, highlight):
        if self.highlighted != highlight:
            self.highlighted = highlight
            self.render()


    def render(self):
        self.image = pygame.Surface((self.width, self.height))
        if self.highlighted:
            self.image.fill(pygame.color.THECOLORS['yellow'])
        else:
            self.image.fill(pygame.color.THECOLORS['black'])

        pygame.draw.rect(self.image, pygame.color.THECOLORS['white'],
                         (self.border, self.border, self.width - 2 * self.border, self.height - 2 * self.border))
        self.image.blit(self.text, [0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
