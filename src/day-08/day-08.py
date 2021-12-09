#%% Setup


def readInp(file: str):
    with open(file, "r") as inp:
        displays = []
        for line in inp.readlines():
            line = line.strip()
            patterns, outputs = line.split("|")
            patterns = patterns.strip().split(" ")
            outputs = outputs.strip().split(" ")
            patterns = [sorted(list(x)) for x in patterns]
            outputs = [sorted(list(x)) for x in outputs]
            displays.append((patterns, outputs))
        return displays


#%% Part 1

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


#%% Part 2

# Oh, every line contains patterns for all ten numbers.. so then this could be
# done much simpler... See cell below

# from itertools import permutations

## fmt: off
# _one   = "..c..f."
# _two   = "a.cde.g"
# _three = "a.cd.fg"
# _four  = ".bcd.f."
# _five  = "ab.de.g"
# _six   = "ab.defg"
# _seven = "a.c..f."
# _eight = "abcdefg"
# _nine  = "abcd.fg"
# _zero  = "abc.efg"
## fmt: on


# def assertLen(length: int, inp: str, num: str):
#    inpLen = len(inp)
#    if inpLen != length:
#        raise Exception(
#            f"Input for number {num} is expected to be of length {length} but was of length {inpLen}"
#        )


# def one(inp: str):
#    assertLen(2, inp, "1")
#    return ["..{0}..{1}.".format(*x) for x in permutations(inp)]


# one("ab")


#%%

from pprint import pprint

displays = readInp("input.txt")

outputSum = 0
for patterns, outputs in displays:
    segments = {
        "a": None,
        "c": None,
        "f": None,
    }
    known = {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
        8: None,
        9: None,
        0: None,
    }
    patterns_2_3_5 = []
    patterns_6_9_0 = []
    for pattern in patterns.copy():

        # Digit 1
        if len(pattern) == 2:
            known[1] = pattern
            continue

        # Digit 7
        if len(pattern) == 3:
            known[7] = pattern
            continue

        # Digit 4
        if len(pattern) == 4:
            known[4] = pattern
            continue

        # One of 2, 3, 5
        if len(pattern) == 5:
            patterns_2_3_5.append(pattern)
            continue

        # One of 6, 9, 0
        if len(pattern) == 6:
            patterns_6_9_0.append(pattern)
            continue

        # Digit 8
        if len(pattern) == 7:
            known[8] = pattern
            continue

    # Find segment "a" by getting the segment in "7" that is not in "1"
    one = known[1]
    for seg in known[7]:
        if seg not in known[1]:
            segments["a"] = seg
            break

    for pattern in patterns_6_9_0:
        # Find 6: Find the one with len=6 that does not include both segments of
        #         "1"
        if not known[6]:
            if one[0] not in pattern:
                known[6] = pattern
                segments["c"] = one[0]
                segments["f"] = one[1]
                continue
            if one[1] not in pattern:
                known[6] = pattern
                segments["c"] = one[1]
                segments["f"] = one[0]
                continue

        # Find 0: Is, after "6" which is already handled, the one that does not
        #         have the same segments as "4"
        if not known[0]:
            for seg in known[4]:
                if seg not in pattern:
                    known[0] = pattern
                    break
            # Did we find 0 in this round?
            if known[0]:
                continue

        # Find 9: the only one left
        known[9] = pattern

    for pattern in patterns_2_3_5:
        # Find 2: "2" is lacking the "f" segment
        if segments["f"] not in pattern:
            known[2] = pattern
            continue

        # Find 5: "5" is lacking the "c" segment
        if segments["c"] not in pattern:
            known[5] = pattern
            continue

        # Find 3: is the only one left
        known[3] = pattern

    # pprint(segments)
    # pprint(known)

    decode = dict(("".join(code), num) for (num, code) in known.items())

    output = 0
    for code in outputs:
        code = ''.join(code)
        digit = decode[code]
        output *= 10
        output += digit
    outputSum += output

print("Result:", outputSum)
