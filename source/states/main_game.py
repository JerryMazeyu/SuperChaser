"""
游戏界面
"""
import pygame
from source import setup
from .. import tools
from .. import constants as C
from ..components import info, maze
from ..runtime import runtime
import time
from config import option
import socket
import threading
import json
import ctypes
import inspect
import random

class MainGame:
    def __init__(self):
        self.setup_server()
        self.start()

    def start(self):
        self.t = threading.Thread(target=self.socketCom)
        self.t.start()
        self.setup_background()
        self.runtime = runtime
        self.gameinfo = self.runtime.gameinfo
        self.gameinfo['score'] = option.init_score
        if self.gameinfo['mode'] == 'train':
            self.runtime.mazeinfo = tools.get_blind_maze()
        else:
            with open(option.maze_file_path, 'r') as f:
                k = f.readlines()
                k = [eval(x.strip('\n')) for x in k]
            self.runtime.mazeinfo = random.choice(k)
        self.mazeinfo = self.runtime.mazeinfo
        self.gameinfo['coins'] = f"{self.mazeinfo['bonusValue']}*{self.mazeinfo['bonusNum']}"
        self.info = info.Info(self.gameinfo)
        self.finished = False
        self.next = None
        self.timer = pygame.time.get_ticks()
        self.gameinfo['round'] += 1
        self.maze = maze.Maze(self.runtime)
        self.client_info = self.get_client()


    def setup_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('localhost', 6999))
        self.server.setblocking(False)
        self.server.listen(1)

    def setup_background(self):
        self.sheet = setup.GRAPHICS['level_1']
        self.background = tools.get_image(self.sheet, 183, 49, 244, 145, (0,0,0), 1.)
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (1200, 800))

    def get_client(self):
        return self.maze.client_info

    def move(self, type):
        self.maze.move(type)

    def get_game_state(self):
        if self.client_info.score <= 0:
            return -1
        elif self.client_info.player_cord == self.client_info.target_cord:
            return 1
        else:
            return 0

    def update(self, surface, keys):
        surface.blit(self.background, (0,0))
        self.info.update()
        self.info.draw(surface)
        if keys[pygame.K_r]:
            self.start()
            time.sleep(0.1)
        self.maze.update(keys)
        self.maze.draw(surface)
        state = self.get_game_state()
        if state == -1 or state == 1:
            self.start()

    def draw(self, surface):
        surface.blit()

    def socketCom(self):
        client_list = []
        while True:
            try:
                connection, addr = self.server.accept()
                client_list.append((connection, addr))
                print(f"接口已连接至: {str(addr[0]) + ':' + str(addr[1])}")
            except BlockingIOError:
                pass
            for client_socket, client_addr in client_list:
                try:
                    client_recv = client_socket.recv(1024)
                    if client_recv:
                        print("接受指令自{} -> {}".format(client_addr, client_recv.decode('utf-8')))
                        if client_recv.decode('utf-8') == 'get':
                            self.maze.update(None)
                        elif client_recv.decode('utf-8') in ['up', 'down', 'left', 'right']:
                            self.move(client_recv.decode('utf-8'))
                        result = json.dumps(self.get_client(), default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
                        client_socket.send(str(result).encode('utf-8'))
                    else:
                        client_socket.close()
                        print("{}已断开连接".format(client_addr))
                        client_list.remove((client_socket, client_addr))
                except (BlockingIOError, ConnectionResetError):
                    pass

    def stop_thread(self):
        def _async_raise(tid, exctype):
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
        thread = self.t
        _async_raise(thread.ident, SystemExit)

