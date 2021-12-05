#%% Input

def importVentLines(file: str) -> Tuple[List[VentLine], Point]:
    ventLines = []
    gridSize = Point(0, 0)
    with open(file, "r") as inp:
        for line in inp.readlines():
            line = line.strip()

            start, end = line.split(" -> ")
            startX, startY = [int(v) for v in start.split(",")]
            endX, endY = [int(v) for v in end.split(",")]

            ventLines.append(VentLine(startX, startY, endX, endY))

            if startX > gridSize.x:
                gridSize = Point(startX, gridSize.y)
            if endX > gridSize.x:
                gridSize = Point(endX, gridSize.y)
            if startY > gridSize.y:
                gridSize = Point(gridSize.x, startY)
            if endY > gridSize.y:
                gridSize = Point(gridSize.x, endY)

    return (ventLines, gridSize)


#%% Part 1

from dataclasses import dataclass
from typing import Callable, List, Tuple
from pprint import pprint


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class VentLine:
    start: Point
    end: Point

    def __init__(self, startX, startY, endX, endY):
        object.__setattr__(self, "start", Point(startX, startY))
        object.__setattr__(self, "end", Point(endX, endY))

    def draw(self, pixelCallback: Callable[[Point], None]):
        start, end = self.start, self.end

        deltaX = abs(start.x - end.x)
        deltaY = abs(start.y - end.y)

        if deltaX < deltaY:
            # Y mode
            if start.y > end.y:
                # Swap start and end
                start, end = end, start
            for y in range(start.y, end.y + 1):
                pixelCallback(Point(start.x, y))
            return

        # X mode
        if start.x > end.x:
            # Swap start and end
            start, end = end, start
        for x in range(start.x, end.x + 1):
            pixelCallback(Point(x, start.y))



class Grid:
    _grid: List[List[int]]

    def __init__(self, width: int, height: int):
        self._grid = [[0 for _ in range(width + 1)] for _ in range(height + 1)]

    def increment(self, point: Point):
        self._grid[point.y][point.x] += 1

    def enumerateGrid(self):
        for y, line in enumerate(self._grid):
            for x, cell in enumerate(line):
                yield x, y, cell


def filterHorizontalAndVertical(line: VentLine):
    return line.start.x == line.end.x or line.start.y == line.end.y


ventLines, gridSize = importVentLines("input.txt")
ventMap = Grid(gridSize.x, gridSize.y)

ventLines = list(filter(filterHorizontalAndVertical, ventLines))

for line in ventLines:
    line.draw(lambda p: ventMap.increment(p))

dangerous = 0
for x, y, val in ventMap.enumerateGrid():
    if val >= 2:
        dangerous += 1

print("Result:", dangerous)

#%% Part 2

from dataclasses import dataclass
from typing import Callable, List, Tuple
from pprint import pprint


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class VentLine:
    start: Point
    end: Point

    def __init__(self, startX, startY, endX, endY):
        object.__setattr__(self, "start", Point(startX, startY))
        object.__setattr__(self, "end", Point(endX, endY))

    def draw(self, drawCallback: Callable[[Point], None]):
        start, end = self.start, self.end

        stepX = sign(end.x - start.x)
        stepY = sign(end.y - start.y)

        if stepX == 0:
            # Y mode
            x = start.x
            for y in range(start.y, end.y + stepY, stepY):
                drawCallback(Point(x, y))
                x += stepX
            return

        # X mode
        y = start.y
        for x in range(start.x, end.x + stepX, stepX):
            drawCallback(Point(x, y))
            y += stepY


def sign(num: int):
    return 1 if num > 0 else -1 if num < 0 else 0


class Grid:
    _grid: List[List[int]]

    def __init__(self, width: int, height: int):
        self._grid = [[0 for _ in range(width + 1)] for _ in range(height + 1)]

    def increment(self, point: Point):
        self._grid[point.y][point.x] += 1

    def enumerateGrid(self):
        for y, line in enumerate(self._grid):
            for x, cell in enumerate(line):
                yield x, y, cell


def filterHorizontalAndVertical(line: VentLine):
    return line.start.x == line.end.x or line.start.y == line.end.y


ventLines, gridSize = importVentLines("input.txt")
ventMap = Grid(gridSize.x, gridSize.y)

#ventLines = list(filter(filterHorizontalAndVertical, ventLines))

for line in ventLines:
    line.draw(lambda p: ventMap.increment(p))

#pprint(ventLines)
#pprint(ventMap._grid)

dangerous = 0
for x, y, val in ventMap.enumerateGrid():
    if val >= 2:
        dangerous += 1

print("Result:", dangerous)
