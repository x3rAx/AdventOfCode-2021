#%% Setup


class Stack:
    _data: list[str]

    def __init__(self, data=None):
        if not data:
            data = []
        self._data = data

    def push(self, e):
        self._data.append(e)

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data[-1]

    def __len__(self):
        return len(self._data)

    def __repr__(self) -> str:
        return f"<stack : {self._data}>"


# --- Setup graph ---
def readGraph(inp: str):
    G = {}

    with open(inp, "r") as file:
        for line in file.read().splitlines():
            line = line.strip()

            a, b = line.split("-")

            if not G.get(a):
                G[a] = []

            if not G.get(b):
                G[b] = []

            if a not in G[b]:
                G[b].append(a)

            if b not in G[a]:
                G[a].append(b)

    return G


def getAllPaths(G: dict[str, list[str]], maxIters: int) -> list[list[str]]:
    # Some sort of depth first search but we keep track of each incomplete path and
    # in each step just pull one of those incomplete paths and add another node
    # to it and put it back on the stack of incomplete paths until 'end' is found.
    incomplete = Stack()
    incomplete.push(["start"])
    paths = []

    i = 0
    while i < maxIters:
        i += 1
        print("---")

        if not incomplete:
            print("DONE")
            break

        path = incomplete.pop()
        print(f"START FROM {path}")
        node = path[-1]

        if node == "end":
            print("PATH", path)
            paths.append(path)
            continue

        nextNodes = G[node]
        nextNodes = list(filter(lambda x: x.isupper() or x not in path, nextNodes))

        for n in nextNodes:
            incomplete.push(path + [n])

        print("  ", node)
        print("  nextNodes ", nextNodes)
        print("  incomplete", incomplete)

    if i >= maxIters:
        raise Exception(f"Maximum allowed iterations of {maxIters} exceeded")

    return paths


#%% Part 1

G = readGraph("input.txt")
paths = getAllPaths(G, maxIters=100000)

print("")
print("Result:", len(paths))
