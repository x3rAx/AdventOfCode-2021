#%% Input


from typing import List


def readInp(inp: str):
    with open(inp, "r") as file:
        return [line.strip() for line in file.readlines()]


class Stack:
    _stack: List[str]

    def __init__(self):
        self._stack = []

    def push(self, sym: str):
        self._stack.append(sym)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]

    def toList(self):
        return list(reversed(self._stack))

    def __iter__(self):
        return reversed(self._stack)


#%% Part 1

scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
score = 0
for line in readInp("input.txt"):
    stack = Stack()

    for char in line:
        if char == "(":
            stack.push(")")
            continue
        if char == "[":
            stack.push("]")
            continue
        if char == "{":
            stack.push("}")
            continue
        if char == "<":
            stack.push(">")
            continue

        # Closing correctly
        if char == stack.pop():
            continue

        # Did not close correctly
        score += scores[char]

print("Result:", score)


#%% Part 2

scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}
lineScores = []
for line in readInp("input.txt"):
    stack = Stack()

    for char in line:
        if char == "(":
            stack.push(")")
            continue
        if char == "[":
            stack.push("]")
            continue
        if char == "{":
            stack.push("}")
            continue
        if char == "<":
            stack.push(">")
            continue

        # Closing correctly
        if char == stack.pop():
            continue

        # Did not close correctly (Syntax error) => Skip line
        break
    else:
        score = 0
        for char in stack:
            score *= 5
            score += scores[char]
        lineScores.append(score)

finalScore = sorted(lineScores)[len(lineScores) // 2]
print("Result:", finalScore)
