#%% Setup

import numpy as np


def readPaper(inp: str) -> tuple[np.ndarray, list[tuple[slice, slice]]]:
    with open(inp, "r") as file:
        dots = np.array([[]], dtype=int)
        slices = []
        for line in file.read().splitlines():
            if line.startswith("fold along"):
                # Add slices
                _, _, fold = line.split(" ")
                dim, idx = fold.split("=")
                idx = int(idx)
                if dim == "x":
                    slice_a = (slice(None), slice(None, idx))
                    slice_b = (slice(None), slice(None, -idx - 1, -1))
                if dim == "y":
                    slice_a = (slice(None, idx), slice(None))
                    slice_b = (slice(None, -idx - 1, -1), slice(None))
                slices.append((slice_a, slice_b))
                continue

            if line.startswith("#"):
                continue
            if line == "":
                continue

            # Add dots
            col, row = line.split(",")
            col, row = int(col), int(row)

            pad_row = max(0, row - dots.shape[0] + 1)
            pad_col = max(0, col - dots.shape[1] + 1)
            dots = np.pad(dots, ((0, pad_row), (0, pad_col)), "constant")

            dots[row, col] = 1

    return (np.array(dots), slices)


def printPaper(filename, d2array):
    with open(filename, "w") as file:
        for line in d2array:
            for el in line:
                el = "#" if el == 1 else "."
                file.write(el)
            file.write("\n")


#%% Part 1

paper, folds = readPaper("test-input.txt")

print("Initial paper shape:", paper.shape)
print("Initial paper dots:", len(paper.nonzero()[0]))
#printPaper("paper-1.txt", paper)

firstFold = folds[0]
print(firstFold)

a = paper[firstFold[0]]
b = paper[firstFold[1]]
#printPaper("paper-2-a.txt", a)
#printPaper("paper-2-b.txt", b)

paper = a
paper[b == 1] = 1

print("Paper shape:", paper.shape)
print("Paper dots:", len(paper.nonzero()[0]))
#printPaper("paper-2.txt", paper)


#%% Part 2

paper, folds = readPaper("test-input.txt")

for fold in folds:
    a = paper[fold[0]]
    b = paper[fold[1]]

    paper = a
    paper[b == 1] = 1

paper
