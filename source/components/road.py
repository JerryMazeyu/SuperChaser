import pygame
import random
from .. import tools, setup

class Road(pygame.sprite.Sprite):
    def __init__(self, position, shape, dark=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'road'
        self.symbol = 0
        self.dark = dark
        self.shape = shape
        self.bright_frames = []
        self.frame_index = 1
        self.sheet = setup.GRAPHICS['level_1']
        self.frames = [tools.get_image_with_shape(self.sheet,0,0,10,10,(0,0,0),self.shape),
                       tools.get_image_with_shape(self.sheet,3416,0,10,10,(255,255,255),self.shape)]
        self.update()
        self.rect = self.image.get_rect()
        self.rect.center = position

    def darken(self):
        self.dark = True

    def lighten(self):
        self.dark = False

    def update(self):
        if self.dark:
            self.image = self.frames[1]
        else:
            self.image = self.frames[0]