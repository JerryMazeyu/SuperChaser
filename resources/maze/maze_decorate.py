from functools import reduce
from resources.maze.maze_generate import Map
from random import sample
from resources.maze.maze_solver import MazeSolver
from copy import deepcopy


class DecorateMaze(object):
    def __init__(self, mazeList=None, numBoom=20, numBonus=2):
        if not mazeList:
            mazeList = [Map.run(10, 10), Map.run(10, 10)]
        baseMaze = deepcopy(mazeList[0])
        solver = MazeSolver(baseMaze)
        start, end = self.getStartAndEnd(baseMaze)
        self.basePath = solver.find_path(start, end)
        mList = []
        for ii in mazeList:
            mList.append(self.addBoom(ii))
        if len(mazeList) > 1:
            self.maze = reduce(self.mergeMaze, mList)
        else:
            self.maze = mazeList[0]
        self.maze = self.addBoom(self.maze, numBoom)
        self.maze = self.addBonus(self.maze, numBonus)
        self.maze[end[0]][end[1]] = 9

    def getMaze(self):
        return self.maze

    def checkMaze(self, maze):
        for i in maze:
            assert len(i) == len(maze[0])

    def getStartAndEnd(self, maze):
        self.checkMaze(maze)
        return (1, 1), (len(maze)-2, len(maze[0])-2)

    def mergeMaze(self, map1, map2):
        assert len(map1) == len(map2) and len(map1[0]) == len(map2[0]), "Cannot merge!"
        res = []
        for i in range(len(map1)):
            m = []
            for j in range(len(map1[0])):
                ele1 = map1[i][j]
                ele2 = map2[i][j]
                if -1 in (ele1, ele2):
                    m.append(-1)
                elif ele1 == 1 and ele2 == 1:
                    m.append(1)
                elif 0 in (ele1, ele2):
                    m.append(0)
                elif 2 in (ele1, ele2):
                    m.append(2)
            res.append(m)
        return res

    def showMaze(self, mazeMatrix):
        for x, row in enumerate(mazeMatrix):
            for y, ele in enumerate(row):
                if ele == 2:
                    print(f'\033[1;32m $ \033[0m', end="")
                elif (x, y) in self.basePath:
                    print('\033[0;32m' + "* " + " " + '\033[0m', end="")
                elif ele == 1:
                    print(f'\033[1;47m # \033[0m', end="")
                elif ele == 0:
                    print(f'\033[1;40m * \033[0m', end="")
                elif ele == -1:
                    print(f'\033[1;31;47m O \033[0m', end="")
            print('')

    def addBoom(self, maze, boomNum=0):
        coord = [(x, y) for y in range(len(maze)) for x in range(len(maze[0]))]
        def helper(x):
            return x not in self.basePath
        coord = list(filter(helper, coord))
        tarLocation = sample(coord, boomNum)
        for (x, y) in tarLocation:
            maze[x][y] = -1
        return maze

    def addBonus(self, maze, bonusNum=0):
        coord = [(x, y) for y in range(1, len(maze)-1) for x in range(1, len(maze[0])-1)]
        tarLocation = sample(coord, bonusNum)
        for (x, y) in tarLocation:
            maze[x][y] = 2
        return maze

if __name__ == '__main__':
    s = DecorateMaze()