import pygame

class PlayerNameLabel(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
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



# TODO: Make a generic abstract button
class PassButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Arial", 24)
        text = self.font.render('PASS', 1, (0, 0, 0))
        self.image = pygame.Surface((120, 50))
        self.image.fill(pygame.color.THECOLORS['white'])
        self.image.blit(text, [0, 0])
        self.rect = self.image.get_rect()
