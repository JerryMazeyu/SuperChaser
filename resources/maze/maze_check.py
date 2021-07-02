import numpy as np
from numpy.lib.stride_tricks import as_strided
from copy import deepcopy


class MazeCheck(object):
    def __init__(self, mazeInfo, blind_depth=3):
        self.loop_pattern, self.loop_shape = self.get_loop_pattern(blind_depth)
        self.mazeInfo = mazeInfo
        self.maze = self.reduce_map()

    def check(self):
        matching_num = 0
        sub_matrix_list = []
        for sp in self.loop_shape:
            sub_matrix_list += self.get_sub_matrix(self.maze, sp)
        for sub_matrix in sub_matrix_list:
            for pat in self.loop_pattern:
                pat = np.array(pat)
                sub_matrix = np.array(sub_matrix)
                if pat.shape == sub_matrix.shape:
                    if (pat == sub_matrix).all():
                        matching_num += 1
        return matching_num

    def get_sub_matrix(self, matrix, sub_shape):
        matrix = np.array(matrix)
        sub_shape = sub_shape
        view_shape = tuple(np.subtract(matrix.shape, sub_shape) + 1) + sub_shape
        arr_view = as_strided(matrix, view_shape, matrix.strides * 2)
        arr_view = arr_view.reshape((-1,) + sub_shape)
        arr_view = arr_view.tolist()
        return arr_view

    def get_loop_pattern(self, depth):
        """获取死路模式"""
        up = [[1] * 3]
        up += [[1,0,1] for x in range(depth)]
        down = [[1,0,1] for x in range(depth)]
        down += [[1] * 3]
        left = [[1] * (depth + 1)]
        left += [[1, *[0 for x in range(depth)]]]
        left += [[1] * (depth + 1)]
        right = [[1] * (depth + 1)]
        right += [[*[0 for x in range(depth)], 1]]
        right += [[1] * (depth + 1)]
        pattern_list = [up, down, left, right]
        return pattern_list, [(depth+1, 3), (3, depth+1)]

    def reduce_map(self):
        """获取朴素地图"""
        maze = deepcopy(self.mazeInfo['maze'])
        for row in range(len(maze)):
            for col in range(len(maze[row])):
                ele = maze[row][col]
                if ele == -1:
                    maze[row][col] = 1
                elif ele in [9, 2]:
                    maze[row][col] = 0
        return maze

# def get_map():
#     flag = True
#     while flag:
#         mazeInfo = getMazeInfo()
#         mc = MazeCheck(mazeInfo)
#         matching_num = mc.check()
#         if matching_num > 0:
#             flag = False




if __name__ == '__main__':
    # mazeInfo = getMazeInfo()
    # mc = MazeCheck(mazeInfo)
    # matching_num = mc.check()
    # print(matching_num)
    # dm = DecorateMaze()
    # dm.showMaze(mazeInfo['maze'])
    pass



