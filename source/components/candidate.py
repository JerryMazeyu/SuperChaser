import pygame
from .. import tools, setup

class Candidate(pygame.sprite.Sprite):
    def __init__(self, position, shape):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.bright_frame_rects = [(0, 16, 15, 15), (16, 16, 15, 15)]
        self.dark_frame_rects = [(0, 48, 15, 15), (16, 48, 15, 15)]
        self.timer = 0
        self.shape = shape
        img = pygame.Surface(shape)
        img.fill((255, 0, 0))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = position







