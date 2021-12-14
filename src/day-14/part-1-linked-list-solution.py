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

    polymer = DLNode.fromList(polymer)

    return polymer, insertions


class DLNode:
    data = None
    prev = None
    next = None

    def __init__(self, data=None, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next

    def fromList(lst: list):
        first = None
        prev = None
        for el in lst:
            node = DLNode(el, prev=prev)
            if prev:
                prev.next = node
            prev = node

            if not first:
                first = node

        return first

    def toStr(self) -> str:
        values = []
        for el in self:
            values.append(el.data)
        return "".join(values)

    def __repr__(self) -> str:
        return f"<{type(self).__name__}[{'<' if self.prev else ' '}-{'>' if self.next else ' '}]: {self.data}>"

    def __iter__(self):
        yield self
        node = self.next

        while node and node != self:
            yield node
            node = node.next


def pairs(node: DLNode):
    prev = None
    for current in node:
        if prev:
            yield prev, current
        prev = current


def countElements(polymer: DLNode) -> dict[str, int]:
    elementCounts = {}
    for el in polymer:
        count = elementCounts.get(el.data, 0)
        elementCounts[el.data] = count + 1
    return elementCounts


def getMaxMinElementCount(elementCounts) -> tuple[int, int]:
    maxCount = max(elementCounts.values())
    minCount = min(elementCounts.values())
    return (maxCount, minCount)


def polymerize(polymer: DLNode, insertions: dict[str, str]) -> DLNode:
    for left, right in pairs(polymer):
        pairStr = f"{left.data}{right.data}"
        insertion = insertions.get(pairStr)

        if not insertion:
            raise Exception(f"No insertion found for pair {pairStr}")

        node = DLNode(insertion, prev=left, next=right)
        left.next = node
        right.prev = node

    return polymer


#%% Part 1

polymer, insertions = readInp("input.txt")
print("Template:", polymer.toStr())

for step in range(10):
    polymer = polymerize(polymer, insertions)

    polymerStr = polymer.toStr()
    if len(polymerStr) < 30:
        print(f"After step {step}: {polymerStr}")
    else:
        print(f"After step {step}: {polymerStr[:30]}... ({len(polymerStr)})")

elementCounts = countElements(polymer)
print(elementCounts)

maxElementCount, minElementCount = getMaxMinElementCount(elementCounts)

result = maxElementCount - minElementCount
print()
print("Result:", result)
