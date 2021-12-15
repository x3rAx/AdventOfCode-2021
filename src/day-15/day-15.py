#%% Setup

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import csgraph


def readCave(inp: str):
    return np.genfromtxt(inp, dtype=int, delimiter=1)


def buildGraph(cave):
    size = len(cave.flat)
    graph = np.zeros((size, size), dtype=int)

    for y in range(cave.shape[0]):
        for x in range(cave.shape[1]):
            pos = y * cave.shape[1] + x

            if y > 0:
                # Above
                above = pos - cave.shape[1]
                graph[pos, above] = cave[y - 1, x]
            if x > 0:
                # Left
                left = pos - 1
                graph[pos, left] = cave[y, x - 1]
            if x < cave.shape[1] - 1:
                # Right
                right = pos + 1
                graph[pos, right] = cave[y, x + 1]
            if y < cave.shape[0] - 1:
                # Below
                below = pos + cave.shape[1]
                graph[pos, below] = cave[y + 1, x]
    return graph


def dijkstra(graph, exitIndex: int):
    sparseGraph = csr_matrix(graph)
    dist_matrix, predecessors = csgraph.dijkstra(
        csgraph=sparseGraph, directed=True, indices=exitIndex, return_predecessors=True
    )

    return predecessors


def leastRisk(cave, predecessors):
    costSum = 0
    pos = 0

    counter = 0
    while predecessors[pos] > -9999:
        counter += 1
        if counter > 10000:
            raise Exception("Maximum iterations exceeded")

        pos = predecessors[pos]
        costSum += cave.flat[pos]
    return costSum


#%% Part 1

cave = readCave("input.txt")
graph = buildGraph(cave)
predecessors = dijkstra(graph, exitIndex=len(cave.flat) - 1)
costSum = leastRisk(cave, predecessors)

print("Result:", costSum)


# --- Alternative 1 ---

# Obviously if you do it right, the `dist_matrix` (even though it is not a
# matrix), really contains the distances of each node to the exit...
sparseGraph = csr_matrix(graph)
dist_matrix = csgraph.dijkstra(
    csgraph=sparseGraph, directed=True, indices=len(cave.flat) - 1
)
print("Alternative 1 - Result:", int(dist_matrix[0]))


# --- Alternative 2 (from HoroTW, thanks <3) ---

# ... Or just let `networx` create a grid graph, set weights and let it find
# the shortest path by weight

from networkx.algorithms.shortest_paths.generic import shortest_path_length
from networkx.classes.digraph import DiGraph
from networkx import grid_2d_graph

inp: np.ndarray = np.genfromtxt("input.txt", delimiter=1, dtype=int)

n = len(inp)
G = grid_2d_graph(n, n, create_using=DiGraph)

for u, v in G.edges:
    G[u][v]["weight"] = inp[v[1]][v[0]]

print("Alternative 2 - Result:", shortest_path_length(G, (0, 0), (n - 1, n - 1), "weight"))


#%% Part 2

from networkx.algorithms.shortest_paths.generic import shortest_path_length
from networkx.classes.digraph import DiGraph
from networkx import grid_2d_graph


def enlargeCave(cave, right: int = 1, down: int = 1):
    newCave = cave.copy()

    # Enlarge to the right
    newCaveParts = []
    for i in range(right):
        newPart = newCave
        newPart = (newPart - 1 + i) % 9 + 1
        newCaveParts.append(newPart)
    newCave = np.block(newCaveParts)

    # Enlarge to the right
    newCaveParts = []
    for i in range(down):
        newPart = newCave
        newPart = (newPart - 1 + i) % 9 + 1
        newCaveParts.append([newPart])
    newCave = np.block(newCaveParts)

    return newCave


cave = readCave("input.txt")
cave = enlargeCave(cave, right=5, down=5)

n = cave.shape[0]
m = cave.shape[1]
G = grid_2d_graph(n, m, create_using=DiGraph)

for u, v in G.edges:
    G[u][v]["weight"] = cave[v[1], v[0]]

print("Result:", shortest_path_length(G, (0, 0), (n - 1, n - 1), "weight"))
