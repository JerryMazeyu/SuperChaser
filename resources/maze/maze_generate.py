from random import randint, choice
from enum import Enum

class MAP_ENTRY_TYPE(Enum):
    MAP_EMPTY = 0,
    MAP_BLOCK = 1,

class WALL_DIRECTION(Enum):
    WALL_LEFT = 0,
    WALL_UP = 1,
    WALL_RIGHT = 2,
    WALL_DOWN = 3,


class Map():
    def __init__(self, width, height):
        self.width = 2*width + 1
        self.height = 2*height + 1
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]

    def resetMap(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.setMap(x, y, value)

    def setMap(self, x, y, value):
        if value == MAP_ENTRY_TYPE.MAP_EMPTY:
            self.map[y][x] = 0
        elif value == MAP_ENTRY_TYPE.MAP_BLOCK:
            self.map[y][x] = 1

    def isVisited(self, x, y):
        return self.map[y][x] != 1

    def showMap(self):
        for row in self.map:
            s = ''
            for entry in row:
                if entry == 0:
                    s += ' 0'
                elif entry == 1:
                    s += ' #'
                else:
                    s += ' X'
            print(s)

    def getMap(self):
        return self.map

    @staticmethod
    def checkAdjacentPos(map, x, y, width, height, checklist):
        directions = []
        if x > 0:
            if not map.isVisited(2 * (x - 1) + 1, 2 * y + 1):
                directions.append(WALL_DIRECTION.WALL_LEFT)

        if y > 0:
            if not map.isVisited(2 * x + 1, 2 * (y - 1) + 1):
                directions.append(WALL_DIRECTION.WALL_UP)

        if x < width - 1:
            if not map.isVisited(2 * (x + 1) + 1, 2 * y + 1):
                directions.append(WALL_DIRECTION.WALL_RIGHT)

        if y < height - 1:
            if not map.isVisited(2 * x + 1, 2 * (y + 1) + 1):
                directions.append(WALL_DIRECTION.WALL_DOWN)

        if len(directions):
            direction = choice(directions)
            if direction == WALL_DIRECTION.WALL_LEFT:
                map.setMap(2 * (x - 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
                map.setMap(2 * x, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
                checklist.append((x - 1, y))
            elif direction == WALL_DIRECTION.WALL_UP:
                map.setMap(2 * x + 1, 2 * (y - 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
                map.setMap(2 * x + 1, 2 * y, MAP_ENTRY_TYPE.MAP_EMPTY)
                checklist.append((x, y - 1))
            elif direction == WALL_DIRECTION.WALL_RIGHT:
                map.setMap(2 * (x + 1) + 1, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
                map.setMap(2 * x + 2, 2 * y + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
                checklist.append((x + 1, y))
            elif direction == WALL_DIRECTION.WALL_DOWN:
                map.setMap(2 * x + 1, 2 * (y + 1) + 1, MAP_ENTRY_TYPE.MAP_EMPTY)
                map.setMap(2 * x + 1, 2 * y + 2, MAP_ENTRY_TYPE.MAP_EMPTY)
                checklist.append((x, y + 1))
            return True
        else:
            return False

    @staticmethod
    def randomPrim(map, width, height):
        startX, startY = (randint(0, width - 1), randint(0, height - 1))
        map.setMap(2 * startX + 1, 2 * startY + 1, MAP_ENTRY_TYPE.MAP_EMPTY)

        checklist = []
        checklist.append((startX, startY))
        while len(checklist):
            entry = choice(checklist)
            if not map.checkAdjacentPos(map, entry[0], entry[1], width, height, checklist):
                checklist.remove(entry)
    @staticmethod
    def doRandomPrim(map):
        map.resetMap(MAP_ENTRY_TYPE.MAP_BLOCK)
        map.randomPrim(map, (map.width - 1) // 2, (map.height - 1) // 2)

    @classmethod
    def run(cls, w, h, verbose=False):
        map = Map(w, h)
        Map.doRandomPrim(map)
        if verbose:
            map.showMap()
        return map.getMap()



if __name__ == '__main__':
    res = Map.run(5,5,True)
    print(res)
