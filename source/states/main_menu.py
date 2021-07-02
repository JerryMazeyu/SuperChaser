"""
主菜单页面
"""
import pygame
from .. import setup
from .. import tools
from .. import constants as C
from ..components import info, cursor, option
from ..runtime import runtime
import time


class MainMenu:
    def __init__(self):
        self.setup_background()
        self.setup_cursor()
        self.setup_option()
        self.option_check_group = pygame.sprite.Group()
        self.setup_hard_info()
        self.runtime = runtime
        self.runtime.gameinfo = {'score': 100, 'coins': '0*0', 'round': 0, 'mode': 'train', 'difficulty':'simple'}
        self.gameinfo = self.runtime.gameinfo
        self.info = info.Info(self.gameinfo)
        self.setup_cursor()
        self.finished = False
        self.next = 'game'
        self.timer = pygame.time.get_ticks()


    def setup_background(self):
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BG_MULTI),
                                                                   int(self.background_rect.height * C.BG_MULTI)))
        self.viewport = setup.SCREEN.get_rect()

    def setup_hard_info(self):
        self.hard_info_image = {'title': (tools.get_text_image("SUPER CHASER", 70), (300, 250))}

    def setup_option(self):
        self.hard = option.ColorOption("hard", 20, (320, 530))
        self.simple = option.ColorOption("simple", 20, (320, 480))
        self.train_mode = option.ColorOption("train mode", 20, (620, 480))
        self.test_mode = option.ColorOption("test mode", 20, (620, 530))
        self.option_list = [self.hard, self.simple, self.train_mode, self.test_mode]

    def setup_cursor(self):
        self.cursor1 = cursor.MushroomCursor((280, 480))
        self.cursor2 = cursor.MushroomCursor((580, 480))
        self.cursor1.activate()
        self.cursor2.deactive()

    def get_active_cursor(self):
        return self.cursor1 if self.cursor1.is_active else self.cursor2

    def deactivate_(self, cursor):
        cursor.deactive()
        if cursor == self.cursor1:
            if cursor.states == 'up':
                try:
                    self.option_check_group.remove(self.hard)
                    self.hard.uncheck()
                except:
                    pass
                self.option_check_group.add(self.simple)
            if cursor.states == 'down':
                try:
                    self.option_check_group.remove(self.simple)
                    self.simple.uncheck()

                except:
                    pass
                self.option_check_group.add(self.hard)
        if cursor == self.cursor2:
            if cursor.states == 'up':
                try:
                    self.option_check_group.remove(self.test_mode)
                    self.test_mode.uncheck()
                except:
                    pass
                self.option_check_group.add(self.train_mode)
            if cursor.states == 'down':
                try:
                    self.option_check_group.remove(self.train_mode)
                    self.train_mode.uncheck()
                except:
                    pass
                self.option_check_group.add(self.test_mode)


    def update_cursor(self, keys):
        self.cursor = self.get_active_cursor()
        self.cursor.update(keys)
        if self.cursor.states == 'up':
            self.cursor.rect.y = 480
        elif self.cursor.states == 'down':
            self.cursor.rect.y = 530
        if self.cursor == self.cursor1 and keys[pygame.K_RIGHT] or keys[pygame.K_RETURN]:
            self.deactivate_(self.cursor1)
            self.cursor2.activate()
            time.sleep(0.2)
        if self.cursor == self.cursor2 and keys[pygame.K_LEFT]:
            self.deactivate_(self.cursor2)
            self.cursor1.activate()
        if self.cursor == self.cursor2 and (keys[pygame.K_RETURN] or keys[pygame.K_RIGHT]):
            self.deactivate_(self.cursor2)
            time.sleep(0.1)
            self.finished = True

    def update_option(self):
        if not self.cursor1.is_active:
            if self.cursor1.states == 'up':
                self.hard.check()


    def update(self, surface, keys):
        self.update_cursor(keys)
        tools.exec_method_in_group(self.option_check_group, 'check')
        for option in self.option_check_group:
            if option.text in ['simple', 'hard']:
                self.gameinfo['difficulty'] = option.text
            elif option.text in ['train mode', 'test mode']:
                self.gameinfo['mode'] = option.text.split(" ")[0]
        surface.blit(self.background, self.viewport)
        for name, (image, rect) in self.hard_info_image.items():
            surface.blit(image, rect)
        surface.blit(self.cursor1.image, self.cursor1.rect)
        surface.blit(self.cursor2.image, self.cursor2.rect)
        for option in self.option_list:
            surface.blit(option.image, option.rect)
            option.update_image()
        self.info.update()
        self.info.draw(surface)

    def draw(self, surface):
        surface.blit()