#%% Setup

from itertools import permutations, product
from icecream import ic
import numpy as np

# fmt:off
IDENTITY = np.array([
    [ 1,  0,  0],
    [ 0,  1,  0],
    [ 0,  0,  1],
])
ROLL_LEFT = np.array([
    [ 0, -1,  0],
    [ 1,  0,  0],
    [ 0,  0,  1],
])
YAW_LEFT = np.array([
    [ 0,  0, -1],
    [ 0,  1,  0],
    [ 1,  0,  0],
])
PITCH_UP = np.array([
    [ 1,  0,  0],
    [ 0,  0,  1],
    [ 0, -1,  0],
])
# fmt:on


def readScanner(inp: str):
    with open(inp, "r") as file:
        scanners = []
        currentScanner = None

        for line in file.read().splitlines():
            if line == "":
                continue

            if line.startswith("---"):
                # New scanner
                if currentScanner:
                    scanners.append(np.array(currentScanner, dtype=int))
                currentScanner = []
                continue

            pt = line.split(",")
            currentScanner.append(pt)
        # Add last scanner
        if currentScanner:
            scanners.append(np.array(currentScanner, dtype=int))

        return scanners


all_rotations_transforms = [
    IDENTITY,
    YAW_LEFT,
    YAW_LEFT @ YAW_LEFT,
    YAW_LEFT @ YAW_LEFT @ YAW_LEFT,
    #
    ROLL_LEFT,
    YAW_LEFT @ ROLL_LEFT,
    YAW_LEFT @ YAW_LEFT @ ROLL_LEFT,
    YAW_LEFT @ YAW_LEFT @ YAW_LEFT @ ROLL_LEFT,
    #
    ROLL_LEFT @ ROLL_LEFT,
    YAW_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    YAW_LEFT @ YAW_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    YAW_LEFT @ YAW_LEFT @ YAW_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    #
    ROLL_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    YAW_LEFT @ ROLL_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    YAW_LEFT @ YAW_LEFT @ ROLL_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    YAW_LEFT @ YAW_LEFT @ YAW_LEFT @ ROLL_LEFT @ ROLL_LEFT @ ROLL_LEFT,
    #
    PITCH_UP,
    YAW_LEFT @ PITCH_UP,
    YAW_LEFT @ YAW_LEFT @ PITCH_UP,
    YAW_LEFT @ YAW_LEFT @ YAW_LEFT @ PITCH_UP,
    #
    PITCH_UP @ PITCH_UP @ PITCH_UP,
    YAW_LEFT @ PITCH_UP @ PITCH_UP @ PITCH_UP,
    YAW_LEFT @ YAW_LEFT @ PITCH_UP @ PITCH_UP @ PITCH_UP,
    YAW_LEFT @ YAW_LEFT @ YAW_LEFT @ PITCH_UP @ PITCH_UP @ PITCH_UP,
]


#%% Part 1

scanners = readScanner("input.txt")

main_scanner = scanners[0]
other_scanners = scanners[1:]

unknown_scanners = other_scanners
scannerPositions = [np.array([0, 0, 0])]

while len(unknown_scanners):
    ic("=== Start batch ===")
    other_scanners = unknown_scanners
    unknown_scanners = []

    for scanner in other_scanners:
        ic("- Next scanner -")

        for iTransform, transform in enumerate(all_rotations_transforms):
            pts = (transform @ scanner.T).T

            distances = [p2 - p1 for p1, p2 in product(main_scanner, pts)]

            uniq, counts = np.unique(distances, axis=0, return_counts=True)
            idx = np.argmax(counts)
            if counts[idx] >= 12:
                offset = uniq[idx]
                ic(iTransform, offset)
                pts = pts - offset

                merged_probes = np.concatenate((main_scanner, pts))
                main_scanner = np.unique(merged_probes, axis=0)
                scannerPositions.append(np.array([0, 0, 0]) - offset)

                break  # NOTE: Maybe there are other rotations that fit even better. If it does not work, remove this and go through all rotations and find the best match
        else:
            unknown_scanners.append(scanner)

print("")
print("Result 1:", len(main_scanner))


#%% Part 2 - Requires part 1

maxManhattanDistance = max(
    sum(abs(a - b)) for a, b in (permutations(scannerPositions, 2))
)
print("Result 2:", maxManhattanDistance)
