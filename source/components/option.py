import pygame
from .. import tools

class ColorOption(pygame.sprite.Sprite):
    def __init__(self, text, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.is_checked = False
        self.text = text
        self.size = size
        self.image = tools.get_text_image(self.text, size, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def check(self):
        self.is_checked = True

    def uncheck(self):
        self.is_checked = False

    def update_image(self):
        if self.is_checked:
            self.image = tools.get_text_image(self.text, self.size, (255, 255, 0))
        else:
            self.image = tools.get_text_image(self.text, self.size, (255, 255, 255))




