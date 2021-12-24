#%%

from enum import Enum
from icecream import ic
import numpy as np
from pipe import map, where
from dataclasses import dataclass


class Action(Enum):
    OFF = 0
    ON = 1


@dataclass()
class Instruction:
    action: Action
    cuboid: np.ndarray


def readRebootInstructions(inp: str) -> tuple[list[Instruction], np.ndarray]:
    instructions = []

    with open(inp, "r") as file:
        for line in file.read().splitlines():

            action, ranges = line.split(" ")
            action = Action.ON if action == "on" else Action.OFF

            ranges = dict(
                ranges.split(",")
                | map(lambda r: r.split("="))
                | map(lambda r: (r[0], r[1].split("..")))
                | map(lambda r: (r[0], (int(r[1][0]), int(r[1][1]))))
            )
            cuboid = np.array(
                [
                    [min(ranges["x"]), min(ranges["y"]), min(ranges["z"])],
                    [max(ranges["x"]), max(ranges["y"]), max(ranges["z"])],
                ],
                dtype=int,
            )

            instructions.append(Instruction(action, cuboid))

    return instructions


def createReactorCuboidFromInstructions(instructions: list[Instruction]):
    reactorCuboid = np.zeros((2, 3), dtype=int)
    for inst in instructions:
        cuboid = inst.cuboid
        tmp = np.vstack((reactorCuboid, cuboid))

        reactorCuboid[0] = np.min(tmp, axis=0)
        reactorCuboid[1] = np.max(tmp, axis=0)
    ic(reactorCuboid)
    return reactorCuboid


def sliceFromVectors(mat: np.ndarray):
    assert len(mat.shape) == 2, f"Matrix must be 2-D"
    assert mat.shape[0] == 2, f"Matrix must contain exactly 2 vectors"
    assert np.min(mat) >= 0, "Matrix vectors must consist of only positive components"

    minVec = np.min(mat, axis=0)
    maxVec = np.max(mat, axis=0)
    return tuple(
        slice(minComponent, maxComponent + 1)
        for minComponent, maxComponent in zip(reversed(minVec), reversed(maxVec))
    )


def translateToPositive(instructions, reactorCuboid):
    reactorOffset = np.min(reactorCuboid, axis=0)
    reactorCuboid -= reactorOffset

    for instr in instructions:
        instr.cuboid -= reactorOffset

    return instructions, reactorCuboid


def createReactor(reactorCuboid):
    assert (
        np.max(np.min(reactorCuboid, axis=0)) >= 0
    ), "Reactor cuboid must be in positive space to create a reactor"
    return np.zeros(tuple(reversed(np.max(reactorCuboid, axis=0) + 1)), dtype=int)


def canonizeCuboid(cuboid):
    return np.array(
        [
            np.min(cuboid, axis=0),
            np.max(cuboid, axis=0),
        ]
    )


def removeLargeInstructions(instructions: list[Instruction]) -> list[Instruction]:
    return list(instructions | where(lambda inst: np.max(np.abs(inst.cuboid)) <= 50))


def cropLargeInstructions(instructions: list[Instruction]) -> list[Instruction]:
    newInstructions = []
    for inst in instructions:
        cuboid = canonizeCuboid(inst.cuboid)

        if cuboid[0, 0] < -50 and cuboid[1, 0] < -50:
            continue
        if cuboid[0, 1] < -50 and cuboid[1, 1] < -50:
            continue
        if cuboid[0, 2] < -50 and cuboid[1, 2] < -50:
            continue

        if cuboid[0, 0] > 50 and cuboid[1, 0] > 50:
            continue
        if cuboid[0, 1] > 50 and cuboid[1, 1] > 50:
            continue
        if cuboid[0, 2] > 50 and cuboid[1, 2] > 50:
            continue

        inst.cuboid[inst.cuboid < -50] = -50
        inst.cuboid[inst.cuboid > 50] = 50

        newInstructions.append(inst)
    return newInstructions


#%% Part 1

instructions = readRebootInstructions("input.txt")

instructions = cropLargeInstructions(instructions)
reactorCuboid = createReactorCuboidFromInstructions(instructions)

instructions, reactorCuboid = translateToPositive(instructions, reactorCuboid)

reactor = createReactor(reactorCuboid)

for instr in instructions:
    s = sliceFromVectors(instr.cuboid)
    reactor[s] = instr.action.value
    ic(np.sum(reactor))

ic(reactor)
ic(np.sum(reactor))

activeCubes = np.sum(reactor)
print()
print("Result 1:", activeCubes)


#%% Part 2

instructions = readRebootInstructions("input.txt")

# instructions = cropLargeInstructions(instructions)
# reactorCuboid = createReactorCuboidFromInstructions(instructions)

# instructions, reactorCuboid = translateToPositive(instructions, reactorCuboid)

# reactor = createReactor(reactorCuboid)

s = 0
for instr in instructions:
    cuboid = canonizeCuboid(instr.cuboid)
    cuboid -= cuboid[0]
    ic(cuboid, np.prod(cuboid[1]))
    s += np.prod(cuboid[1])
ic(s)

#%%

# NOTE: From here on, a cuboid must always fullfill the following requirements:
#       - The first vector must always be the one closer to the origin. => If
#         the second vector is closer to the origin, the volume is assumed to be
#         negative.
#       - The second vector is **exclusive**, meaning that it's coordinate is
#         not part of the cuboids volume. E.g. `([10,10,10],[11,11,11])` has a
#         volume of `0` and `([5,5,5],[11,11,11])` has a volume of `5*5*5=125`

# TODO: Change everything to consider the second vector of a cuboid to be
#       exclusive like described above.

# fmt:off
a = canonizeCuboid(np.array([
    [10, 10],
    [20, 20],
]))
b = canonizeCuboid(np.array( [
    [5, 5],
    [25, 25],
]))
b = canonizeCuboid(np.array( [
    [5, 5],
    [25, 25],
]))
# fmt:on


def _make3d(vecOrMat: np.ndarray) -> np.ndarray:
    if len(vecOrMat.shape) == 1:
        # Vector
        vecOrMat = [vecOrMat]
    # Matrix
    return np.array([[vec[0], vec[1], i] for i, vec in enumerate(vecOrMat)])


def volume(canonizedCuboid: np.ndarray) -> int:
    # TODO: cub[1] is going to be exclusive, so do `cub[1] -1` first
    cub = canonizedCuboid
    cub -= cub[0]
    return np.prod(cub[1])


def isAllPositive(vec: np.ndarray) -> bool:
    return np.min(vec) > 0


def isAllNegative(vec: np.ndarray) -> bool:
    return np.max(vec) < 0


def liesWithin(vec: np.ndarray, canonizedCuboid: np.ndarray) -> bool:
    # TODO: Consider points within if they are greater or equal to the cuboids
    #       first vector and if they are smaller than the cuboids second vector.
    cub = canonizedCuboid
    return isAllPositive(vec - cub[0]) and isAllNegative(vec - cub[1])


def getCubeVertices(canonizedCuboid: np.ndarray) -> np.ndarray:
    cub = canonizedCuboid
    return np.array(
        [
            [cub[0, 0], cub[0, 1], cub[0, 2]],
            [cub[1, 0], cub[0, 1], cub[0, 2]],
            [cub[0, 0], cub[1, 1], cub[0, 2]],
            [cub[1, 0], cub[1, 1], cub[0, 2]],
            [cub[0, 0], cub[0, 1], cub[1, 2]],
            [cub[1, 0], cub[0, 1], cub[1, 2]],
            [cub[0, 0], cub[1, 1], cub[1, 2]],
            [cub[1, 0], cub[1, 1], cub[1, 2]],
        ]
    )


def splitCuboid(canonizedCuboid: np.ndarray, vec: np.ndarray) -> np.ndarray:
    cub = canonizedCuboid
    # fmt:off
    return np.array([
        # FIXME: The cubes volume will increase if vec is outside of it. Maybe
        #        using the min/max of some values can fix this. Eg. min(cub[0],
        #        vec) to prevent it from growing towards the origin. But make
        #        sure that it does not prevent the cuboids with negative volume.
        #        Maybe it is possible to clamp the cutting vector `vec` to be
        #        within the cube.
        [ [cub[0,0], cub[0,1], cub[0,2]],   [vec[0] -1, vec[1] -1, vec[2] -1 ] ], # 1
        [ [vec[0],   cub[0,1], cub[0,2]],   [cub[1,0],  vec[1] -1, vec[2] -1 ] ], # 2
        [ [cub[0,0], vec[1],   cub[0,2]],   [vec[0] -1, cub[1,1],  vec[2] -1 ] ], # 3
        [ [vec[0],   vec[1],   cub[0,2]],   [cub[1,0],  cub[1,1],  vec[2] -1 ] ], # 4
        [ [cub[0,0], cub[0,1], vec[2]  ],   [vec[0] -1, vec[1] -1, cub[1,2]  ] ], # 5
        [ [vec[0],   cub[0,1], vec[2]  ],   [cub[1,0],  vec[1] -1, cub[1,2]  ] ], # 6
        [ [cub[0,0], vec[1],   vec[2]  ],   [vec[0] -1, cub[1,1],  cub[1,2]  ] ], # 7
        [ [vec[0],   vec[1],   vec[2]  ],   [cub[1,0],  cub[1,1],  cub[1,2]  ] ], # 8
    ])
    # fmt:on


a3 = _make3d(a)
ic(a3)
ic(getCubeVertices(a3))
ic("---")
for vertex in getCubeVertices(a3):
    ic(liesWithin(vertex, a3))

#%%

a3[0, 2] = 10
a3[1, 2] = 20
ic(a3)
ic(splitCuboid(a3, [11, 11, 11]))


pass
