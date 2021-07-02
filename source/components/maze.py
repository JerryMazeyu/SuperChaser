import pygame
from .. import constants as C
from . import coin, brick, road, boom, player, candidate, target
from .. import tools
pygame.font.init()
import time
import numpy as np
from source.runtime import ClientInfo
import random
from config import option

class Maze:
    def __init__(self, runtime):
        self.runtime = runtime
        self.mazeinfo = runtime.mazeinfo
        self.maze = self.mazeinfo['maze']
        self.player_coordinate = [1, 1]
        self.target_coordinate = [int(len(self.maze)-1/2)-1, int(len(self.maze)-1/2)-1]
        self.client_info = ClientInfo(option.init_score, (10,10), len(self.maze), self.runtime.gameinfo['round'],
                                      self.mazeinfo['bonusValue'], 0,self.player_coordinate, self.target_coordinate)
        self.mazearea = C.MAZE_AREA
        self.ele_shape = (int(self.mazearea[3] / max(len(self.maze), len(self.maze[0]))),
                          int(self.mazearea[3] / max(len(self.maze), len(self.maze[0]))))
        self.element_group = pygame.sprite.Group()
        self.bright_group = pygame.sprite.Group()
        self.brick_group = pygame.sprite.Group()
        self.boom_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()

        self.target_history = []
        self.oppo_dir = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
        self.build_maze()
        self.setup_player()
        self.setup_target()
        self.candidate = candidate.Candidate(self.cal_location(self.player_coordinate), (self.ele_shape[0]-5, self.ele_shape[1]-5))

    def build_maze(self):
        for ii in range(len(self.maze)):
            for jj in range(len(self.maze[ii])):
                location = self.cal_location((ii, jj))
                if self.maze[ii][jj] == 1:
                    element = brick.Brick(location, self.ele_shape, dark=True)
                    self.brick_group.add(element)
                elif self.maze[ii][jj] in [0, 9]:
                    element = road.Road(location, self.ele_shape, dark=True)
                elif self.maze[ii][jj] == -1:
                    element = boom.Boom(location, self.ele_shape, dark=True)
                    self.boom_group.add(element)
                else:
                    element = coin.FlashingCoin(location, self.ele_shape, dark=True)
                    self.coin_group.add(element)
                self.element_group.add(element)

    def setup_player(self):
        self.player = player.Player((self.ele_shape[0]-5, self.ele_shape[1]-3))

    def setup_target(self):
        self.target = target.Target((self.ele_shape[0]-5, self.ele_shape[1]-3))

    def move(self, type):
        target = self.player
        self.client_info.total_steps += 1
        current_coordinate = self.player_coordinate
        if type == 'left':
            target.left()
            candidate_cor = [current_coordinate[0], current_coordinate[1]-1]
        elif type == 'right':
            target.right()
            candidate_cor = [current_coordinate[0], current_coordinate[1]+1]
        elif type == 'up':
            candidate_cor = [current_coordinate[0]-1, current_coordinate[1]]
        elif type == 'down':
            candidate_cor = [current_coordinate[0]+1, current_coordinate[1]]

        item_type, item = self.check_move(candidate_cor)

        if item_type == 'road':
            current_coordinate = candidate_cor
            self.runtime.gameinfo['score'] -= 1
        elif item_type == 'coin':
            current_coordinate = candidate_cor
            self.runtime.gameinfo['score'] += self.runtime.mazeinfo['bonusValue']  # TODO: 把client中地图信息修改掉
            item.symbol = 0
            item.eaten()
            self.maze[current_coordinate[0]][current_coordinate[1]] = 0
        elif item_type == 'brick':
            self.runtime.gameinfo['score'] -= 2
        elif item_type == 'boom':
            self.runtime.gameinfo['score'] -= 1000

        self.client_info.score = self.runtime.gameinfo['score']

        self.player_coordinate = current_coordinate
        self.player_location = self.cal_location(current_coordinate)
        target.rect.center = self.player_location
        self.process_neighbours()
        self.move_target()
        self.client_info.player_cord = self.player_coordinate
        self.client_info.target_cord = self.target_coordinate
        time.sleep(0.1)

    def move_target(self):
        difficulty = self.runtime.gameinfo['difficulty']
        if difficulty == 'simple':
            if random.uniform(0, 1) >= 0.8:
                return
        if self.player_coordinate == self.target_coordinate:
            return
        target_candidate = {'up': [self.target_coordinate[0] - 1, self.target_coordinate[1]],
                            'down': [self.target_coordinate[0] + 1, self.target_coordinate[1]],
                            'left': [self.target_coordinate[0], self.target_coordinate[1] - 1],
                            'right': [self.target_coordinate[0], self.target_coordinate[1] + 1]}
        direct_cand = []
        coor_cand = []
        if abs(self.target_coordinate[0]-self.player_coordinate[0])>C.MODAL_RANGE or abs(self.target_coordinate[1]-self.player_coordinate[1])>C.MODAL_RANGE:
            for k,v in target_candidate.items():
                if self.maze[v[0]][v[1]] in [0, 2]:
                    if k in self.target_history[-3:]:
                        if random.uniform(0,1) > 0.7:
                            direct_cand.append(k)
                            coor_cand.append(v)
                    else:
                        oppo_dir = self.oppo_dir[k]
                        direct_cand.append(oppo_dir)
                        coor_cand.append(v)
            if coor_cand != []:
                choosen_ind = random.randint(0, len(coor_cand)-1)
                self.target_coordinate = coor_cand[choosen_ind]
                self.target_history.append(direct_cand[choosen_ind])
            else:
                self.target_history.append("nothing")
        else:
            current_distance = self.get_distance(self.target_coordinate, self.player_coordinate)
            back_cor_cand = []
            back_dir_cand = []
            for k,v in target_candidate.items():
                if self.maze[v[0]][v[1]] in [0, 2]:
                    candidate_distance = self.get_distance(self.player_coordinate, v)
                    if candidate_distance >= current_distance:
                        direct_cand.append(k)
                        coor_cand.append(v)
                    else:
                        back_dir_cand.append(k)
                        back_cor_cand.append(v)
            if coor_cand == []:
                coor_cand = back_cor_cand
                direct_cand = back_dir_cand
            if coor_cand != []:
                choosen_ind = random.randint(0, len(coor_cand) - 1)
                self.target_coordinate = coor_cand[choosen_ind]
                self.target_history.append(direct_cand[choosen_ind])
            else:
                self.target_history.append("nothing")

    def get_distance(self, x, y):
        return np.sqrt(np.square(x[0]-y[0]) + np.square(x[1]-y[1]))


    def update_player(self):
        self.player_location = self.cal_location(self.player_coordinate)
        self.player.rect.center = self.player_location
        self.player.update()

    def update_target(self):
        self.target_location = self.cal_location(self.target_coordinate)
        self.target.rect.center = self.target_location
        self.target.update()

    def check_move(self, candidate):
        item = self.get_collide_sprite(candidate)
        return item.name, item

    def get_collide_sprite(self, cor):
        loc = self.cal_location(cor)
        self.candidate.rect.center = loc[0], loc[1]
        return pygame.sprite.spritecollide(self.candidate, self.element_group, False)[0]

    def process_neighbours(self, range_=C.MODAL_RANGE):
        minX, minY, maxX, maxY = self.get_local_range(range_)
        for i in range(minX, maxX+1):
            for j in range(minY, maxY+1):
                sp = self.get_collide_sprite([j, i])
                self.client_info.maze[j][i] = sp.symbol
                sp.lighten()

    def get_local_range(self, range_):
        center = self.player_coordinate
        minY = max(center[0] - range_, 0)
        maxY = min(center[0] + range_, len(self.maze)-1)
        minX = max(center[1] - range_, 0)
        maxX = min(center[1] + range_, len(self.maze[0])-1)
        return (minX, minY, maxX, maxY)

    def cal_location(self, coordinate):
        y, x = coordinate
        rect_y = self.mazearea[1] + (y + 1) * (self.ele_shape[0])
        rect_x = self.mazearea[0] + (x + 1) * (self.ele_shape[1])
        return rect_x, rect_y

    def cal_coordinate(self, rect):
        y = (rect[1] - self.mazearea[1]) / self.ele_shape[0] - 1
        x = (rect[1] - self.mazearea[0]) / self.ele_shape[1] - 1
        return x, y

    def update(self, keys):
        self.element_group.update()
        self.update_player()
        self.update_target()
        if keys[pygame.K_RIGHT]:
            self.move('right')
        if keys[pygame.K_LEFT]:
            self.move('left')
        if keys[pygame.K_UP]:
            self.move('up')
        if keys[pygame.K_DOWN]:
            self.move('down')

    def draw(self, surface):
        for ele in self.element_group:
            surface.blit(ele.image, ele.rect)
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.target.image, self.target.rect)

