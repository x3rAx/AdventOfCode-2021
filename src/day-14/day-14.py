#%%


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


#%% Part 1

polymer, insertions = readInp("input.txt")
print("Template:", polymer)

for step in range(10):
    offset = 0
    for i, pair in enumerate(pairs(polymer)):
        insertion = insertions.get(pair)

        if not insertion:
            raise Exception(f"No insertion found for pair {pair}")

        polymer = polymer[: i + offset + 1] + insertion + polymer[i + offset + 1 :]
        offset += 1

    if len(polymer) < 30:
        print(f"After step {step}: {polymer}")
    else:
        print(f"After step {step}: {polymer[:30]}... ({len(polymer)})")

elementCounts = {}
for char in polymer:
    count = elementCounts.get(char, 0)
    elementCounts[char] = count + 1

print(elementCounts)

maxElementCount = max(elementCounts.values())
minElementCount = min(elementCounts.values())

result = maxElementCount - minElementCount
print()
print("Result:", result)
