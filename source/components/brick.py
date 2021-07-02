import pygame
import random
from .. import tools, setup
from .. import constants as C

class Brick(pygame.sprite.Sprite):
    def __init__(self, position, shape, dark=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'brick'
        self.symbol = 1
        self.dark = dark
        self.shape = shape
        self.frame_index = 1
        self.bright_frame_rects = [(0, 2, 13, 13), (16, 2, 13, 13), (36, 2, 13, 13), (49, 2, 13, 13)]
        self.dark_frame_rects = [(0, 34, 13, 13), (16, 34, 13, 13), (36, 34, 13, 13),  (49, 34, 13, 13)]
        self.load_frames()
        self.update()
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.timer = 0

    def darken(self):
        self.dark = True

    def lighten(self):
        self.dark = False

    def load_frames(self):
        sheet = setup.GRAPHICS['tile_set']
        self.frames = {'bright': [], 'dark': []}
        for frame_rect in self.bright_frame_rects:
            self.frames['bright'].append(tools.get_image_with_shape(sheet, *frame_rect, (0,0,0), self.shape))
        for frame_rect in self.dark_frame_rects:
            self.frames['dark'].append(tools.get_image_with_shape(sheet, *frame_rect, (255,255,255), self.shape))

    def update(self):
        if self.dark:
            self.image = self.frames['dark'][self.frame_index]
        else:
            self.image = self.frames['bright'][self.frame_index]