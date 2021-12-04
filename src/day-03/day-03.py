#%% Part 1

positionCounter = []
with open("input.txt", "r") as inp:
    for lineNum, line in enumerate(inp.readlines()):
        line = line.strip()
        if not positionCounter:
            positionCounter = [int(char) for char in line]
            continue

        for i, char in enumerate(line):
            if char == "1":
                positionCounter[i] += 1

lineCount = lineNum + 1
print("Position counter:", positionCounter)
print("Lines:", lineCount)

# If 1 was on a given position more than lineCount/2 times, then that position
# should be a 1, otherwise a 0
# NOTE: For a TIE, a `1` is selcted. But as this is not mentioned, I think it
#       does not matter
gamma = [1 if x >= lineCount / 2 else 0 for x in positionCounter]
# Invert bits of gamma using XOR
epsilon = [x ^ 1 for x in gamma]

print("Gamma:", gamma)
print("Epsilon:", epsilon)


def bitlistToInt(bitlist):
    result = 0
    for bit in bitlist:
        result = result << 1
        result = result | bit
    return result


gammaRate = bitlistToInt(gamma)
epsilonRate = bitlistToInt(epsilon)
print("Gamma rate:", gammaRate)
print("Epsilon rate:", epsilonRate)
print("Result", gammaRate * epsilonRate)

# NOTE: Idea for pandas:
#       - Read lines
#       - Each char is a column
#       - For each column, count `1`s


#%% Part 2

# For the "axygen generator rating", keep all values, that have, from the left
# position on, the same value as the mos common value of that position in all
# lines. This effectively means, find the number, that is numerivally closest
# to `gammaRate`.
# Same goes for "CO2 scrubber rating" and `epsilonRate` but instead for the
# least common value.
#
# ATTENTION: There is a catch:
# With the algorithm described on AoC, it is possible that among the remaining
# numbers, an equal amount of ones and zeroes for a given position can occure,
# in which case the numbers with `1` should be kept. This destroys the
# "closest to" idea from above 😿

import sys

lastDiffGamma = sys.maxsize
lastDiffEpsilon = sys.maxsize

closestToGamma = 0
closestToEpsilon = 0

with open("input.txt", "r") as inp:
    for line in inp.readlines():
        line = line.strip()

        bitlist = [int(char) for char in line]
        num = bitlistToInt(bitlist)

        diffGamma = abs(gammaRate - num)
        diffEpsilon = abs(epsilonRate - num)

        if diffGamma < lastDiffGamma:
            lastDiffGamma = diffGamma
            closestToGamma = num

        if diffEpsilon < lastDiffEpsilon:
            lastDiffEpsilon = diffEpsilon
            closestToEpsilon = num

print("Closest to gamma (oxygen generator rating):", closestToGamma)
print("Closest to epsilon (CO2 scrubber rating):", closestToEpsilon)
print("NOT the Result:", closestToGamma * closestToEpsilon)


#%% Part 2 - second try


def countOnesOnPos(pos, bitlistList):
    counter = 0
    for bitlist in bitlistList:
        if bitlist[pos] == 1:
            counter += 1
    return counter


def mostCommonBitOnPos(pos, bitlistList):
    listLen = len(bitlistList)
    count = countOnesOnPos(pos, bitlistList)
    # TIE favors `1`
    return 1 if count >= (listLen / 2) else 0


def bitstrToBitlist(bitstr):
    return [int(c) for c in bitstr]


def part2try2():
    bitlistList = []
    with open("input.txt", "r") as inp:
        for line in inp.readlines():
            line = line.strip()

            bitlist = bitstrToBitlist(line)
            bitlistList += [bitlist]

    gammaBitlistList = bitlistList
    for p in range(0, len(bitlistList[0])):
        bitToKeep = mostCommonBitOnPos(p, gammaBitlistList)
        gammaBitlistList = list(
            filter(lambda bitlist: bitlist[p] == bitToKeep, gammaBitlistList)
        )
        if len(gammaBitlistList) == 1:
            oxygenGeneratorRating = bitlistToInt(gammaBitlistList[0])
            break

    epsilonBitlistList = bitlistList
    for p in range(0, len(bitlistList[0])):
        bitToDiscard = mostCommonBitOnPos(p, epsilonBitlistList)
        epsilonBitlistList = list(
            filter(lambda bitlist: bitlist[p] != bitToDiscard, epsilonBitlistList)
        )
        if len(epsilonBitlistList) == 1:
            co2ScrubberRating = bitlistToInt(epsilonBitlistList[0])
            break

    print("Oxygen generator rating:", oxygenGeneratorRating)
    print("CO2 scrubber rating:", co2ScrubberRating)
    print("Result:", oxygenGeneratorRating * co2ScrubberRating)


part2try2()
