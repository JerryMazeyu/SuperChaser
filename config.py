class Option:
    def __init__(self):
        self.maze_dim = 9  # 迷宫维度 = ((2 * maze_dim) + 1) * ((2 * maze_dim) + 1)
        self.maze_blind_depth = 4  # 生成迷宫的死路深度
        self.maze_blind_num = 2  # 生成迷宫的死路最小数量
        self.perception_range = 4  # 感知的范围半径
        self.init_score = 100  # 初始分数
        self.maze_file_path = "/Users/mazeyu/PythonProject/2021.05/SuperChaser/maze.txt"


option = Option()
