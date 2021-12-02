#%% Part 1

last = None
count = 0
with open('input.txt') as file:
    for line in file.readlines():
        if last and int(line) > last:
            count += 1
        last = int(line)

print(count)



#%% Part 2

last = None
count = 0
window = []
with open('input.txt') as file:
    for line in file.readlines():
        val = int(line)

        window.append(val)
        if len(window) < 3:
            continue

        s = sum(window)
        window = window[1:]

        if last and s > last:
            count += 1
        last = s

print(count)



#%% Part 1 (Pandas)

import pandas as pd
from pandas.core.frame import DataFrame

# pandas read a text file
df :DataFrame = pd.read_csv('input.txt', header=None)
df = df.diff()
print("Solution:", df[df > 0].dropna().count()[0])

df.hist(bins=150)

#%%

pd.read_csv('input.txt', header=None, names=['A']).diff().query('A > 0').dropna().count()[0]




#%% --- Useful functions to inspect stuff ---
#dir(myObj)
#import dis
#dis.dis(myFunc) # Show disassembly of function
