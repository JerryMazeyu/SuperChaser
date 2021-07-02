import pygame
from .. import tools, setup
from .. import constants as C
from source.components.road import Road

class FlashingCoin(pygame.sprite.Sprite):
    def __init__(self, position=(280,45), shape=(20, 31), dark=False):
        pygame.sprite.Sprite.__init__(self)
        self.name = 'coin'
        self.symbol = 2
        self.frame_index = 0
        self.bright_frame_rects = [(3, 98, 11, 14), (19, 98, 11, 14), (35, 98, 11, 14), (51, 98, 11, 14)]
        self.dark_frame_rects = [(146, 98, 11, 14), (162, 98, 11, 14), (178, 98, 11, 14), (194, 98, 11 ,14)]
        self.timer = 0
        self.dark = dark
        self.shape = shape
        self.visible = True
        self.load_frames()
        self.update()
        self.rect = self.image.get_rect()
        self.rect.center = position

    def darken(self):
        self.dark = True

    def lighten(self):
        self.dark = False

    def eaten(self):
        self.visible = False

    def load_frames(self):
        sheet = setup.GRAPHICS['item_objects']
        self.frames = {'bright': [], 'dark': []}
        for frame_rect in self.bright_frame_rects:
            if not self.shape:
                self.frames['bright'].append(tools.get_image(sheet, *frame_rect, (0, 0, 0), C.BG_MULTI))
            else:
                self.frames['bright'].append(tools.get_image_with_shape(sheet, *frame_rect, (0, 0, 0), self.shape))
        for frame_rect in self.dark_frame_rects:
            if not self.shape:
                self.frames['dark'].append(tools.get_image(sheet, *frame_rect, (0, 0, 0), C.BG_MULTI))
            else:
                self.frames['dark'].append(tools.get_image_with_shape(sheet, *frame_rect, (255, 255, 255), self.shape))

    def update(self):
        self.current_time = pygame.time.get_ticks()
        frame_durations = [375, 125, 125, 125]

        if self.timer == 0:
            self.timer = self.current_time
        elif self.current_time - self.timer > frame_durations[self.frame_index]:
            self.frame_index += 1
            self.frame_index %= 4
            self.timer = self.current_time

        self.image = self.frames['dark' if self.dark else 'bright'][self.frame_index]
        if not self.visible:
            self.image = Road(self.rect.center, self.shape, dark=self.dark).image


