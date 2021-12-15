#%% Part 1

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import csgraph


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
    # For some reason it just works with `directed=True`... So we mirror the
    # graph matrix... But what's this? It works even when we do not mirror it???
    # And it's even faster then!!!
    # graph[graph == 0] = graph.T[graph == 0]

    dGraph = csr_matrix(graph)
    dist_matrix, predecessors = csgraph.dijkstra(
        csgraph=dGraph, directed=True, indices=exitIndex, return_predecessors=True
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


cave = np.genfromtxt("input.txt", dtype=int, delimiter=1)
graph = buildGraph(cave)
predecessors = dijkstra(graph, exitIndex=len(cave.flat) - 1)
costSum = leastRisk(cave, predecessors)

print("Result:", costSum)
