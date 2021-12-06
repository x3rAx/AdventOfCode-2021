#%%

# Python accounts for changes in a list while iterating it, meaning you can
# append an element to the list being iterated and it will also be iterated
# after all other elements have been handled. This can cause an infinite loop
# when adding new elements in each iteration step or might lead to unwanted
# behavior when the list should be iterated multiple time and new elements
# should only be iterated in the next round. Therefore `.copy()` the list before
# iterating it:

myList = [1, 2, 3]
for a in myList.copy():
    print(a, myList)
    myList.append(0)
    # To prevent an infinite loop, exit when the list exceeds a critical size
    if len(myList) > 10:
        break


#%% Input

from os import removexattr
from typing import List


def readInput(file: str):
    with open("input.txt", "r") as inp:
        return [int(fish) for fish in inp.readline().split(",")]


#%% Part 1


def joinScool(scool: List[int], sep: str = ","):
    return sep.join(str(fish) for fish in scool)


scool = readInput("input.txt")

print("Initial state:", joinScool(scool))
for day in range(0, 80):
    for i, fish in enumerate(scool.copy()):
        if fish > 0:
            scool[i] -= 1
            continue
        scool[i] = 6
        scool.append(8)
    print(f"Afterr day {day+1:3}:", joinScool(scool))

print("Result:", len(scool))


#%% Part 2

from typing import Dict, OrderedDict as TOrderedDict
from collections import Counter, OrderedDict
from pprint import pprint


def groupByDaysLeft(scool: List[int]) -> Dict[int, int]:
    # Dict with keys 0 to 8
    scoolDict = dict((k,0) for k in range(0,9))

    spawnDayFrequency = Counter(scool)
    scoolDict.update(spawnDayFrequency)

    return scoolDict


scool = readInput("input.txt")
scoolDict = groupByDaysLeft(scool)
print("Initial state:", scoolDict)

for day in range(0,256):
    newDict = dict((k,0) for k in scoolDict.keys())

    spawnToday = scoolDict[0]

    # Reduce spawn days for all fish with more than 0 days
    for k in range(1, len(scoolDict)):
        val = scoolDict[k]
        newDict[k-1] = val

    # Update days for fish sawning new fish today
    newDict[6] += spawnToday
    # Add new fish
    newDict[8] = spawnToday

    scoolDict = newDict
    print(f"Afterr day {day+1:3}:", scoolDict)


print("Result:", sum(scoolDict.values()))


