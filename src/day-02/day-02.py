#%% Part 1

horiz = 0
depth = 0

with open('input.txt') as file:
    for line in file.readlines():
        direction,amount = line.split(' ', 1)
        amount = int(amount)

        if direction == 'forward':
            horiz += amount
            continue
        if direction == 'down':
            depth += amount
            continue
        if direction == 'up':
            depth -= amount
            continue


print(horiz * depth)



#%% Part 2

horiz = 0
depth = 0
aim = 0

with open('input.txt') as file:
    for line in file.readlines():
        direction,amount = line.split(' ', 1)
        amount = int(amount)

        if direction == 'forward':
            horiz += amount
            depth += amount * aim
            continue
        if direction == 'down':
            aim += amount
            continue
        if direction == 'up':
            aim -= amount
            continue


print(horiz * depth)
