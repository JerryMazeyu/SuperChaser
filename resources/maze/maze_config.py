from config import option


class Opt(object):
    def __init__(self):
        self.dim = option.maze_dim  # 迷宫维度
        self.num = 2  # 迷宫由几个子迷宫拼成
        self.blind_num = option.maze_blind_num
        self.blind_depth = option.maze_blind_depth

opt = Opt()
