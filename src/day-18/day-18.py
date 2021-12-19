#%% Setup

from __future__ import annotations

import json
from os import EX_PROTOCOL
from typing import TypeVar, Generic, Union
from icecream import ic
from dataclasses import dataclass
from math import ceil, floor


T = TypeVar("T")


@dataclass()
class Ref(Generic[T]):
    val: T

    def _deref(self, other):
        if type(other) is Ref:
            return other.val
        return other

    def __add__(self, other):
        self.val = Ref(self.val + self._deref(other))

    def __iadd__(self, other):
        self.val += self._deref(other)

    def __eq__(self, other):
        return self.val == self._deref(other)

    def __repr__(self) -> str:
        return f"*{repr(self.val)}"

    def __str__(self) -> str:
        return f"{str(self.val)}"

    def __bool__(self):
        return not not self.val


def left(pair: Ref[list]) -> Ref:
    return pair.val[0]


def right(pair: Ref[list]) -> Ref:
    return pair.val[1]


def descend(selector, pair, stop=lambda el: type(el.val) is not list):
    if stop(pair):
        return pair
    return descend(selector, selector(pair), stop)


def leftmost(pair: Ref[list]) -> Union[Ref, None]:
    return descend(left, pair)


def rightmost(pair: Ref[list]) -> Union[Ref, None]:
    return descend(right, pair)


def findFirst(predicate, pair, stack=None):
    if not stack:
        stack = []

    stack = stack.copy()

    if predicate(pair, stack):
        return pair, stack

    if type(pair.val) is not list:
        return None

    stack.append(pair)

    if result := findFirst(predicate, left(pair), stack):
        return result
    if result := findFirst(predicate, right(pair), stack):
        return result

    return None


def reduce_explode(pair: Ref[list]):
    def exploding(el, stack):
        return type(el.val) is list and len(stack) >= 4

    result = findFirst(exploding, pair)

    if not result:
        return False
    pair, stack = result

    leftBranch = None
    rightBranch = None
    current = pair
    while stack and not (leftBranch and rightBranch):
        child = current
        current = stack.pop()
        leftChild = left(current)
        rightChild = right(current)
        if not leftBranch != None and child is not leftChild:
            leftBranch = leftChild
        if not rightBranch != None and child is not rightChild:
            rightBranch = rightChild

    if leftBranch != None:
        leftNum = rightmost(leftBranch)
        leftNum += left(pair)
    if rightBranch != None:
        rightNum = leftmost(rightBranch)
        rightNum += right(pair)

    pair.val = 0

    return True


def reduce_split(pair: Ref[list]):
    def splitting(el, stack):
        return type(el.val) is int and el.val >= 10

    result = findFirst(splitting, pair)

    if not result:
        return False
    num, _ = result

    num.val = [
        Ref(floor(num.val / 2)),
        Ref(ceil(num.val / 2)),
    ]

    return True


def add(*nums: list[Ref]):
    num = None
    for nextNum in nums:
        if not num:
            num = nextNum
            continue

        ic(num)
        ic("+", nextNum)
        num = Ref([num, nextNum])
        snailfish_reduce(num)
        ic("=", num)
    return num


def snailfish_reduce(num: Ref):
    counter = 0
    while True:
        counter += 1
        print(f"~ {toStr(num)}")
        if reduce_explode(num):
            ic("after explode", num)
            continue
        if reduce_split(num):
            ic("after split", num)
            continue
        break
    return counter > 1


def convertToRefs(el):
    if type(el) is list:
        return Ref([convertToRefs(x) for x in el])
    return Ref(el)


def magnitude(el: Ref):
    if type(el.val) is list:
        return 3 * magnitude(left(el)) + 2 * magnitude(right(el))
    return el.val


COLOR_RED = "\033[91m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[92m"


def toStr(num: Ref, depth=0):
    colorStart = ""
    colorEnd = ""

    if type(num.val) is list:
        if depth >= 4:
            colorStart = COLOR_RED
            colorEnd = COLOR_RESET
        return f"{colorStart}[{', '.join([toStr(el,depth+1) for el in num.val])}]{colorEnd}"

    if depth <= 4:
        colorStart = COLOR_GREEN
        colorEnd = COLOR_RESET

        if num.val > 9:
            colorStart = COLOR_BLUE

    return f"{colorStart}{num}{colorEnd}"


#%% Tests

numbers = [
    "[[[[[9,8],1],2],3],4]",
    "[7,[6,[5,[4,[3,2]]]]]",
    "[[6,[5,[4,[3,2]]]],1]",
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
]

for i, number in enumerate(numbers):
    number = json.loads(number)
    num0 = convertToRefs(number)
    num1 = convertToRefs(number)

    ic.prefix = f"ic| {i}| "
    ic("----------")
    ic(num0)
    ic(reduce_explode(num1))

    ic(num0)
    ic(num1)

ic.prefix = "ic| "
ic("----------")
for i in range(5, 15):
    num = Ref(i)
    reduce_split(num)
    ic(i, num)

ic("----------")

a = convertToRefs(json.loads("[[[[4,3],4],4],[7,[[8,4],9]]]"))
b = convertToRefs(json.loads("[1,1]"))

num = add(a, b)


ic("----------")

ic(magnitude(convertToRefs(4)))
ic(magnitude(convertToRefs([4, 2])))
ic(magnitude(convertToRefs([9, [4, 2]])))

ic(
    magnitude(
        convertToRefs(
            [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
        )
    )
)

ic("----------")
ic(magnitude(convertToRefs([[1, 2], [[3, 4], 5]])) == 143)
ic(magnitude(convertToRefs([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])) == 1384)
ic(magnitude(convertToRefs([[[[1, 1], [2, 2]], [3, 3]], [4, 4]])) == 445)
ic(magnitude(convertToRefs([[[[3, 0], [5, 3]], [4, 4]], [5, 5]])) == 791)
ic(magnitude(convertToRefs([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])) == 1137)
ic(
    magnitude(
        convertToRefs(
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
        )
    )
    == 3488
)

ic("---------- Add numbers test ----------")


nums = [
    [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]],
    [7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]],
    [[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]],
    [[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]],
    [7, [5, [[3, 8], [1, 4]]]],
    [[2, [2, 2]], [8, [8, 1]]],
    [2, 9],
    [1, [[[9, 3], 9], [[9, 0], [0, 7]]]],
    [[[5, [7, 4]], 7], 1],
    [[[[4, 2], 2], 6], [8, 7]],
]
nums = [convertToRefs(num) for num in nums]

partialResults = [
    None,
    "[[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]]",
    "[[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]]",
    "[[[[7, 0], [7, 7]], [[7, 7], [7, 8]]], [[[7, 7], [8, 8]], [[7, 7], [8, 7]]]]",
    "[[[[7, 7], [7, 8]], [[9, 5], [8, 7]]], [[[6, 8], [0, 8]], [[9, 9], [9, 0]]]]",
    "[[[[6, 6], [6, 6]], [[6, 0], [6, 7]]], [[[7, 7], [8, 9]], [8, [8, 1]]]]",
    "[[[[6, 6], [7, 7]], [[0, 7], [7, 7]]], [[[5, 5], [5, 6]], 9]]",
    "[[[[7, 8], [6, 7]], [[6, 8], [0, 8]]], [[[7, 7], [5, 0]], [[5, 5], [5, 6]]]]",
    "[[[[7, 7], [7, 7]], [[8, 7], [8, 7]]], [[[7, 0], [7, 7]], 9]]",
    "[[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]",
]

num = None
ic.disable()
for nextNum, expected in zip(nums, partialResults):
    if not num:
        num = nextNum
        continue

    print(f"  {toStr(num)}")
    print(f"+ {toStr(nextNum)}")
    num = add(num, nextNum)
    result = toStr(num)
    print(f"= {result}")
    print(f"? {expected}")
    print(result == expected)
    print("")


#%% Part 1

ic.disable()
with open("input.txt") as file:
    nums = [convertToRefs(json.loads(line)) for line in file.read().splitlines()]

result = add(*nums)
magn = magnitude(result)

print("Result 1:", magn)
