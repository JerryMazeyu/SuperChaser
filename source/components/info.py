import pygame
from .. import constants as C
from . import coin
from .. import tools
pygame.font.init()

class Info:
    def __init__(self, info=None):
        if info is None:
            info = {'score': 0, 'coins': 0, 'round': 0, 'mode': 'train', 'difficulty':'simple'}
        self.info = info
        self.create_info_labels()
        self.create_info_contents(info)
        self.flash_coin = coin.FlashingCoin()

    def create_info_contents(self, info):
        self.state_labels = []
        self.state_labels.append((tools.get_text_image(str(info['score']), 20, (255, 255, 0)), (80, 75)))
        self.state_labels.append((tools.get_text_image(str(info['coins']), 20, (255, 255, 0)), (265, 75)))
        self.state_labels.append((tools.get_text_image(str(info['round']), 20, (255, 255, 0)), (490, 75)))
        self.state_labels.append((tools.get_text_image(str(info['mode']), 20, (255, 255, 0)), (705, 75)))
        self.state_labels.append((tools.get_text_image(str(info['difficulty']), 20, (255, 255, 0)), (990, 75)))

    def create_info_labels(self):
        self.info_labels = []
        self.info_labels.append((self.create_label('Score'), (50, 35)))
        self.info_labels.append((self.create_label('Round'), (450, 35)))
        self.info_labels.append((self.create_label('Mode'), (700, 35)))
        self.info_labels.append((self.create_label('difficulty'), (950, 35)))

    def create_label(self, label, size=20, width_scale=1.25, height_scale=1):
        font = pygame.font.Font(C.FONT, size)
        label_image = font.render(label, False, (255,255,255))
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(label_image, (int(rect.width*width_scale), int(rect.height*height_scale)))
        return label_image

    def get_info(self):
        return self.info

    def update(self):
        self.flash_coin.update()
        self.create_info_contents(self.info)

    def draw(self, surface):
        for label in self.info_labels:
            surface.blit(label[0], label[1])
        for label in self.state_labels:
            surface.blit(label[0], label[1])
        surface.blit(self.flash_coin.image, self.flash_coin.rect)
