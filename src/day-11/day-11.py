#%% Setup


def readInput(inp: str):
    with open(inp, "r") as file:
        return [[int(n) for n in line.strip()] for line in file.readlines()]


def simulateStep(octos):
    flashList: List[Tuple[int, int]] = []

    for idx, octo in np.ndenumerate(octos):
        octos[idx] += 1
        if octo >= 9:
            flashList.append(idx)

    for idx in flashList:
        mask = np.zeros(octos.shape, dtype=int)

        rows = slice(max(0, idx[0] - 1), min(idx[0] + 2, mask.shape[0]))
        cols = slice(max(0, idx[1] - 1), min(idx[1] + 2, mask.shape[1]))

        mask[rows, cols] = 1
        mask[idx] = 0

        neighbors = list(zip(*mask.nonzero()))

        for neighbor in neighbors:
            octos[neighbor] += 1
            if octos[neighbor] == 10:
                flashList.append(neighbor)

    for idx in flashList:
        octos[idx] = 0

    return len(flashList)


#%% Part 1

from typing import List, Tuple
import numpy as np

octos = np.array(readInput("input.txt"))


flashCounter = 0
for i in range(100):
    flashCounter += simulateStep(octos)
    print(f"After step {i+1}:")
    print(octos)

print("Result:", flashCounter)
