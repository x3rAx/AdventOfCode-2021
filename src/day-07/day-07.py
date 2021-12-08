#%% Setup

def readPositions(file: str):
    with open(file, 'r') as inp:
        line = inp.readline()
        return [int(x) for x in line.split(',')]


#%% Part 1

import pandas as pd
from pandas import DataFrame

positions = readPositions('input.txt')
positions.sort()
median = positions[int(len(positions)/2)]

result = sum(map(lambda x: abs(median-x), positions))
print("Result:", result)


#%% Part 1 - Pandas

df = pd.read_csv('input.txt', header=None).astype(int).transpose()
med = df.median()
result = (med - df).abs().sum()

print("Result:", result.astype(int)[0])

