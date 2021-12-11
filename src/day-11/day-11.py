#%% Setup

import numpy as np


def readInput(inp: str):
    with open(inp, "r") as file:
        return [[int(n) for n in line.strip()] for line in file.readlines()]


def maskAdjacent(idx, ndarray: np.ndarray):
    assert len(idx) == len(ndarray.shape), "Index and array dimensions must match"

    mask = np.full(ndarray.shape, False)

    selector = []
    for dim, size in enumerate(mask.shape):
        selector.append(slice(max(0, idx[dim] - 1), min(idx[dim] + 2, size)))

    mask[tuple(selector)] = True
    mask[idx] = False

    return mask


def mask_ndenumerate(ndarray: np.ndarray, mask: np.ndarray):
    assert ndarray.shape == mask.shape, "Array and mask must be of same shape"

    for idx in mask_ndindex(mask):
        yield idx, ndarray[idx]


def mask_ndindex(mask: np.ndarray):
    for idx in zip(*np.where(mask)):
        if mask[idx]:
            yield idx


def simulateStep(octos):
    flashList: List[Tuple[int, int]] = []

    for idx, octo in np.ndenumerate(octos):
        octos[idx] += 1
        if octo >= 9:
            flashList.append(idx)

    for idx in flashList:
        mask = maskAdjacent(idx, octos)

        for idx in mask_ndindex(mask):
            octos[idx] += 1
            if octos[idx] == 10:
                flashList.append(idx)

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
