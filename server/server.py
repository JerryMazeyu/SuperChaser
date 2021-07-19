import argparse
from source import tools
from config import option
import random
from source import runtime
from source import constants as C
import json
import numpy as np

parser = argparse.ArgumentParser(description="Im2Latex Training Program")
parser.add_argument("-m", "--mode", choices=("train", "test"), default="test", help="游戏模式")
parser.add_argument("-d", "--difficulty", default="hard", help="游戏难度")
parser.add_argument("-n", "--num", default=4, help="创建环境个数")
args = parser.parse_args()

class Player():
    def __init__(self):
        self.cord = None
    def left(self):
        self.cord[1] -= 1
    def right(self):
        self.cord[1] += 1
    def up(self):
        self.cord[0] -= 1
    def down(self):
        self.cord[0] += 1
class Target():
    def __init__(self):
        self.cord = None
        self.history = []
        self.oppo_dir = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}


class Game():
    def __init__(self, mode=args.mode, difficulty=args.difficulty):
        self.mode = mode
        self.difficulty = difficulty
        self.setup_env()
        self.setup_player()
        self.setup_target()
        self.setup_runtime()

    def setup_runtime(self):
        self.runtime.game_info = {'score': 100, 'round': 0, 'mode': self.mode, 'difficulty': self.difficulty}
        self.runtime.client_info = runtime.ClientInfo(option.init_score, (10, 10), len(self.maze),
                                                      self.runtime.game_info['round'],
                                                      self.runtime.maze_info['bonusValue'], 0, self.player.cord,
                                                      self.target.cord)
        self.client_info = self.runtime.client_info

    def setup_env(self):
        self.runtime = runtime.RuntimeGlobalInfo()
        if self.mode == 'train':
            self.runtime.maze_info = tools.get_blind_maze()
        else:
            with open(option.maze_file_path, 'r') as f:
                k = f.readlines()
                k = [eval(x.strip('\n')) for x in k]
            self.runtime.maze_info = random.choice(k)
        self.maze_info = self.runtime.maze_info
        self.maze = self.maze_info['maze']

    def setup_player(self):
        self.player = Player()
        self.player.cord = [1, 1]

    def setup_target(self):
        self.target = Target()
        self.target.cord = [int(len(self.maze)-1/2)-1, int(len(self.maze)-1/2)-1]

    def player_move(self, type_):
        self.client_info.total_steps += 1
        current_coordinate = self.player.cord
        candidate_cor = None
        if type_ == 'left':
            candidate_cor = [current_coordinate[0], current_coordinate[1] - 1]
        elif type_ == 'right':
            candidate_cor = [current_coordinate[0], current_coordinate[1] + 1]
        elif type_ == 'up':
            candidate_cor = [current_coordinate[0] - 1, current_coordinate[1]]
        elif type_ == 'down':
            candidate_cor = [current_coordinate[0] + 1, current_coordinate[1]]

        item_type = self.check_move(candidate_cor)

        if item_type == 'road':
            current_coordinate = candidate_cor
            self.runtime.game_info['score'] -= 1
        elif item_type == 'coin':
            current_coordinate = candidate_cor
            self.runtime.game_info['score'] += self.runtime.maze_info['bonusValue']
            self.maze[current_coordinate[0]][current_coordinate[1]] = 0
        elif item_type == 'brick':
            self.runtime.game_info['score'] -= 2
        elif item_type == 'boom':
            self.runtime.game_info['score'] -= 1000

        self.client_info.score = self.runtime.game_info['score']

        self.player.cord = current_coordinate
        self.process_neighbours()
        self.client_info.player_cord = self.player.cord
        self.move_target()
        self.client_info.target_cord = self.target.cord
        return self.get_client_info()

    def check_move(self, candidate):
        if self.maze[candidate[0]][candidate[1]] == 0:
            return 'road'
        elif self.maze[candidate[0]][candidate[1]] == 2:
            return 'coin'
        elif self.maze[candidate[0]][candidate[1]] == -1:
            return 'boom'
        elif self.maze[candidate[0]][candidate[1]] == 1:
            return 'brick'

    def get_local_range(self, range_):
        center = self.player.cord
        minY = max(center[0] - range_, 0)
        maxY = min(center[0] + range_, len(self.maze)-1)
        minX = max(center[1] - range_, 0)
        maxX = min(center[1] + range_, len(self.maze[0])-1)
        return (minX, minY, maxX, maxY)

    def process_neighbours(self):
        minX, minY, maxX, maxY = self.get_local_range(C.MODAL_RANGE)
        for i in range(minX, maxX+1):
            for j in range(minY, maxY+1):
                symbol = self.maze[j][i]
                self.client_info.maze[j][i] = symbol

    def get_client_info(self):
        return json.dumps(self.runtime.client_info, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)

    def get_distance(self, x, y):
        return np.sqrt(np.square(x[0]-y[0]) + np.square(x[1]-y[1]))

    def move_target(self):
        difficulty = self.runtime.game_info['difficulty']
        if difficulty == 'simple':
            if random.uniform(0, 1) >= 0.8:
                return
        if self.player.cord == self.target.cord:
            return
        target_candidate = {'up': [self.target.cord[0] - 1, self.target.cord[1]],
                            'down': [self.target.cord[0] + 1, self.target.cord[1]],
                            'left': [self.target.cord[0], self.target.cord[1] - 1],
                            'right': [self.target.cord[0], self.target.cord[1] + 1]}
        direct_cand = []
        coor_cand = []
        if abs(self.target.cord[0]-self.player.cord[0])>C.MODAL_RANGE or abs(self.target.cord[1]-self.player.cord[1])>C.MODAL_RANGE:
            for k,v in target_candidate.items():
                if self.maze[v[0]][v[1]] in [0, 2]:
                    if k in self.target.history[-3:]:
                        if random.uniform(0,1) > 0.7:
                            direct_cand.append(k)
                            coor_cand.append(v)
                    else:
                        oppo_dir = self.target.oppo_dir[k]
                        direct_cand.append(oppo_dir)
                        coor_cand.append(v)
            if coor_cand != []:
                choosen_ind = random.randint(0, len(coor_cand)-1)
                self.target.cord = coor_cand[choosen_ind]
                self.target.history.append(direct_cand[choosen_ind])
            else:
                self.target.history.append("nothing")
        else:
            current_distance = self.get_distance(self.target.cord, self.player.cord)
            back_cor_cand = []
            back_dir_cand = []
            for k,v in target_candidate.items():
                if self.maze[v[0]][v[1]] in [0, 2]:
                    candidate_distance = self.get_distance(self.player.cord, v)
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
                self.target.cord = coor_cand[choosen_ind]
                self.target.history.append(direct_cand[choosen_ind])
            else:
                self.target.history.append("nothing")

    def step(self, action):
        return self.player_move(action)

    def showMaze(self, mazeMatrix):
        for x, row in enumerate(mazeMatrix):
            for y, ele in enumerate(row):
                if ele == 2:
                    print(f'\033[1;32m $ \033[0m', end="")
                elif [x, y] in [self.target.cord, self.player.cord]:
                    print('\033[0;32m' + "^ " + " " + '\033[0m', end="")
                elif ele == 1:
                    print(f'\033[1;47m # \033[0m', end="")
                elif ele == 0:
                    print(f'\033[1;40m * \033[0m', end="")
                elif ele == -1:
                    print(f'\033[1;31;47m O \033[0m', end="")
                else:
                    print(f'\033[1;31;48m 9 \033[0m', end="")
            print('')

class Server():
    def __init__(self, game_num=args.num):
        self.games = [Game(args) for _ in range(game_num)]

    def step(self, move_batch:list, verbose=False):
        assert len(move_batch) == len(self.games), ValueError(f"Batch size expected {self.games}, but got {len(move_batch)}")
        res = []
        for ii in range(len(self.games)):
            res.append(json.loads(self.games[ii].step(move_batch[ii])))
            if verbose:
                self.games[ii].showMaze(json.loads(self.games[ii].get_client_info())['maze'])
                print(">" * 40)
                print()
        return res




if __name__ == '__main__':
    s = Server(2)  # 环境个数
    for i in range(10):
        r = s.step(['right', 'right'], verbose=True)








