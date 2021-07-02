from resources.maze.maze_generate import Map
from resources.maze.maze_decorate import DecorateMaze
from resources.maze.maze_config import opt
from resources.maze.maze_check import MazeCheck
from random import choice


def getMazeInfo():
    boomNum = choice(range(5, 25))
    bonusNum = choice(range(2, 5))
    lst = []
    for i in range(opt.num):
        lst.append(Map.run(opt.dim, opt.dim))
    dm = DecorateMaze(lst, boomNum, bonusNum)
    resultDict = {'maze': dm.getMaze(), 'boomNum': boomNum, 'bonusNum': bonusNum, 'bonusValue': choice(range(5, 50))}
    return resultDict

def get_maze_with_loop(blind_num=opt.blind_num, verbose=True):
    while True:
        maze_info = getMazeInfo()
        mc = MazeCheck(maze_info, opt.blind_depth)
        matching_num = mc.check()
        if matching_num >= blind_num:
            if verbose:
                dm = DecorateMaze()
                dm.showMaze(maze_info['maze'])
            return maze_info




if __name__ == '__main__':
    # print(getMazeInfo())
    get_maze_with_loop()