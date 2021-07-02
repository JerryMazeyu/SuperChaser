"""
入口文件，启动游戏
"""
import pygame
from source import tools
from source.states import main_menu, main_game

def main():
    state_dict = {
        'main_menu': main_menu.MainMenu(),
        'game': main_game.MainGame()
    }
    game = tools.Game(state_dict, 'main_menu')
    game.run()


if __name__ == '__main__':
    main()