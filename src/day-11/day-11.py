#%% Setup

import numpy as np


def readInput(inp: str):
    with open(inp, "r") as file:
        return [[int(n) for n in line.strip()] for line in file.readlines()]


def maskAdjacent(idx, ndarray: np.ndarray):
    assert len(idx) == len(ndarray.shape), "Index and array dimensions must match"

    mask = np.zeros(ndarray.shape, dtype=int)

    selector = []
    for dim, size in enumerate(mask.shape):
        selector.append(slice(max(0, idx[dim] - 1), min(idx[dim] + 2, size)))

    mask[tuple(selector)] = 1
    mask[idx] = 0

    return mask


def simulateStep(octos):
    flashList: List[Tuple[int, int]] = []

    for idx, octo in np.ndenumerate(octos):
        octos[idx] += 1
        if octo >= 9:
            flashList.append(idx)

    for idx in flashList:
        mask = maskAdjacent(idx, octos)

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


#%% Part 2

from typing import List, Tuple
import numpy as np

octos = np.array(readInput("input.txt"))
counter = 0
for counter in range(1, 1000):
    flashCounter = simulateStep(octos)
    print(flashCounter)
    if flashCounter >= octos.size:
        break

print("Result:", counter)
