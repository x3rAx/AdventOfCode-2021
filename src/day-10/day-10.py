#%% Input


def readInp(inp: str):
    with open(inp, "r") as file:
        return [line.strip() for line in file.readlines()]


class Stack:
    _stack = []

    def push(self, sym: str):
        self._stack.append(sym)

    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]


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
