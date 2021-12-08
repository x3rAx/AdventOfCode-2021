#%% Part 1


def readInp(file: str):
    with open(file, "r") as inp:
        displays = []
        for line in inp.readlines():
            line = line.strip()
            patterns, output = line.split("|")
            patterns = patterns.strip().split(" ")
            output = output.strip().split(" ")
            displays.append((patterns, output))
        return displays


displays = readInp("input.txt")

outputs = [output for (patterns, output) in displays]

# 0 = 6 segments
# 1 = 2 segments *
# 2 = 5 segments
# 3 = 5 segments
# 4 = 4 segments *
# 5 = 5 segments
# 6 = 6 segments
# 7 = 3 segments *
# 8 = 7 segments *
# 9 = 6 segments


def flatten(lst: list):
    return [item for sublist in lst for item in sublist]


outputsMerged = flatten(outputs)


identifyingOutputs = list(
    filter(
        lambda x: len(x) == 2 or len(x) == 4 or len(x) == 3 or len(x) == 7,
        outputsMerged,
    )
)

print("Result:", len(identifyingOutputs))
