import pygame
from .. import tools, setup

class Boom(pygame.sprite.Sprite):
    def __init__(self, position, shape, dark):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'boom'
        self.symbol = -1
        self.frame_index = 0
        self.bright_frame_rects = [(0, 16, 15, 15), (16, 16, 15, 15)]
        self.dark_frame_rects = [(0, 48, 15, 15), (16, 48, 15, 15)]
        self.timer = 0
        self.dark = dark
        self.shape = shape
        self.load_frames()
        self.update()
        self.rect = self.image.get_rect()
        self.rect.center = position

    def darken(self):
        self.dark = True

    def lighten(self):
        self.dark = False

    def load_frames(self):
        sheet = setup.GRAPHICS['enemies']
        self.frames = {'bright': [], 'dark': []}
        for frame_rect in self.bright_frame_rects:
            self.frames['bright'].append(tools.get_image_with_shape(sheet, *frame_rect, (0, 0, 0), self.shape))
        for frame_rect in self.dark_frame_rects:
            self.frames['dark'].append(tools.get_image_with_shape(sheet, *frame_rect, (255, 255, 255), self.shape))


    def update(self):
        self.current_time = pygame.time.get_ticks()
        frame_durations = [375, 375]

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            self.frame_index %= 2
            self.timer = self.current_time

        self.image = self.frames['dark' if self.dark else 'bright'][self.frame_index]


