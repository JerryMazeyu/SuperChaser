from resources.maze.maze_generate import Map


class MazeSolver(object):
    def __init__(self, maze):
        self.path = []
        self.dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.maze = maze

    def mark(self, pos):
        self.maze[pos[0]][pos[1]] = 2

    def passable(self, pos):
        return self.maze[pos[0]][pos[1]] == 0

    def find_path(self, pos, end):
        self.mark(pos)
        if pos == end:
            self.path.append(pos)
            return True
        for i in range(4):
            nextp = pos[0] + self.dirs[i][0], pos[1] + self.dirs[i][1]
            # 考虑下一个可能方向
            if self.passable(nextp):
                if self.find_path(nextp, end):
                    self.path.append(pos)
                    return self.path
        return False

    def see_path(self):
        for i, p in enumerate(self.path):
            if i == 0:
                self.maze[p[0]][p[1]] = "E"
            elif i == len(self.path) - 1:
                self.maze[p[0]][p[1]] = "S"
            else:
                self.maze[p[0]][p[1]] = 3
        print("\n")
        for r in self.maze:
            for c in r:
                if c == 3:
                    print('\033[0;31m' + "*" + " " + '\033[0m', end="")
                elif c == "S" or c == "E":
                    print('\033[0;34m' + c + " " + '\033[0m', end="")
                elif c == 2:
                    print('\033[0;32m' + "#" + " " + '\033[0m', end="")
                elif c == 1:
                    print('\033[0;;40m' + " " * 2 + '\033[0m', end="")
                else:
                    print(" " * 2, end="")
            print()

    def run(self, start, end):
        self.find_path(start, end)
        self.see_path()


if __name__ == '__main__':
    dim = 10
    maze1 = Map.run(dim, dim)
    maze2 = Map.run(dim, dim)
    start = (1, 1)
    end = (dim*2-1, dim*2-1)
    s1 = MazeSolver(maze1)
    s1.run(start, end)
    s2 = MazeSolver(maze2)
    s2.run(start, end)

