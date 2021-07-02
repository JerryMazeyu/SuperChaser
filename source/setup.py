"""
游戏初始化的操作
"""

import pygame
from . import constants as C
from . import tools

pygame.init()
SCREEN = pygame.display.set_mode(C.SCREEN_SIZE)

GRAPHICS = tools.load_graphics('resources/graphics')