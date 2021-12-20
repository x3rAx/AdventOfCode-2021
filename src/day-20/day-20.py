#%% Setup

from functools import reduce
from icecream import ic
from scipy import ndimage
from dataclasses import dataclass
from matplotlib import pyplot as plt
import numpy as np


@dataclass()
class InfImage:
    crop: np.ndarray  # Just the part of the image we can see
    rest: int  # All other infinite pixels of the image


def recieveImage(inp: str):
    def convertInpToNum(char: str) -> int:
        num = {
            ".": 0,
            "#": 1,
        }.get(char)
        if num is None:
            raise Exception(f'Invalid input: "{char}"')
        return num

    with open(inp, "r") as file:
        algo = None
        crop = []
        for line in file.read().splitlines():
            if not algo:
                algo = [convertInpToNum(x) for x in line]
                continue

            if line == "":
                continue

            crop.append([convertInpToNum(x) for x in line])

    crop = np.array(crop)
    img = InfImage(crop, 0)

    return algo, img


def enhance(img: InfImage, algo):
    def apply_algo(elems: np.ndarray, algo):
        bin_list = np.char.mod("%d", elems)
        bin_str = "".join(bin_list)
        idx = int(bin_str, 2)
        return algo[idx]

    crop, rest = img.crop, img.rest
    crop = np.pad(crop, 1, "constant", constant_values=rest)
    crop = ndimage.generic_filter(
        crop,
        lambda elems: apply_algo(elems, algo),
        footprint=[
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ],
    )
    rest = algo[0b000_000_000] if rest == 0 else algo[0b111_111_111]

    return InfImage(crop, rest)


#%% Part 2

algo, img = recieveImage("input.txt")

ic(img.rest)
plt.imshow(img.crop)
plt.show()

for _ in range(2):
    img = enhance(img, algo)

    ic(img.rest)
    plt.imshow(img.crop)
    plt.show()

print("Result 1:", img.crop.sum())


#%% Part 2

algo, img = recieveImage("input.txt")

ic(img.rest)
plt.imshow(img.crop)
plt.show()

for i in range(50):
    print(i)
    img = enhance(img, algo)

ic(img.rest)
plt.imshow(img.crop)
plt.show()

print("Result:", img.crop.sum())
