#%% Setup


def readInp(inp: str):
    polymer = None
    insertions = {}

    with open("input.txt", "r") as file:
        for line in file.read().splitlines():
            if line == "":
                continue

            if not polymer:
                polymer = line
                continue

            pair, insertion = line.split(" -> ")

            if insertions.get(pair):
                raise Exception(f"The pair {pair} already exists")

            insertions[pair] = insertion

    return polymer, insertions


def pairs(string: str):
    for i in range(len(string) - 1):
        yield string[i : i + 2]


def getMaxMinElementCount(elementCounts) -> tuple[int, int]:
    maxCount = max(elementCounts.values())
    minCount = min(elementCounts.values())
    return (maxCount, minCount)


#%% Part 1


def countElements(polymer: str) -> dict[str, int]:
    elementCounts = {}
    for char in polymer:
        count = elementCounts.get(char, 0)
        elementCounts[char] = count + 1
    return elementCounts


def polymerize(polymer: str, insertions: dict[str, str]) -> str:
    offset = 0
    for i, pair in enumerate(pairs(polymer)):
        insertion = insertions.get(pair)

        if not insertion:
            raise Exception(f"No insertion found for pair {pair}")

        polymer = polymer[: i + offset + 1] + insertion + polymer[i + offset + 1 :]
        offset += 1

    return polymer


polymer, insertions = readInp("input.txt")
print("Template:", polymer)

for step in range(10):
    polymer = polymerize(polymer, insertions)

    if len(polymer) < 30:
        print(f"After step {step}: {polymer}")
    else:
        print(f"After step {step}: {polymer[:30]}... ({len(polymer)})")


elementCounts = countElements(polymer)
print(elementCounts)

maxElementCount, minElementCount = getMaxMinElementCount(elementCounts)

result = maxElementCount - minElementCount
print()
print("Result:", result)


#%% Part 2


def countPairs(polymer: str) -> dict[str, int]:
    pairCounts = {}

    for pair in pairs(polymer):
        count = pairCounts.get(pair, 0)
        pairCounts[pair] = count + 1

    return pairCounts


def countElements(pairCounts: dict[str, int], lastElement: str):
    elementCounts = {lastElement: 1}

    for pair, count in pairCounts.items():
        element = pair[0]
        elementSum = elementCounts.get(element, 0)
        elementCounts[element] = elementSum + count

    return elementCounts


def polymerize(
    pairCounts: dict[str, int], insertions: dict[str, str]
) -> dict[str, int]:
    newPairCounts = {}
    for pair, count in pairCounts.items():
        insertion = insertions.get(pair)

        if not insertion:
            raise Exception(f"No insertion found for pair {pair}")

        left = f"{pair[0]}{insertion}"
        right = f"{insertion}{pair[1]}"

        leftCount = newPairCounts.get(left, 0)
        rightCount = newPairCounts.get(right, 0)

        newPairCounts[left] = leftCount + count
        newPairCounts[right] = rightCount + count

    return newPairCounts


polymer, insertions = readInp("input.txt")
print("Template:", polymer)

lastElement = polymer[-1]
pairCounts = countPairs(polymer)

for step in range(40):
    pairCounts = polymerize(pairCounts, insertions)


elementCounts = countElements(pairCounts, lastElement)
print(elementCounts)

maxElementCount, minElementCount = getMaxMinElementCount(elementCounts)

result = maxElementCount - minElementCount
print()
print("Result:", result)
