import numpy as np
class RuntimeGlobalInfo:
    def __init__(self):
        pass


class ClientInfo:
    def __init__(self, score=0, target=(9,9), maze_size=9, state=0, bonus_value=0, total_steps=0, player_cord=(1,1), target_cord=(1,1)):
        self.maze = np.ones((maze_size, maze_size)) * -9
        self.maze = self.maze.tolist()
        self.score = score
        self.target = target
        self.state = state
        self.bonus_value = bonus_value
        self.total_steps = total_steps
        self.player_cord = player_cord
        self.target_cord = target_cord


runtime = RuntimeGlobalInfo()
