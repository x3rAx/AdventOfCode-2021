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


#%% Part 1


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
