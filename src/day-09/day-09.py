#%% Input


def readHeightMap(inp: str):
    with open(inp, "r") as file:
        return [[int(x) for x in list(line.strip())] for line in file.readlines()]


#%% Part 1

import numpy as np
import scipy.ndimage as ndimage

hMap = np.array(readHeightMap("input.txt"))

neighborFootprint = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
)


def filter(values):
    if values[2] == max(values):
        return -1
    if values[2] == min(values):
        return values[2]
    return -1


best = ndimage.generic_filter(hMap, (filter), footprint=neighborFootprint)
riskLevels = best + 1
riskLevels

result = riskLevels.sum()
print("Result:", result)


#%% Part 2

from pylab import *
from scipy.ndimage import measurements
from skimage.measure import label, regionprops

hMap = np.array(readHeightMap("input.txt"))
hMap += 1
hMap[hMap == 10] = 0

labels, num_labels = measurements.label(hMap)
areas = sorted([region.area for region in regionprops(labels)])

result = np.prod(areas[-3:])
print("Result:", result)

imshow(labels, origin="lower", interpolation="nearest")
