"""
实现Game的基类，并实现加载图像的函数操作
"""

import pygame
import os
from resources.maze import maze_get
from source import constants as C

class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()  # 主屏幕
        self.clock = pygame.time.Clock()  # 时钟
        self.keys = pygame.key.get_pressed()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
        self.state_name = start_state

    def update(self):
        if self.state.finished:
            next_state = self.state.next
            self.state_name = next_state
            self.state.finished = False
            self.state = self.state_dict[next_state]
        self.state.update(self.screen, self.keys) # 执行state中的update方法

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.state_name == 'game':
                        self.state.stop_thread()
                    pygame.display.quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()
            pygame.display.update()
            self.clock.tick(60)  # 控制帧率

def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics

def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
    return image

def get_image_with_shape(sheet, x, y, width, height, colorkey, shape):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, shape)
    return image

def get_text_image(text, size, color=(255,255,255)):
    font = pygame.font.Font(C.FONT, size)
    label_image = font.render(text, False, color)
    return label_image

def get_single_image(sheet, width, height):
    image = pygame.transform.scale(sheet, (width, height))
    return image

def exec_method_in_group(group, method, *args):
    for sprite in group.sprites():
        getattr(sprite, method)(*args)

def get_blind_maze():
    return maze_get.get_maze_with_loop(verbose=False)

