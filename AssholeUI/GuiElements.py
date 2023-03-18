import pygame


class PlayerNameLabel(pygame.sprite.Sprite):
    def __init__(self, name, x_pos, y_pos):
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
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 24)
        text = self.font.render('PASS', 1, (0, 0, 0))
        self.image = pygame.Surface((120, 80))
        self.image.fill(pygame.color.THECOLORS['white'])
        self.image.blit(text, [0, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
