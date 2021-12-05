#%% Setup

import re
from pprint import pprint
from typing import List


def readBingo(file: str):
    numbers = None
    boards = []
    currentBoard = []

    with open(file, "r") as inp:
        for line in inp.readlines():
            line = line.strip()

            if not numbers:
                numbers = [int(x) for x in line.split(",")]
                continue

            if line == "":
                if currentBoard:
                    boards.append(Board(currentBoard))
                currentBoard = []
                continue

            boardLine = [int(x) for x in re.split(" +", line)]
            currentBoard.append(boardLine)

    if currentBoard:
        boards.append(Board(currentBoard))

    return numbers, boards


class Board:
    _board: List[List[int]]
    _checked: List[List[bool]]

    def __init__(self, values: List[List[int]]):
        self._board = values
        # Add a 2D list with an element for every element in `values` and set
        # all to False
        self._checked = [[False for _ in row] for row in values]

    def check(self, num) -> bool:
        for y, row in enumerate(self._board):
            for x, col in enumerate(row):
                if col == num:
                    self._checked[y][x] = True

                    if self.testRow(y):
                        return True
                    if self.testCol(x):
                        return True
                    return []

    def testRow(self, y):
        for x, row in enumerate(self._checked[y]):
            if row == False:
                return False
        return True

    def testCol(self, x):
        for y, col in enumerate([row[x] for row in self._checked]):
            if col == False:
                return False
        return True

    def getUnmarked(self):
        unmarked = []
        for y, row in enumerate(self._checked):
            for x, checked in enumerate(row):
                if checked:
                    continue

                unmarked.append(self._board[y][x])
        return unmarked


#%% Part 1

def part1():
    numbers, boards = readBingo("input.txt")

    for num in numbers:
        for board in boards:
            if bingo := board.check(num):
                print("BINGO")
                break
        else:
            continue
        break
    unmarked = board.getUnmarked()
    print(num, unmarked)

    print("Result:", sum(unmarked) * num)


part1()


#%% Part 2

def part2():
    numbers, boards = readBingo('input.txt')

    lastBingoBoard = None
    lastBingoNum = 0

    for num in numbers:
        finishedBoards = []
        for board in boards:
            if board.check(num):
                print("BINGO")
                lastBingoNum = num
                lastBingoBoard = board
                finishedBoards.append(board)
        for board in finishedBoards:
            boards.remove(board)

    unmarked = lastBingoBoard.getUnmarked()
    print(lastBingoNum, unmarked)
    print("Result:", sum(unmarked) * lastBingoNum)


part2()
